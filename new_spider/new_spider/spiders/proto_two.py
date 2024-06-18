import scrapy
import re

class proto_two(scrapy.Spider):
    name = 'proto_two'
    
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
        
        
        links = response.css('a::attr(href)').getall()
        for link in links:
            absolute_url = response.urljoin(link)
            if absolute_url not in self.visited_urls:
                self.visited_urls.add(absolute_url)
                yield {
                    'type': 'link',
                    'url': absolute_url
                }

                #can check links here (with regular expressions) to see if they have links embedded before callback - dont need to redo all later then
                    #if it matches the regex empressions pass to -> email set 
                    #

                yield response.follow(link, callback=self.parse, meta={'depth': current_depth + 1})


        emails = re.findall(r'[-a-zA-Z0-9._]+@[-a-zA-Z0-9_]+.[a-zA-Z0-9_.]+', response.text, re.IGNORECASE)
        #see if there is a better response to check - via doc

        email_links = response.css('a[href^=mailto]::attr(href)').getall()
        for email_link in email_links:
            emails.append(email_link.split(':')[1])

        

        text_nodes = response.css('*::text').getall()
        for text in text_nodes:
            emails.extend(re.findall(r'[-a-zA-Z0-9._]+@[-a-zA-Z0-9_]+.[a-zA-Z0-9_.]+', text, re.IGNORECASE))


        for email in set(emails):
            yield {
                'type': 'email',
                'email': email
            }



#scrapy crawl proto_two -o output.json -a max_depth=1 