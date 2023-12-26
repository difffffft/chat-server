from selenium import webdriver
from bs4 import BeautifulSoup


class Chrome:

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        # 浏览器无头模式，可以
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.options)

    def get_soup(self, url):
        self.driver.get(url)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        return soup

    def get_text_from_soup(self, soup):
        return soup.get_text()

    def quit(self):
        self.driver.close()
