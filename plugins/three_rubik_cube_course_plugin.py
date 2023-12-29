import json

from .base_plugin import BasePlugin


class ThreeRubikCubeCoursePlugin(BasePlugin):

    def __init__(self):
        super().__init__()
        self.name = "three_rubik_cube_course"
        self.description = "Third Order Rubik's Cube Reduction Tutorial"
        self.params = {
            "type": "object",
            "properties": {},
        }

    def start(self, params):
        return json.dumps({
            "code": 0,
            "data": {
                '第一步': "https://v.douyin.com/i8sfHhmC",
                '第二步': "https://v.douyin.com/i8sfWfDo",
                '第三步': "https://v.douyin.com/i8sPdLH9",
                '第四步': "https://v.douyin.com/i8sP2XE3",
                '第五步': "https://v.douyin.com/i8sP6yDe",
                '第六步': "https://v.douyin.com/i8sPr3us",
                '第七步': "https://v.douyin.com/i8sPrHcN",
            },
            "message": "success"
        })
