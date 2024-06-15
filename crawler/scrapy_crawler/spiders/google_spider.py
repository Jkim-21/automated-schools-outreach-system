import scrapy
from scrapy_splash import SplashRequest, SlotPolicy
import json


class GoogleSpider(scrapy.Spider):
    name = "google_spider"
    allowed_domains = ["google.com"]
    
    def start_requests(self):
        search_queries = [
            "Belmont High School website",
            "Lexington High School website",
            "Winchester High School website"
        ]
        
        for query in search_queries:
            url = f'https://www.google.com/search?q={query}'
            yield SplashRequest(url,
                                args = {'wait': 1})
            

    def parse(self, response):
        filename = f'response.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        elements = response.css('span.BNeawe').getall()
        self.logger.info(f"Found elements: {elements}")
        
        for element in elements:
            yield {
                'element': element
            }