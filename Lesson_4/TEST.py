# https://ru.ebay.com/b/Apple-iPhone-11-Pro/9355/bn_7116328165
import requests
from lxml import html
from pprint import pprint

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:84.0) Gecko/20100101 Firefox/84.0'}

url = 'https://ru.ebay.com/b/Apple-iPhone-11-Pro/9355/bn_7116328165'

response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

items = dom.xpath("//li[contains(@class,'s-item')]")

phones = []
for item in items:
    phone = {}
    name = item.xpath(".//h3[@class='s-item__title']/text()")
    price = item.xpath(".//span[@class='s-item__price']//text()")
    image = item.xpath(".//img[@class='s-item__image-img']/@src")

    phone['name'] = name[0]
    phone['price'] = price
    phone['image'] = image[0]
    phones.append(phone)

pprint(phones)