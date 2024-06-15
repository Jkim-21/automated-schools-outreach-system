# Scrapy settings for scrapy_crawler project

BOT_NAME = "scrapy_crawler"

SPIDER_MODULES = ["scrapy_crawler.spiders"]
NEWSPIDER_MODULE = "scrapy_crawler.spiders"

SPLASH_URL = 'http://localhost:8050'


DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723, # Manages cookies for Splash requests
    'scrapy_splash.SplashMiddleware': 725, # Handles the actual request and response processing for Splash
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810, # Ensure the HTTP responses are properly decompressed
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100, # Supports the `cache_args` feature saving disk space by not storing duplicate Splash arguments multiple times in a disk request queue
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage' # Custom cache storage backend

LOG_FILE = 'scrapy_log.txt'

ROBOTSTXT_OBEY = False

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
