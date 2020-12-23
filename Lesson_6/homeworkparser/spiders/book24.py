import scrapy


class book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['http://book24.ru/']

    def parse(self, response):
        pass
