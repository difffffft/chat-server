import json
import os
import subprocess
from uuid import uuid4

from .base_plugin import BasePlugin


class RunPythonCodePlugin(BasePlugin):

    def __init__(self):
        super().__init__()
        self.name = "run_python_code"
        self.description = "Users can only run python code using this"
        self.params = {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "python code",
                },
            },
            "required": ["code"],
        }

    """
    我桌面的地址是C:\\Users\\67222\\Desktop，帮我在桌面新建一个文件夹，名字叫hello
    
    我桌面的地址是C:\\Users\\67222\\Desktop，桌面有一个文件夹叫hello，里面有很多txt文件，帮我把文件重命名为1-10.txt
    """
    def start(self, params):
        code = params['code']
        file_path = os.path.join(os.getcwd(), f"temp/{uuid4()}.py")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        # 使用cmd运行该文件
        command = f'python {file_path}'
        print("指令文件命令", command)
        # 使用subprocess运行命令
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)
        # 输出命令的执行结果
        return json.dumps({"content": "运行完成"})
