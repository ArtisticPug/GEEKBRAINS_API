from pymongo import MongoClient
from pprint import pprint


client = MongoClient('127.0.0.1', 27017)
db = client['Instagram']
collection = db['instagram']


def search_db(query):
    list = collection.find(query)
    l = 0
    for item in list:
        l += 1
        pprint(item)
    print(f'\nНайдено {l} записей\n')


subbed_to={'subscribed_to': {'mexicalibeer': 2083506881}}
subbed_by={'subscribed_by': {'mexicalibeer': 2083506881}}

search_db(subbed_to), search_db(subbed_by)