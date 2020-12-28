# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import hashlib
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes


class LMImagesPipeLine(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['images']:
            for img in item['images']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['images'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'full/{item["_id"]}/{image_guid}.jpg'


class LeroyMerlinPipeline:

    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.db = client['LeroyMerlin']

    def process_item(self, item, spider):
        t = len(item['info_key'])
        item['info'] = self.process_info(item['info_key'], item['info_item'], t)
        del item['info_key']
        del item['info_item']

        collection = self.db[spider.name]
        try:
            collection.insert_one(item)
        except:
            pass
        return item

    def process_info(self, key, item, t):
        list = {}
        for el in range(t):
            list.update({key[el].replace('\n', '').replace('  ', ''): item[el]})
        return list
