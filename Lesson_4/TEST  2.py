from pprint import pprint
from lxml import html
from datetime import datetime
import requests

# Current date time in local system
print(datetime.now())

print(datetime.date(datetime.now()))

# //div[contains(@class, 'js-module') and contains(@name, 'clb20268335') and contains(@data-module, 'TrackBlocks')]//div[contains(@class, 'daynews__item')] | //div[contains(@class, 'js-module') and contains(@name, 'clb20268335') and contains(@data-module, 'TrackBlocks')]/ul/li

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

pprint(yandex_news())