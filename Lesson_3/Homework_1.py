from pprint import pprint
from pymongo import MongoClient
import json

def salary_search(var_1):
    try:
        salary = int(var_1)
        for job in hh.find({'$or': [{'payment_min': {'$gt': int(salary)}}, {'payment_max': {'$gt': int(salary)}}]}).sort('payment_min'):
            pprint(job)
    except ValueError:
        print('Error! Value in not valid!')


client = MongoClient('127.0.0.1', 27017)

db = client['jobs']
hh = db.headhunter
sj = db.superjob

with open("HeadHunterResults.json", "r") as read_HH:
    read_HH = json.load(read_HH)
with open("SuperjobResults.json", "r") as read_SJ:
    read_SJ = json.load(read_SJ)

#db.inventory.find( { $or: [ { status: "A" }, { qty: { $lt: 30 } } ] } )
#db.inventory.find( { status: { $in: [ "A", "D" ] } } )

#print(len(list(hh.find({'$or': [{'payment_min': {'$gt': 100000}}, {'payment_max': {'$gt': 100000}}]}))))
#for job in hh.find({'$or': [{'payment_min': {'$gt': 100000}}, {'payment_max': {'$gt': 100000}}]}):
#    pprint(job)

salary_search(100000)