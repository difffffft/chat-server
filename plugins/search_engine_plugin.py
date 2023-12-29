import re

from .base_plugin import BasePlugin
from chrome import Chrome


class SearchEnginePlugin(BasePlugin):

    def __init__(self):
        super().__init__()

        self.name = "search_engine"
        self.description = "getting information from search engines"
        self.params = {
            "type": "object",
            "properties": {
                "wd": {
                    "type": "string",
                    "description": "keywords",
                },
            },
            "required": ["limit"],
        }

    def start(self, params):
        chrome = Chrome()

        wd = params.get('wd', '')
        soup = chrome.get_soup(f"https://www.bing.com/search?q={wd}")

        res = ""
        for result in soup.find_all('li', class_=re.compile('^b_algo')):
            tag_h2 = result.find('h2')
            tag_a = tag_h2.find('a')
            href = tag_a.get('href')

            # 搜索第一页内容
            chrome_1 = Chrome()
            res_1_soup = chrome_1.get_soup(str(href))
            text = chrome_1.get_text_from_soup(res_1_soup)

            chrome_1.quit()

            # token太多

            res += text
            break

        chrome.quit()
        return res
