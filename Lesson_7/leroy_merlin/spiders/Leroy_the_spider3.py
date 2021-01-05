# Взять любую категорию товаров на сайте Леруа Мерлен. Собрать с использованием ItemLoader следующие данные:
# ● название;
# ● все фото;
# ● параметры товара в объявлении;
# ● ссылка;
# ● цена.


import scrapy
from scrapy.http import HtmlResponse
from Lesson_7.leroy_merlin.items import LeroyMerlinItem
from scrapy.loader import ItemLoader


class LeroyTheSpiderSpider3(scrapy.Spider):
    name = 'Leroy_the_spider3'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super(LeroyTheSpiderSpider3, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response:HtmlResponse):
        links_list = response.xpath("//a[@class='plp-item__info__title']")
        for link in links_list:
            yield response.follow(link, callback=self.carpet_parse)
        next_page = response.xpath("//a[contains(@class, 'next-paginator-button')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def carpet_parse(self, response:HtmlResponse):
        loader = ItemLoader(item=LeroyMerlinItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('images', "//source[contains(@media, '1024px')]/@srcset")  # Все изображения на сайте имею несколько расширений и 1024 это наибольшее,
        loader.add_xpath('info_key', "//dl/div/dt/text()")                          # которое присутствует в каждом товаре сайта
        loader.add_xpath('info_item', "//dl/div/dd/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('_id', "//span[@slot='article']/text()")
        loader.add_value('link', response.url)
        yield loader.load_item()

        # name = response.xpath("//h1/text()").extract_first()
        # images = response.xpath("//source[contains(@media, '1024px')]/@srcset").extract()
        # info = response.xpath("//dl/div").extract()
        # link = response.url
        # price = response.xpath("//span[@slot='price']/text()").extract_first()
        # _id = response.xpath("//span[@slot='article']/text()")
        # yield LeroyMerlinItem(name=name, images=images, info=info, link=link, price=price, _id=_id)
