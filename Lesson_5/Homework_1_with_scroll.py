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
elem.send_keys('HERE_WAS_LOGIN')
button = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'button'))
        )
button.click()

elem = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'password-input'))
        )
elem.send_keys('HERE_WAS_PASSWORD')
button = WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'second-button'))
        )
button.click()

elem = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'llc')]"))
        # Список писем видимых на странице
    )

timer = 0
link_list = []
end = None
while end == None:
    # //a[contains(@class, 'list-letter-spinner')] когда последний ребенок будет таким нужно прервать цикл
    try:
        try:
            end = driver.find_element_by_class_name('list-letter-spinner')
        except:
            end = None
        mail_list = driver.find_elements_by_xpath("//a[contains(@class, 'llc')]")
        for item in mail_list:
            link = item.get_attribute('href')
            if link_list.count(link) == 0 and link != None:
                link_list.append(link)
                timer += 1

        actions = ActionChains(driver)
        actions.move_to_element(mail_list[-1])
        actions.perform()

    except:
        print('ERROR')

timer = 0
timer2 = 0

for link in link_list:
    elem = driver.get(link)
    letter = {}
    letter['_id'] = re.findall(r'0:\d+:0', driver.current_url)[0]
    # В ссылке есть айди письма, которое использую в качестве айди при добавлении в БД

    sender = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'letter-contact'))
    )
    letter['from'] = sender.text

    date = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'letter__date'))
    )
    letter['date'] = date.text

    theme = WebDriverWait(driver, 10).until(
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
    timer2 += 1

    try:
        mailru.insert_one(letter)
        timer += 1
        print(timer)
    except:
        pass
print(f'из {timer2} писем, добавлено {timer} новых в базу {mailru}')
driver.close()

# Этот метод показался более надежным
