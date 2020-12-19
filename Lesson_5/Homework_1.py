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

import time
from pprint import pprint
import re

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

letter_list = []

driver.get('https://mail.ru')

elem = driver.find_element_by_class_name('email-input')
elem.send_keys('study.ai_172@mail.ru')
button = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'button'))
        )
button.click()

elem = driver.find_element_by_class_name('password-input')
elem.send_keys('NextPassword172')
button = WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'second-button'))
        )
button.click()

elem = WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'llc')][1]"))
        )
driver.get(elem.get_attribute('href'))
timer = 0
while True:
    try:
        letter = {}
        letter['id'] = re.findall(r'0:\d+:0', driver.current_url)[0]
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
        letter.clear()
        timer+=1
        print(timer)

        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(@data-title-shortcut, 'Ctrl+↓')]"))
        )
        button.click()
        time.sleep(1)
    except:
        print('Finished of Error')
        break


# elem = driver.find_element_by_xpath("//a[contains(@class, 'llc')][1]")
# driver.get(elem.get_attribute('href'))
#
# time.sleep(2)
#
# print(driver.find_element_by_class_name('letter__body').text)
