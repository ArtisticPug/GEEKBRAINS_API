# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HomeworkparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    book_url = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    old_price = scrapy.Field()
    new_price = scrapy.Field()
    rating = scrapy.Field()
