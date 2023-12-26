import json

from .base_plugin import BasePlugin


class RewardAuthorPlugin(BasePlugin):

    def __init__(self):
        super().__init__()
        self.name = "reward_author"
        self.description = "reward an author"
        self.params = {
            "type": "object",
            "properties": {},
        }

    """
    我想打赏作者
    """
    def run(self, params):
        res = "微信二维码：http://localhost:8080/static/reward-wechat.jpg"
        return json.dumps({"content": res})
