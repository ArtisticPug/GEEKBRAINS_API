# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
from pymongo import MongoClient

class HomeworkparserPipeline:

    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.db = client['books']

    def process_item(self, item, spider):
        item['_id'] = self.process_to_int(item['_id'])
        item['old_price'] = self.process_to_int(item['old_price'])
        item['new_price'] = self.process_to_int(item['new_price'])
        item['rating'] = self.process_to_float(item['rating'])
        collection = self.db[spider.name]
        try:
            collection.insert_one(item)
        except:
            pass
        return item

    def process_to_int(self, value):
        if value != None:
            value = int(re.search(r'\d+', f"{value.replace(' ', '')}").group())
        return value

    def process_to_float(self, value):
        if value != None:
            value = float(value.replace(',', '.'))
        return value