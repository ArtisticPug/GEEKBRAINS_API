import pandas as pd
import openpyxl
from bs4 import BeautifulSoup as bs
import requests
import json
import time
from pprint import pprint


# https://hh.ru/vacancies/data-engineer
# vacancy-serp__vacancy
def hhsearch(searchhh, filename):  # Принимает часть поисковой строки с параметрами и имя для json файла
    main_link = 'https://hh.ru'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    job = searchhh
    link = f'{main_link}/vacancies{job}'

    response = requests.get(link, headers=headers)
    soup = bs(response.text, 'html.parser')

    if response.ok:
        completed_jobs_list = []
        while True:
            job_list = soup.find('div', {'class': 'vacancy-serp'})
            job_list_items = job_list.find_all('div', {'class': 'vacancy-serp-item'})
            for job_list_item in job_list_items:
                job_data = {}

                job_name = job_list_item.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})  # Нахожу название вакансии
                name = job_name.text
                job_data['name'] = name

                job_pay = job_list_item.find('span',
                                             {'data-qa': 'vacancy-serp__vacancy-compensation'})  # Нахожу зарплату вакансии
                if job_pay is not None:
                    pay = job_pay.text
                    payment = []
                    currency = []
                    if pay.count('до') == 0 and pay.count('от') == 0 and pay.count(
                            '-') != 0:  # Проверяю формат в котором представлена зарплата: 1) Полный 100 - 200 руб
                        for elem in pay.split('-'):
                            min_max_pay = []
                            pre_currency = []
                            for el in elem:
                                if el.isdigit():
                                    min_max_pay.append(el)
                                elif el.isalpha():
                                    pre_currency.append(el)
                            payment.append(int(''.join(''.join(min_max_pay).split(' '))))
                            currency.append(str(''.join(pre_currency)))

                        payment_min = payment[0]
                        payment_max = payment[1]
                        currency = currency[-1]

                        job_data['payment_min'] = int(payment_min)
                        job_data['payment_max'] = int(payment_max)
                        job_data['currency'] = currency

                    elif pay.count('до') != 0:  # Проверяю формат в котором представлена зарплата: 2) До 200 руб
                        payment_max = []
                        currency = []
                        for elem in pay:
                            if elem.isdigit():
                                payment_max.append(elem)
                        for elem in pay.split(' '):
                            currency.append(elem)
                        payment_max = ''.join(payment_max)
                        payment_min = None
                        currency = currency[-1]

                        job_data['payment_min'] = None
                        job_data['payment_max'] = int(payment_max)
                        job_data['currency'] = currency

                    elif pay.count('от') != 0:  # Проверяю формат в котором представлена зарплата: 2) До 200 руб
                        payment_min = []
                        currency = []
                        for elem in pay:
                            if elem.isdigit():
                                payment_min.append(elem)
                        for elem in pay.split(' '):
                            currency.append(elem)
                        payment_max = None
                        payment_min = ''.join(payment_min)
                        currency = currency[-1]

                        job_data['payment_min'] = int(payment_min)
                        job_data['payment_max'] = None
                        job_data['currency'] = currency

                    elif pay.count('-') == 0 and pay.count('до') == 0 and pay.count('от') == 0:
                        payment_min = []
                        currency = []
                        for elem in pay:
                            if elem.isdigit():
                                payment_min.append(elem)
                        for elem in pay.split(' '):
                            currency.append(elem)
                        payment_max = None
                        payment_min = ''.join(payment_min)
                        currency = currency[-1][:3]

                        job_data['payment_min'] = int(payment_min)
                        job_data['payment_max'] = None
                        job_data['currency'] = currency

                else:
                    job_data['payment_min'] = None
                    job_data['payment_max'] = None
                    job_data['currency'] = None

                job_location = job_list_item.find('span', {'data-qa': 'vacancy-serp__vacancy-address'})
                job_data['Location'] = job_location.text

                job_employer = job_list_item.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'})
                job_data['Employer'] = job_employer.text

                job_link = job_list_item.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
                job_data['Vacancy_link'] = job_link['href']

                job_data['Vacancy_from'] = main_link

                completed_jobs_list.append(job_data)
                # time.sleep(0.5)                 # Замедлял его с той же целью
            next_page = soup.find('a', {
                'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})  # next_page['href'] = '/vacancies/data-engineer?page=1...'
            if next_page is None:  # нахожу кнопку "Дальше" и если ее нет - то обрываю цикл
                print(f'Found {len(completed_jobs_list)} jobs on HeadHunter')  # Использовал, чтобы лучше наблюдать процесс
                break
            link = f'{main_link}{next_page["href"]}'  # подставляю обновленную ссылку на следующую страницу
            response = requests.get(link, headers=headers)
            soup = bs(response.text, 'html.parser')
        with open(f"{filename}.json", "w") as write_HH:
            json.dump(completed_jobs_list, write_HH)
