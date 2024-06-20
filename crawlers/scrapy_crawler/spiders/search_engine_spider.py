import scrapy
from scrapy_splash import SplashRequest
import json
import os
import sys
import search_engine_preprocess

class SearchEngineSpider(scrapy.Spider):
    name = "search engine spider"
    allowed_domains = ["startpage.com"]
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.search_queries = search_engine_preprocess.csv_to_array_of_strings_sample("../../data/no_website_schools/search_engine_prep.csv", 3)
    
    def start_requests(self):
        for query in self.search_queries:
            url = f'https://www.startpage.com/do/search?cmd=process_search&query={query}'
            yield SplashRequest(url,
                                args = {'wait': 1})
            

    def parse(self, response):
        directory = './crawl_results'
        filename = os.path.join(directory, 'response.html')
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        
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
            