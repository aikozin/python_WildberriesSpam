import threading
import time
import tkinter as tk
import pyrebase

import requests
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json


search = True
oldEvent = ''
newEvent = ''
userAgent = ''
requestsJson = ''
firebaseConfig = {
  'apiKey': "AIzaSyB7fGTlgTMlPucaSi1Ta1VoiwBbOB2u7Yc",
  'authDomain': "wildberriesspam-d3f26.firebaseapp.com",
  'databaseURL': "https://wildberriesspam-d3f26-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "wildberriesspam-d3f26",
  'storageBucket': "wildberriesspam-d3f26.appspot.com",
  'messagingSenderId': "604940975627",
  'appId': "1:604940975627:web:7a3e190c031a4a1372910e"
}
message = 'Здравствуйте! Мы компания, которая предоставляет услуги в сфере фулфилмента. Мы предложим Вам самую лучшую ' \
          'цену на рынке! Если Вы заинтересованы, напишите обратное сообщение на номер WhatsApp: +7 977 447-88-22. ' \
          'Если Вы дадите обратную связь в течение 3-х дней, мы предоставим Вам дополнительную СКИДКУ в размере 10%. ' \
          'Спасибо за внимание! '


def asyncUpdateCategoryInfo():
    oldCountBrands = 0
    global userAgent
    while search:
        time.sleep(0.5)
        try:
            newCountBrands = 0
            for item in driver.requests:
                if 'filters?appType=' in item.url:
                    jsonObject = json.loads(item.response.body)
                    if search:
                        global requestsJson
                        requestsJson = jsonObject['data']['filters'][1]['items']
                        userAgent = item.headers.get('user-agent')
                        newCountBrands = len(requestsJson)
            if oldCountBrands != newCountBrands:
                oldCountBrands = newCountBrands
                catalogTitle = driver.find_element(By.XPATH, "//h1[@class='catalog-title']").text
                nameCategory = ''
                categories = driver.find_elements(By.XPATH, "(//li[@class='breadcrumbs__item'])")
                for i in range(categories.__len__()):
                    nameCategory += categories.__getitem__(i).text + ' / '
                if search:
                    try:
                        txtEdit.insert(tk.END, f'Открыта страница "{catalogTitle}" в категории "{nameCategory}" \n')
                        txtEdit.insert(tk.END, f'В категории найдено {newCountBrands} брендов \n\n')
                    except Exception:
                        txtEdit.insert(tk.END, 'Ошибка: Не удалось получить информацию о выбранной категории \n')
        except:
            pass


def start():
    txtEdit.insert(tk.END, 'Шаг 1: Войдите в учетную запись в открывшемся окне браузера Chrome \n\n')
    driver.get('https://www.wildberries.ru/security/login?returnUrl=https%3A%2F%2Fwww.wildberries.ru%2Fsecurity%2Flogin'
        '%3FreturnUrl%3Dhttps%253A%252F%252Fwww.wildberries.ru%252F')
    txtEdit.insert(tk.END, 'Шаг 2: Выберите категорию товаров \n\n')
    thread1 = threading.Thread(target=asyncUpdateCategoryInfo)
    thread1.start()


def asyncSendMessages():
    brand = driver.find_element(By.XPATH, '//*[@id="filters"]/*[@data-filter-name="fbrand"]/div[2]/fieldset/label[1]')
    for i in range(0, len(requestsJson)):
        if i % 5 == 0:
            txtEdit.insert(tk.END, f'Получаем токен... \n')
            driver.execute_script(
                'window.open("https://www.wildberries.ru/gettoken", "new_window")')
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(1)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        try:
            txtEdit.insert(tk.END, f'Бренд {i + 1} из {len(requestsJson)} : ')
            txtEdit.insert(tk.END, f'Пишем бренду {requestsJson[i]["name"]}... ')
            driver.execute_script("arguments[0].setAttribute('data-value', '" + str(requestsJson[i]['id']) + "')", brand)
            driver.execute_script("arguments[0].textContent='" + requestsJson[i]['name'] + "'", brand)
            brand.click()
            waitEvent()

            driver.execute_script('window.open("' + driver.find_element(By.XPATH, '//div[@class="product-card-list"]/div[1]/div/a').get_attribute('href') + '", "new_window")')
            waitEvent()
            driver.switch_to.window(driver.window_handles[1])

            driver.find_element(By.XPATH, '//span[@class="same-part-kt__count-review"]').click()
            waitEvent()
            driver.find_element(By.XPATH, '//*[@id="a-Questions"]').click()
            time.sleep(1)
            driver.find_element(By.XPATH, '//textarea[@id="new-question"]').click()
            driver.find_element(By.XPATH, '//textarea[@id="new-question"]').send_keys(message)
            driver.find_element(By.XPATH, '//button[@id="addComment"]').click()
            elemets = driver.find_elements(By.XPATH, '//div[@class="i-popup-publication-answer shown"]')
            if not elemets:
                txtEdit.insert(tk.END, 'Ошибка \n')
            else:
                txtEdit.insert(tk.END, 'Успешно \n')

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            brand.click()
            waitEvent()
        except:
            txtEdit.insert(tk.END, 'Непредвиденная ошибка\n')


def send():
    global search
    global oldEvent
    global newEvent
    search = False
    for item in driver.requests:
        if 'https://www.wildberries.ru/stats/events' in item.url:
            oldEvent = item.__getattribute__('date')
    newEvent = oldEvent
    thread2 = threading.Thread(target=asyncSendMessages).start()


def waitEvent():
    global oldEvent
    global newEvent
    starttime = time.time()
    while newEvent == oldEvent or time.time() - starttime < 10:
        for item in driver.requests:
            if 'https://www.wildberries.ru/stats/events' in item.url:
                newEvent = item.__getattribute__('date')
    oldEvent = newEvent


firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
isAllow = db.child('accessApp').get().val()['isAllow']
if isAllow == 1:
    driver = webdriver.Chrome(service=Service(".\\chromedriver.exe"))
    driver.implicitly_wait(5)
    driver.maximize_window()

    window = tk.Tk()
    window.title('Спам Wildberries')
    window.geometry('900x700')
    window.resizable(width=False, height=False)
    window.rowconfigure(0, minsize=200, weight=1)
    window.columnconfigure(1, weight=1)

    txtEdit = tk.Text(window, wrap=tk.CHAR)
    scroll = tk.Scrollbar(command=txtEdit.yview)
    frameButtons = tk.Frame(window)
    btnStart = tk.Button(frameButtons, text="Начать работу", command=start)
    btnSend = tk.Button(frameButtons, text="Начать рассылку", command=send)

    btnStart.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btnSend.grid(row=1, column=0, sticky="ew", padx=5)

    frameButtons.grid(row=0, column=0, sticky="ns")
    txtEdit.grid(row=0, column=1, sticky="nsew")
    scroll.grid(row=0, column=2, sticky="ns")
    txtEdit.config(yscrollcommand=scroll.set)

    window.mainloop()