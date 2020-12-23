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
        if spider.name == 'labirint':
            item['_id'] = self.process_id(item['_id'])
            collection = self.db[spider.name]
            collection.insert_one(item)

        return item

    def process_id(self, _id):
        _id = int(re.search(r'\d+', f'{_id}').group(0))
        return _id

