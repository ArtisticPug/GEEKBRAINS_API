from pprint import pprint
from pymongo import MongoClient
import json

def salary_search(var_1):
    # Возвращает список вакансий с минимальной ИЛИ максимальной ЗП больше var_1.
    result = []
    try:
        salary = int(var_1)
        for job in hh.find({'$or': [{'payment_min': {'$gt': int(salary)}}, {'payment_max': {'$gt': int(salary)}}]}).sort('payment_min'):
            result.append(job)
    except ValueError:
        print('Error! Value in not valid!')
    return result


def add_new_jobs(db, json):
    # В качестве аргумента принимает переменную содержащую в себе коллекцию в MONGO и переменныю с json.load
    # Создает временный список с ссылками на уже имеющиеся в базе вакансии
    jobs_before = []
    a = 0
    for el in db.find({}):
        jobs_before.append(el['Vacancy_link'][21:])
    # Проверяет список добавляемых на предмет наличия в базе и добавляет если в наличии нет
    for el in json:
        if jobs_before.count(el['Vacancy_link'][21:]) == 0:
            db.insert_one(el)
            a = a + 1
    print(f'Added {a} new jobs')  # Выдает сообщение о том, сколько было добавлено новых вакансий в базу

client = MongoClient('127.0.0.1', 27017)

db = client['jobs']
hh = db.headhunter  # Ссылки на коллекции в MONGO
sj = db.superjob

with open("HeadHunterResults.json", "r") as read_HH:  #Беру json из которого буду добавлять новые вакансии
    read_HH = json.load(read_HH)

pprint(salary_search(100000)[0])

add_new_jobs(hh, read_HH)  # hh - коллекция, read_HH - json.load (список словарей)

with open("SuperjobResults.json", "r") as read_SJ:
    read_SJ = json.load(read_SJ)

add_new_jobs(sj, read_SJ)  # sj - коллекция, read_SJ - json.load (список словарей)

# db.inventory.find( { $or: [ { status: "A" }, { qty: { $lt: 30 } } ] } )
# db.inventory.find( { status: { $in: [ "A", "D" ] } } )

# print(len(list(hh.find({'$or': [{'payment_min': {'$gt': 100000}}, {'payment_max': {'$gt': 100000}}]}))))
# for job in hh.find({'$or': [{'payment_min': {'$gt': 100000}}, {'payment_max': {'$gt': 100000}}]}):
#    pprint(job)
