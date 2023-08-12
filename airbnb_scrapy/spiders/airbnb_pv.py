import scrapy


class AirbnbPvSpider(scrapy.Spider):
    name = "airbnb_pv"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]

    def parse(self, response):
        pass
