# Взять любую категорию товаров на сайте Леруа Мерлен. Собрать с использованием ItemLoader следующие данные:
# ● название;
# ● все фото;
# ● параметры товара в объявлении;
# ● ссылка;
# ● цена.


# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import MapCompose, TakeFirst


def process_to_int(value):  # Преобразую в int то, что получается преобразовать без особой обработки
    try:
        if value != None:
            value = int(re.search(r'\d+', f"{value.replace(' ', '')}").group())
        return value
    except Exception as e:
        print(e)


def process_to_float(value):  # Преобразую во float то, что получается преобразовать без особой обработки
    try:
        new_value =[]
        try:
            value = value.replace('\n', '').replace('  ', '')
            if value.isdigit:
                value = float(value)
                new_value.append(value)
        except:
            new_value.append(value)
        return new_value
    except Exception as e:
        print(e)


class LeroyMerlinItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field(input_processor=MapCompose(process_to_int), output_processor=TakeFirst())  # _id он же артикул товара
    name = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field(input_processor=MapCompose())
    info_key = scrapy.Field(output_processor=MapCompose())
    info_item = scrapy.Field(output_processor=MapCompose(process_to_float))  # Беру весь список
    info = scrapy.Field()
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(process_to_float), output_processor=TakeFirst())  # Беру первое значение