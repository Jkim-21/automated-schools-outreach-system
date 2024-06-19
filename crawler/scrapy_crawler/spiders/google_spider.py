import scrapy
from scrapy_splash import SplashRequest
import json


class GoogleSpider(scrapy.Spider):
    name = "google_spider"
    allowed_domains = ["google.com"]
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.search_queries = [
            "Belmont High School massachusetts website",
            "Lexington High School massachusetts website",
            "Winchester High School massachusetts website"
        ]
    
    def start_requests(self):
        for query in self.search_queries:
            url = f'https://www.startpage.com/do/search?cmd=process_search&query={query}'
            yield SplashRequest(url,
                                args = {'wait': 1})
            

    def parse(self, response):
        filename = 'response.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
            
        elements = response.css('div.result')[:3]
            
        for element in elements:
            link = element.css('span.link-text::text').get()
            main_link = ""
            if link:
                if 'http' in link:
                    link = link[link.index('http'):]
            
            yield {
                'link': link
            }