from pprint import pprint
from lxml import html
from datetime import datetime
import requests

# Current date time in local system
print(datetime.now())

print(datetime.date(datetime.now()))

# //div[contains(@class, 'js-module') and contains(@name, 'clb20268335') and contains(@data-module, 'TrackBlocks')]//div[contains(@class, 'daynews__item')] | //div[contains(@class, 'js-module') and contains(@name, 'clb20268335') and contains(@data-module, 'TrackBlocks')]/ul/li

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

            source = item_dom.xpath(".//div[contains(@class, 'article js-article')]/*//span[contains(@class, 'link__text')]/text()")
            name = item_dom.xpath(".//div[contains(@class, 'article js-article')]/*[2]//h1[contains(@class, 'hdr__inner')]/text()")
            date = item_dom.xpath(".//div[contains(@class, 'article js-article')]/*//span[@datetime]/@datetime")

            top_news['source'] = source[0]
            top_news['name'] = name[0]
            top_news['link'] = item_url[0]
            top_news['date'] = date[0].replace('T', ' ')[:19]
            mailru_news_list.append(top_news)
        return mailru_news_list
    except:
        print('Error')

pprint(mailru_news())