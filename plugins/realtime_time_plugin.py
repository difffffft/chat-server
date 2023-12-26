import json

from .base_plugin import BasePlugin
from datetime import datetime


class RealtimeTimePlugin(BasePlugin):

    def __init__(self):
        super().__init__()
        self.name = "realtime_time"
        self.description = "get the current time or date"
        self.params = {
            "type": "object",
            "properties": {},
        }

    """
    当前时间
    现在时间是多久
    """
    def run(self, params):
        current_datetime = datetime.now()

        current_date = current_datetime.strftime("%Y-%m-%d")
        current_time = current_datetime.strftime("%H:%M:%S")

        return json.dumps({"content": {
            "current_datetime": current_date,
            "current_date": current_time
        }})
