# 1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о письмах в базу данных
# (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172


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
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'llc')][1]"))
            # Открываю первое письмо
        )
driver.get(elem.get_attribute('href'))

timer = 0
timer2 = 0
letter_list = []
while True:
    try:
        letter = {}
        letter['_id'] = re.findall(r'0:\d+:0', driver.current_url)[0]
        # В ссылке есть айди письма, которое использую в качестве айди при добавлении в БД

        sender = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'letter-contact'))
        )
        letter['from'] = sender.text

        date = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'letter__date'))
        )
        letter['date'] = date.text

        theme = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH, '//h2'))
        )
        letter['theme'] = theme.text

        elem = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'letter__body'))
        )
        text = elem.text.replace('\n', ' ').split(' ')
        for el in text:
            if el == '':
                text.remove(el)
        letter['text_full'] = ' '.join(text)
        letter_list.append(letter.copy())
        timer2 += 1

        try:
            mailru.insert_one(letter)
            timer += 1
            print(timer)
        except:
            pass


        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(@data-title-shortcut, 'Ctrl+↓')]"))
        )
        button.click()
        # Вместо скролинга использована кнопка "следущее письмо"

        time.sleep(0.8)
        # Вот этот таймер спасает от ошибок

    except:
        print(f'из {timer2} писем, добавлено {timer} новых в базу {mailru}\nFinished or Error occurred')
        break

driver.close()

# В этом методе часто возникала ошибка, возникавшая из-за того, что код начинал обрабатывать блоки до того как они обновились
# В итоге выдавал ошибку что элементы не имеют отношения к текущей странице
# Пришлось ставить таймер
# Начал с этого метода потому из спортивного интереса доделал до конца
