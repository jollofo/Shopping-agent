import requests
from bs4 import BeautifulSoup
from phi.tools import Toolkit
import json
import queue
import time
import os
from dotenv import load_dotenv
from requests.exceptions import ProxyError, HTTPError

class WebScraper(Toolkit):
    def __init__(self):
        super().__init__(name="web_scraper")
        self.register(self.extract_product_info)
        load_dotenv()

    def extract_product_info(self, url):
        self.headers = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate, br, zstd",
            "Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
        }
        response = requests.get(url, self.headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find('cel_widget_id')
        print(products)
        return soup