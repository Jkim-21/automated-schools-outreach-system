import scrapy
import re

class PracticeSpider(scrapy.Spider):
    name = 'proto_one'
    
    def __init__(self, max_depth=2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = self.read_urls()
        self.visited_urls = set()
        self.max_depth = int(max_depth)

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
        
        # Extract and yield links
        links = response.css('a::attr(href)').getall()
        for link in links:
            absolute_url = response.urljoin(link)
            if absolute_url not in self.visited_urls:
                self.visited_urls.add(absolute_url)
                yield {
                    'type': 'link',
                    'url': absolute_url
                }
                yield response.follow(link, callback=self.parse, meta={'depth': current_depth + 1})

        # Extract emails from the response text
        emails = re.findall(r'[\w\.-]+@[\w\.-]+', response.text, re.IGNORECASE)

        # Extract emails from mailto links
        email_links = response.css('a[href^=mailto]::attr(href)').getall()
        for email_link in email_links:
            emails.append(email_link.split(':')[1])

        # Extract emails from span elements
        span_emails = response.css('span::text').re(r'[\w\.-]+@[\w\.-]+', re.IGNORECASE)
        emails.extend(span_emails)

        # Yield unique emails
        for email in set(emails):
            yield {
                'type': 'email',
                'email': email
            }



#scrapy crawl proto_one -o output.json -a max_depth=2

