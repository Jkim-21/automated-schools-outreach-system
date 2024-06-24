import scrapy
from scrapy_splash import SplashRequest
import json
import os
import sys
import importlib

class SearchEngineSpider(scrapy.Spider):
    name = "ip_check_spider"
    allowed_domains = ["httpbin.org"]
    
    def start_requests(self):
        for i in range(3):
            url = 'http://httpbin.org/ip'
            yield scrapy.Request(url,
                                callback=self.parse,
                                dont_filter = True,
                                )

    def parse(self, response):
       ip_address = response.json().get('origin')
       self.logger.info(f"IP Address: {ip_address}")