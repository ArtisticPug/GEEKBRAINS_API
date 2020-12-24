# Каждый паук должен собирать:
# * Ссылку на книгу
# * Наименование книги
# * Автор(ы)
# * Основную цену
# * Цену со скидкой
# * Рейтинг книги


import scrapy
from scrapy.http import HtmlResponse
from Lesson_6.homeworkparser.items import HomeworkparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5/']
    # Программирование

    def parse(self, response:HtmlResponse):
        book_links = response.xpath("//a[@class = 'cover']/@href").extract()

        for link in book_links:
            yield response.follow(link, callback=self.book_parse)

        next_page = response.xpath("//a[@class= 'pagination-next__text']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response:HtmlResponse):
        _id = response.xpath("//div[@class='articul']/text()").extract_first()
        book_url = response.url
        name = response.xpath("//div[@id ='product-title']/h1/text()").extract_first()
        author = response.xpath("//a[@data-event-label='author']/text()").extract_first()
        old_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract_first()
        new_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract_first()
        if new_price is None:
            new_price = response.xpath("//span[@class='buying-price-val-number']/text()").extract_first()
        rating = response.xpath("//div[@id='rate']/text()").extract_first()

        yield HomeworkparserItem(
            book_url = book_url,
            name = name,
            author = author,
            old_price = old_price,
            new_price = new_price,
            rating = rating,
            _id = _id
        )
