# Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.

# if db.count_documents({'Vacansy_link':el['Vacancy_link'][21:]) == 0:
#     db.insert_one(el)

from pymongo import MongoClient
from pprint import pprint
from lxml import html
from datetime import datetime
import requests


def yandex_news():
    yandex_news_list = []
    try:
        url = 'https://yandex.ru/news/'
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        response = requests.get(url, headers=header)
        dom = html.fromstring(response.text)

        items = dom.xpath("//div[contains(@class, 'news-top-stories')]/*")
        for item in items:
            top_news = {}

            source = item.xpath(".//span[contains(@class, 'mg-card-source__source')]/a/text()")
            name = item.xpath(".//h2[contains(@class, 'mg-card__title')]/text()")
            link = item.xpath(".//span[contains(@class, 'mg-card-source__source')]/a/@href")
            date = item.xpath(".//span[contains(@class, 'mg-card-source__time')]/text()")

            top_news['source'] = source[0]
            top_news['name'] = name[0]
            top_news['link'] = link[0]
            top_news['date'] = f"{datetime.date(datetime.now())} {date[0]}"
            yandex_news_list.append(top_news)
        return yandex_news_list
    except:
        print('Error')


def lenta_news():
    lenta_news_list = []
    try:
        url = 'https://lenta.ru/'
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        response = requests.get(url, headers=header)
        dom = html.fromstring(response.text)

        items = dom.xpath("//section[contains(@class, 'b-top7-for-main')]/div/div[contains(@class, 'item')]//a[@href and ./time]")
        for item in items:
            top_news = {}

            name = item.xpath("./text()")
            link = item.xpath("./@href")
            date = item.xpath("./time/@datetime")

            top_news['source'] = 'lenta.ru'
            top_news['name'] = name[0].replace('\xa0', ' ')
            top_news['link'] = f"{url}{link[0]}"
            top_news['date'] = date
            lenta_news_list.append(top_news)
        return lenta_news_list
    except:
        print('Error')


def mailru_news():
    mailru_news_list = []
    try:
        url = 'https://news.mail.ru/'
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        response = requests.get(url, headers=header)
        dom = html.fromstring(response.text)

        items = dom.xpath("//div[contains(@class, 'js-module') and contains(@name, 'clb20268335') and contains(@data-module, 'TrackBlocks')]//div[contains(@class, 'daynews__item')] | //div[contains(@class, 'js-module') and contains(@name, 'clb20268335') and contains(@data-module, 'TrackBlocks')]/ul/li")
        for item in items:
            item_url = item.xpath("./a/@href")
            irem_response = requests.get(item_url[0])
            item_dom = html.fromstring(irem_response.text)
            top_news = {}

            source = item_dom.xpath(".//div[contains(@class, 'article js-article js-module')]/*[1]//span[contains(@class, 'link__text')]/text()")
            name = item_dom.xpath(".//div[contains(@class, 'article js-article js-module')]/*[2]//h1[contains(@class, 'hdr__inner')]/text()")
            date = item_dom.xpath(".//div[contains(@class, 'article js-article js-module')]/*//span[@datetime]/@datetime")

            top_news['source'] = source[0]
            top_news['name'] = name[0]
            top_news['link'] = item_url[0]
            top_news['date'] = date[0].replace('T', ' ')[:19]
            mailru_news_list.append(top_news)
        return mailru_news_list
    except:
        print('Error')


def add_new_news(db, list):
    # В качестве аргумента принимает переменную содержащую в себе коллекцию в MONGO и переменныю с списокм
    a = 0
    for el in list:
        if db.count_documents({'link': el['link']}) == 0:
            db.insert_one(el)
            a = a + 1
    print(f'Added {a} news to {str(db)}')  # Выдает сообщение о том, сколько было добавлено новостей


client = MongoClient('127.0.0.1', 27017)
db = client['News']
yandex = db.yandex
lenta = db.lenta
mailru = db.mailru

add_new_news(yandex, yandex_news())
add_new_news(lenta, lenta_news())
add_new_news(mailru, mailru_news())

