# Scrapy settings for scrapy_crawler project
from dotenv import load_dotenv
import os

load_dotenv()

BOT_NAME = "scrapy_crawler"

SPIDER_MODULES = ["scrapy_crawler.spiders"]
NEWSPIDER_MODULE = "scrapy_crawler.spiders"

SPLASH_URL = 'http://localhost:8050'

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723, # Manages cookies for Splash requests
    'scrapy_splash.SplashMiddleware': 725, # Handles the actual request and response processing for Splash
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810, # Ensure the HTTP responses are properly decompressed
    'scrapy_zyte_smartproxy.ZyteSmartProxyMiddleware': 610,
    
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None, # Turns off built in user agent middleware
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100, # Supports the `cache_args` feature saving disk space by not storing duplicate Splash arguments multiple times in a disk request queue
}

FAKEUSERAGENT_PROVIDERS = [
    'scrapy_fake_useragent.providers.FakeUserAgentProvider',  # this is the first provider we'll try
    'scrapy_fake_useragent.providers.FakerProvider',  # if FakeUserAgentProvider fails, we'll use faker to generate a user-agent string for us
    'scrapy_fake_useragent.providers.FixedUserAgentProvider',  # fall back to USER_AGENT value
]

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'

RANDOM_UA_PER_PROXY = True

ZYTE_SMARTPROXY_ENABLED = True
ZYTE_SMARTPROXY_URL = "http://api.zyte.com:8011"
ZYTE_SMARTPROXY_APIKEY = os.getenv('ZYTE_API_KEY')

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage' # Custom cache storage backend

LOG_FILE = './crawl_results/scrapy_log.txt'

ROBOTSTXT_OBEY = False

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
