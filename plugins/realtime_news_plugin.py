import json
import re

from .base_plugin import BasePlugin
from chrome import Chrome


class RealtimeNewsPlugin(BasePlugin):

    def __init__(self):
        super().__init__()
        self.name = "realtime_news"
        self.description = "get real-time news"
        self.params = {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "number",
                    "description": "number of news",
                },
            },
            "required": ["limit"],
        }

    def start(self, params):
        chrome = Chrome()
        soup = chrome.get_soup("https://top.baidu.com/board?tab=realtime")

        limit = params.get("limit", 10)
        limit_count = 0

        res = ""
        # 换行输出
        res += "\n"

        # 清洗数据
        for result in soup.find_all('div', class_=re.compile('^category-wrap_')):
            if limit_count == limit:
                break
            title = result.find('div', class_='c-single-text-ellipsis').get_text()
            content = result.find('div', class_=re.compile('^hot-desc_')).get_text()
            res += "\n"
            res += "### " + title + "\n"
            res += content.replace("查看更多>", "") + "  \n"
            limit_count += 1

        chrome.quit()

        return json.dumps({"content": res})
