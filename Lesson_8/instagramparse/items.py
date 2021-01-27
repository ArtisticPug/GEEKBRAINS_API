# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramparseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    user_name = scrapy.Field()
    user_full_name = scrapy.Field()
    user_img = scrapy.Field()
    is_private = scrapy.Field()
    subscribed_to = scrapy.Field()
    subscribed_by = scrapy.Field()
    Error = scrapy.Field()
