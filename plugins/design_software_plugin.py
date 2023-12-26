import json
import re

import requests
from bs4 import BeautifulSoup

from chrome import Chrome
from .base_plugin import BasePlugin
from datetime import datetime


class DesignSoftwarePlugin(BasePlugin):

    def __init__(self):
        super().__init__()
        self.name = "design_software_download"
        self.description = "commonly used design software download, When answering, provide the zip password"
        self.params = {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "software name",
                },
            },
            "required": ["name"],
        }

    """
    我想下载ps
    """

    def run(self, params):
        res = {
            "zip_password": "ruancang.net",
            "list": []
        }
        chrome = Chrome()
        soup = chrome.get_soup(f"https://ruancang.net/#/?page=0&id={0}")
        for result in soup.find_all('nz-card'):
            href = result.find_all('a')[0].get('href')
            title = result.find('div', class_=re.compile('^title')).get_text()
            res["list"].append({
                href: href,
                title: title
            })
        chrome.quit()
        return json.dumps({"content": res})
