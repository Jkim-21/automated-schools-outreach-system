import scrapy
import re
from urllib.parse import urlparse
#from bs4 import BeautifulSoup
from scrapy.selector import Selector
import pandas as pd

#json_parser.convert_json()

class school_scraper_1_1(scrapy.Spider):
    name = 'school_scraper_1_1'
    
    # SETUP:
    # put urls that you want to scrape in links.txt
    # clean output.JSON, does not need to be empty but should be emptied
    # call with: scrapy crawl school_scraper_1_1 -o output.json -a max_depth=1 -a show_links=True (True or true both work)
    #

    def __init__(self, max_depth=2, show_links=False, cancel_copies = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.show_links = show_links in ['True','true',True]
        self.cancel_copies = cancel_copies in ['True','true',True]
        self.start_urls = self.read_urls()
        self.visited_urls = set()
        self.max_depth = int(max_depth)
        self.basedomains = [urlparse(url).netloc for url in self.start_urls]
        self.keywebsites = ['directory','activities','music','handbook']
        self.keywords = ['admin@','music@','band@','choir@','deansoffice@','dean@',]
        self.blacklist_keywords = ['news','archive','transport','sports','publication']
        self.completed_domains = set()

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
        
        cur_domain = urlparse(response.url).netloc
        if cur_domain in self.completed_domains:
            return
            #skip domains that have a good enough keyword found

        self.visited_urls.add(response.url)

        emails = re.findall(r'[a-zA-Z0-9._+-]+@[a-zA-Z0-9-]+\.(?:com|net|edu|org|biz|info|gov)', response.text, re.IGNORECASE)
        
        for email in set(emails):
            yield {
                'link': response.url,
                'email': email,
            }

            if any(keyword in email for keyword in self.keywords):
                self.completed_domains.add(cur_domain)
                return
                #if a keyword is matched end the process and 

        links = response.css('a::attr(href)').getall()

        keyword_website_matches = set()

        for link in links:
            if (word in link for word in self.keywebsites):
                keyword_website_matches.add(link)
        
        if len(keyword_website_matches) != 0:
            links = keyword_website_matches

        for link in links:
            absolute_url = response.urljoin(link)
            parsed_url = urlparse(absolute_url)
            if parsed_url.netloc in self.basedomains and absolute_url not in self.visited_urls:
                self.visited_urls.add(absolute_url)

                if self.show_links:
                    yield {
                        'type': 'link',
                        'url': absolute_url
                    }

                if (word not in absolute_url for word in self.blacklist_keywords):
                    #blacklist
                    yield scrapy.Request(absolute_url, callback=self.parse, meta={'depth': current_depth + 1, 'base_url': response.meta['base_url']}) #add meta for other

        
        

#different places / ways looking for emails:


