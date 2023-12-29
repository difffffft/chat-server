import json
import time

from flask import Flask, request, Response
from flask_cors import CORS
from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageToolCall
from openai.types.chat.chat_completion_message_tool_call import Function

from client import base_client, base_model, base_response_headers, get_base_system_messages
from plugins import plugin_list

from config import CONFIG
from utils import num_tokens_from_string

app = Flask(__name__)
app.static_folder = CONFIG['APP']['STATIC_FOLDER']
CORS(app, supports_credentials=True, resources=r"/*")


def get_all_context_messages():
    """
    获取所有的上下问对话
    :return:
    """
    # 用户的上下文
    chat_list = request.json['chat_list']
    # 基础上下文
    messages = []
    # 清洗上下文数据
    for item in chat_list:
        # 函数调用
        if item.get('tool_calls', None):
            tool_calls = []
            for n in item['tool_calls']:
                tool_calls.append(ChatCompletionMessageToolCall(id=n['id'], type=n['type'],
                                                                function=Function(arguments=n['function']['arguments'],
                                                                                  name=n['function']['name'])))
            messages.append(ChatCompletionMessage(content=item['content'], role=item['role'],
                                                  tool_calls=tool_calls))
        # 调用结果
        elif item.get('tool_call_id', None):
            messages.append({
                "tool_call_id": item['tool_call_id'],
                "name": item['name'],
                "role": item['role'],
                "content": item['content'],
            })
        else:
            messages.append({
                "role": item['role'],
                "content": item['content'],
            })
    return messages


def clear_tool(context_messages):
    if isinstance(context_messages[-1], dict) and context_messages[-1].get('tool_call_id'):
        context_messages.pop(-1)
        clear_tool(context_messages)
    else:
        pass


# 清洗数据
def get_context_messages(token_num=0):
    token_str = ""
    all_context_messages = get_all_context_messages()
    context_messages = []
    for item in all_context_messages[::-1]:
        if isinstance(item, dict):
            if item['content']:
                token_str += item['content']
        else:
            if item.content:
                token_str += item.content

        token_num += num_tokens_from_string(token_str)
        if token_num < 15000:
            context_messages.append(item)
        else:
            break

    # 如果截取到tool_call_id
    clear_tool(context_messages)

    base_context_messages = get_base_system_messages()
    for item in base_context_messages[::-1]:
        context_messages.append(item)

    context_messages.reverse()

    print(context_messages)
    return context_messages


@app.route("/chat/have/plugin/list", methods=["POST"])
def chat_have_plugin_list():
    messages = get_context_messages()

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
        # 如果有插件
        if tool_calls:
            danger_flag = False
            for tool_call in tool_calls:
                plugin_name = tool_call.function.name
                plugin = next((plugin for plugin in plugin_list if plugin.name == plugin_name), None)
                if plugin:
                    if plugin.danger:
                        danger_flag = True
                else:
                    raise Exception(f"插件{plugin_name}不存在")

            res = response_message.model_dump_json()
            return {
                "danger_flag": danger_flag,
                "plugin_list": json.loads(res)
            }
        else:
            return json.dumps(None)


@app.route("/chat/run/plugin/list", methods=["POST"])
def chat_run_plugin_list():
    """
    运行插件列表
    :return:
    """
    tool_calls = request.json['tool_calls']
    for tool_call in tool_calls:
        plugin_name = tool_call['function']['name']
        plugin_arguments = tool_call['function']['arguments']
        plugin = next((plugin for plugin in plugin_list if plugin.name == plugin_name), None)
        if plugin:
            try:
                plugin_response = plugin.run(json.loads(plugin_arguments))
                tool_call['response'] = plugin_response
            except Exception as e:
                print(e)
                raise Exception('插件运行异常')
        else:
            raise Exception(f"插件{plugin_name}不存在")
    return tool_calls


@app.route("/chat/stream", methods=["POST"])
def chat_stream():
    messages = get_context_messages()
    messages.append({
        "role": "system",
        "content": "You can only answer the user markdown format!"
    })
    # 开始回答问题
    stream_response = base_client.chat.completions.create(
        model=base_model,
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
