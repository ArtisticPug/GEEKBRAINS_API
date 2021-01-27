# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient


class InstagramparsePipeline:

    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.db = client['Instagram']


    def process_item(self, item, spider):
        item['_id'] = int(item['_id'])
        try:
            if item.__contains__('subscribed_by'):
                item['subscribed_by'] = {list(item['subscribed_by'].keys())[0]: int(list(item['subscribed_by'].values())[0])}
            elif item.__contains__('subscribed_to'):
                item['subscribed_to'] = {list(item['subscribed_to'].keys())[0]: int(list(item['subscribed_to'].values())[0])}
        except Exception as ex:
            print(ex)
        collection = self.db[spider.name]
        try:
            if collection.find_one({'_id': item['_id']}):
                if item.__contains__('subscribed_by'):
                    if not collection.find_one({'_id': item['_id'], 'subscribed_by': item['subscribed_by']}):
                        collection.update_one(
                            {'_id': item['_id']},
                            {
                                '$push': {'subscribed_by': item['subscribed_by']}
                            },
                            upsert=True
                        )

                if item.__contains__('subscribed_to'):
                    if not collection.find_one({'_id': item['_id'], 'subscribed_to': item['subscribed_to']}):
                        collection.update_one(
                            {'_id': item['_id']},
                            {
                                '$push': {'subscribed_to': item['subscribed_to']}
                            },
                            upsert=True
                        )

            elif not collection.find_one({'_id': item['_id']}):
                if item.__contains__('subscribed_by'):
                    item['subscribed_by'] = [item['subscribed_by']]
                    collection.insert_one(item)
                elif item.__contains__('subscribed_to'):
                    item['subscribed_to'] = [item['subscribed_to']]
                    collection.insert_one(item)
            else:
                collection.insert_one(item)
        except Exception as e:
            print(e)
        return item
