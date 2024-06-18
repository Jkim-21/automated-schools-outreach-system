import scrapy
import re
import datetime
from scrapy.selector import Selector

class proto_three(scrapy.Spider):
    name = 'proto_three'
    
    # SETUP:
    # put urls that you want to scrape in links.txt
    # clean output.JSON, does not need to be empty but should be emptied
    #call with: scrapy crawl proto_three -o output.json -a max_depth=1 

    #
    def __init__(self, max_depth=2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = self.read_urls()
        self.visited_urls = set()
        self.max_depth = int(max_depth)

    #parse links in links.txt for __init__
    def read_urls(self):
        with open('links.txt', 'r') as f:
            urls = [url.strip() for url in f.readlines() if url.strip()]
        return urls


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={'depth': 0}) 

    def parse(self, response):
        current_depth = response.meta['depth']
        if current_depth > self.max_depth:
            return
        
        self.visited_urls.add(response.url)
        
        links = response.css('a::attr(href)').getall()

        for link in links:
            absolute_url = response.urljoin(link)
            if absolute_url not in self.visited_urls:
                self.visited_urls.add(absolute_url)
                yield {
                    'type': 'link',
                    'url': absolute_url
                }
                yield response.follow(link, callback=self.parse, meta={'depth': current_depth + 1}) #add meta for other

        
        



#scrapy crawl proto_three -o output.json -a max_depth=1 