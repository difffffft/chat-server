from client import base_model
from utils import num_tokens_from_string


class BasePlugin:

    def __init__(self):
        self.name = None
        self.description = None
        self.params = None
        self.danger = False

    def info(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.params
            },
        }

    def start(self, params: dict):
        pass

    def run(self, params: dict):
        res = self.start(params)
        num = num_tokens_from_string(res)
        if num > 15000:
            raise Exception('工具返回TOKEN过长')
        return res
