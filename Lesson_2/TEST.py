from pprint import pprint
from pymongo import MongoClient
import json


#testHHoutput.xlsx

with open('HeadHunterResultsTest.json', 'r+') as test_read:
    test_read = json.load(test_read)

with open('HeadHunterResultsTest2.json', 'r+') as test_read2:
    test_read2 = json.load(test_read2)

job_list_before = []
job_list_after = []

for el in test_read:
    print(el['Vacancy_link'][21:])
    job_list_before.append(el['Vacancy_link'][21:])

print('-'*20)

for el in test_read2:
    print(el['Vacancy_link'][21:])
    job_list_after.append(el['Vacancy_link'][21:])

print('-'*20)

print(job_list_before, end=' '), print(len(job_list_before))
print(job_list_after, end=' '), print(len(job_list_after))

print('-'*20)

for el in test_read:
    if job_list_after.count(el['Vacancy_link'][21:]) == 0:
        job_list_after.append(el['Vacancy_link'][21:])

print('-'*20)

print(job_list_before, end=' '), print(len(job_list_before))
print(job_list_after, end=' '), print(len(job_list_after))

print('-'*20)

for el in test_read:
    if job_list_after.count(el['Vacancy_link'][21:]) == 0:
        job_list_after.append(el['Vacancy_link'][21:])
    else:
        print('Уже есть!', end=' ')