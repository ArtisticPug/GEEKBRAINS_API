from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
import time
from pprint import pprint
import re


client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
hits = db.hits

hits.delete_many({})

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
driver.get('https://www.mvideo.ru/')

# buttons = driver.find_elements_by_xpath("//div[contains(text(),'Хиты продаж')]//ancestor::div[contains(@class, 'gallery-layout_product-set')]//a[contains(@class, 'next-btn')]")
for i in range(3):  # Кликаю по кнопке чтобы в HTML попали все эелементы карусели
    button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Хиты продаж')]//ancestor::div[contains(@class,'gallery-layout_product-set')]//a[contains(@class,'next-btn')]"))  # Кнопка листающая карусель
    )
    button.click()
    time.sleep(0.5)

items_list = []  # Сюда попадает все, что собирается с сайта в сыром виде

# Товары карусели. Довольно долго искал способ сослаться именно на интересующую меня карусель. На сайте их несколько и они идентичные
# В итоге нашел только один надежный способ - оттолкнуться от текста "Хиты продаж"
items = driver.find_elements_by_xpath(
    # "//div[contains(text(),'Хиты продаж')]//ancestor::div[contains(@class,'gallery-layout_product-set')]//li[contains(@class,'gallery-list-item')]//a[@class='sel-product-tile-title']"
    "//div[contains(text(),'Хиты продаж')]//ancestor::div[contains(@class,'gallery-layout_product-set')]//a[@class='sel-product-tile-title']"
)
for item in items:
    items_list.append(item.get_attribute('data-product-info'))

for elem in items_list:
    elem = elem.replace('\n', '').replace('\t', '').replace('"', '').replace('{', '').replace('}', '').split(',')  # Готовлю сырые данные для употребления MONGOО
    element = {}                                                                                                   # .replace('productId', '_id') Для использование id продукта в качестве id в базе,
    for item in elem:                                                                                              # однако т.к скрипт подразумаевает очищение базы с каждым запуском в этом нет смысла
        element.update({f"{item.split(': ')[0]}": f"{item.split(': ')[1]}"})
    try:
        hits.insert_one(element)
    except:
        print('Error')
        pass

driver.close()