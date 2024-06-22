import scrapy
import re
import datetime
from scrapy.selector import Selector
from urllib.parse import urlparse
import logging

#imported things:
#re: regex or regular expressions used to find strings
#
#
#

class scraper_final(scrapy.Spider):
    name = 'scraper_final'
    
    # SETUP:
    # put urls that you want to scrape in links.txt
    # clean output.JSON, does not need to be empty but should be emptied
    #call with: scrapy crawl scraper_final -o output.json -a max_depth=1 

    #
    def __init__(self, max_depth=2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = self.read_urls()
        self.visited_urls = set()
        self.max_depth = int(max_depth)
        self.basedomains = [urlparse(url).netloc for url in self.start_urls]

    #parse links in links.txt for __init__
    def read_urls(self):
        with open('links.txt', 'r') as f:
            urls = [url.strip() for url in f.readlines() if url.strip()]
        return urls


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={'depth': 0, 'base_url': url}) 

    def parse(self, response):
        current_depth = response.meta['depth']
        if current_depth > self.max_depth:
            return
        
        self.visited_urls.add(response.url)
        
        links = response.css('a::attr(href)').getall()

        for link in links:
            absolute_url = response.urljoin(link)
            parsed_url = urlparse(absolute_url)
            if parsed_url.netloc in self.basedomains and absolute_url not in self.visited_urls:
                self.visited_urls.add(absolute_url)
                yield {
                    'type': 'link',
                    'url': absolute_url
                }
                
                yield scrapy.Request(absolute_url, callback=self.parse, meta={'depth': current_depth + 1, 'base_url': response.meta['base_url']}) #add meta for other

        emails = re.findall(r'[-a-zA-Z0-9._]+@[-a-zA-Z0-9_]+.[a-zA-Z0-9_.]+', response.text, re.IGNORECASE)
        
        for email in set(emails):
            yield {
                'type': 'email',
                'email': email
            }
        

#different places / ways looking for emails:


