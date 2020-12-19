# 1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о письмах в базу данных
# (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172

# button = WebDriverWait(driver,10).until(
#             EC.presence_of_element_located((By.CLASS_NAME, 'second-button'))
#         )

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


def add_new_letters(db, list):
    # В качестве аргумента принимает переменную содержащую в себе коллекцию в MONGO и переменныю с списокм
    a = 0
    for el in list:
        db.insert_one(el)
        a = a + 1
    print(f'Added {a} letters to {str(db)}')  # Выдает сообщение о том, сколько было добавлено новостей


client = MongoClient('127.0.0.1', 27017)
db = client['email']
mailru = db.mailru

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
driver.get('https://mail.ru')

elem = driver.find_element_by_class_name('email-input')
elem.send_keys('study.ai_172@mail.ru')
button = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'button'))
        )
button.click()

elem = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'password-input'))
        )
elem.send_keys('NextPassword172')
button = WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'second-button'))
        )
button.click()

elem = WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'llc')][1]")) # Открываю первое письмо
        )
