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


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5']
    # Программирование

    def parse(self, response:HtmlResponse):
        book_links = response.xpath("//a[@class='book-preview__image-link']/@href").extract()

        for link in book_links:
            yield response.follow(link, callback=self.book_parse)

        next_page = response.xpath("//a[text()='Далее']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response:HtmlResponse):
        _id = response.xpath("//div[@class='item-tab__chars-item']/span[contains(text(),'Артикул')]/../span[@class='item-tab__chars-value']/text()").extract_first()
        book_url = response.url
        name = response.xpath("//h1/text()").extract_first()
        author = response.xpath("//a[@itemprop='author']/text()").extract_first()
        old_price = response.xpath("//div[@class='item-actions__price-old']/text()").extract_first()
        if old_price is None:
            old_price = response.xpath("//div[@class='item-actions__price-old']/text()").extract_first()
        new_price = response.xpath("//b[@itemprop='price']/text()").extract_first()
        if new_price is None:
            new_price = response.xpath("//div[@class='item-actions__price']/b/text()").extract_first()
        rating = response.xpath("//span[@class='rating__rate-value']/text()").extract_first()

        yield HomeworkparserItem(
            book_url=book_url,
            name=name,
            author=author,
            old_price=old_price,
            new_price=new_price,
            rating=rating,
            _id=_id
        )