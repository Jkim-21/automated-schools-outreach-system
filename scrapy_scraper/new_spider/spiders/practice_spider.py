import scrapy
import re

class practice_spider(scrapy.Spider):
    name = 'practice_spider'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = self.read_urls()

    def read_urls(self):
        with open('links.txt', 'r') as f:
            urls = [url.strip() for url in f.readlines() if url.strip()]
        return urls

    def parse(self,response):
        for link in response.css('a::attr(href)').getall():
            yield{
                'type':'link',
                'url':response.urljoin(link)
            }
        emails = re.findall(r'[\w\.-]+@[\w\.-]+', response.text)

        email_links = response.css('a[href^=mailto]::attr(href)').getall()
        for email_link in email_links:
            emails.append(email_link.split(':')[1])

        span_emails = response.css('span::text').re(r'[\w\.-]+@[\w\.-]+')
        emails.extend(span_emails)

        for email in set(emails):
            yield {
                'type': 'email',
                'email': email
            }




#go deeper with:
'''

for link in response.css('a::attr(href)').getall():
    yield response.follow(link, callback=self.parse)

add a self.visited urls field

urllib.parse
'''

#how to use
#
#
#scrapy crawl practice_spider -o output.json
#
