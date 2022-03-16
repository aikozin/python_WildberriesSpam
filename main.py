import time

from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from threading import Thread
import json

message = 'Здравствуйте! Мы компания, которая предоставляет услуги в сфере фулфилмента. Мы предложим Вам самую лучшую ' \
          'цену на рынке! Если Вы заинтересованы, напишите обратное сообщение на номер WhatsApp: +7 977 447-88-22. ' \
          'Если Вы дадите обратную связь в течение 3-х дней, мы предоставим Вам дополнительную СКИДКУ в размере 10%. ' \
          'Спасибо за внимание! '

print('Шаг 1: Войдите в учетную запись в открывшемся окне браузера Chrome')

driver = webdriver.Chrome(service=Service("C:\\Users\\Alex\\Downloads\\chromedriver.exe"))
driver.maximize_window()
# driver.get('https://www.wildberries.ru/security/login?returnUrl=https%3A%2F%2Fwww.wildberries.ru%2Fsecurity%2Flogin'
#            '%3FreturnUrl%3Dhttps%253A%252F%252Fwww.wildberries.ru%252F')
driver.get('https://www.wildberries.ru/catalog/krasota/aksessuary/aksessuary-dlya-makiyazha')

print('Шаг 2: Выберите категорию товаров')

def updateCategoryInfo():
    search = True
    oldCountBrands = 0
    while search:
        time.sleep(0.5)
        try:
            newCountBrands = 0
            for item in driver.requests:
                if 'filters=xsubject;fbrand' in item.url:
                    jsonObject = json.loads(item.response.body)
                    newCountBrands = len(jsonObject['data']['filters'][1]['items'])
            if oldCountBrands != newCountBrands:
                oldCountBrands = newCountBrands
                ctalogTitle = driver.find_element(By.XPATH, "//h1[@class='catalog-title']").text
                nameCategory = ''
                categories = driver.find_elements(By.XPATH, "(//li[@class='breadcrumbs__item'])")
                for i in range(categories.__len__()):
                    nameCategory += categories.__getitem__(i).text + ' / '
                try:
                    print(f'Открыта страница "{ctalogTitle}" в категории "{nameCategory}"')
                    print(f'В категории найдено {newCountBrands} брендов')
                except Exception:
                    print('Ошибка: Не удалось получить информацию о выбранной категории')
        except:
            pass

thread = Thread(target=updateCategoryInfo())
thread.start()