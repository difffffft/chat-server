import json

from flask import Flask, request, Response
from flask_cors import CORS

from client import base_client, base_model, base_response_headers, get_base_system_messages
from plugins import plugin_list

from config import CONFIG

app = Flask(__name__)
app.static_folder = CONFIG['APP']['STATIC_FOLDER']
CORS(app, supports_credentials=True, resources=r"/*")


@app.route("/chat/token/count", methods=["GET"])
def chat_token_count():
    """
    获取最大token数量
    :return:
    """
    # data = request.json
    response = base_client.chat.completions.create(
        model=base_model,
        prompt="XX",
        max_tokens=1
    )
    return response['usage']['total_tokens']


@app.route("/chat/data-analysis", methods=["POST"])
def chat_data_analysis():
    """
    数据分析，数据整理
    :return:
    """
    data = request.json
    response = base_client.chat.completions.create(
        model=base_model,
        messages=[
            {"role": "system",
             "content": "Please find the answer in the data given by the user"},
            {"role": "user", "content": "data:" + data['data'] + "\nquestions:" + data['prompt']},
        ]
    )
    return response.choices[0].message.content


@app.route("/chat/stream", methods=["POST"])
def chat_stream():
    # 用户的上下文
    context_list = request.json['context_list']
    # 基础上下文
    messages = get_base_system_messages()
    # 封装新的上下文
    for item in context_list:
        for q in item['q']['list']:
            messages.append({
                "role": item['q']['role'],
                "content": q['content']
            })
        for a in item['a']['list']:
            messages.append({
                "role": item['a']['role'],
                "content": a['content']
            })
    # 判断程序是否需要调用工具
    func_response = base_client.chat.completions.create(
        model=base_model,
        messages=messages,
        # 工具列表
        tools=[plugin.info() for plugin in plugin_list],
        tool_choice="auto"
    )
    if func_response:
        response_message = func_response.choices[0].message
        tool_calls = response_message.tool_calls
        # 如果有函数
        if tool_calls:
            messages.append(response_message)
            # 调用函数
            for tool_call in tool_calls:
                plugin_name = tool_call.function.name
                plugin_arguments = tool_call.function.arguments
                # print("运行插件", plugin_name, plugin_arguments)
                plugin = next((plugin for plugin in plugin_list if plugin.name == plugin_name), None)
                if plugin:
                    plugin_response = plugin.run(json.loads(plugin_arguments))
                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": plugin_name,
                            "content": plugin_response,
                        }
                    )
                else:
                    raise Exception(f"插件{plugin_name}不存在")

    # 插件执行完成
    stream_response = base_client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        stream=True
    )

    # 流式响应
    def generate():
        for trunk in stream_response:
            content = trunk.choices[0].delta.content
            if trunk.choices[0].finish_reason != 'stop':
                yield content

    # 流式响应
    return Response(generate(), mimetype='text/event-stream', headers=base_response_headers)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
