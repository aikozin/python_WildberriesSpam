import threading
import time
import tkinter as tk

from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json

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
                    txtEdit.insert(tk.END, f'Открыта страница "{ctalogTitle}" в категории "{nameCategory} \n"')
                    txtEdit.insert(tk.END, f'В категории найдено {newCountBrands} брендов \n')
                except Exception:
                    txtEdit.insert(tk.END, 'Ошибка: Не удалось получить информацию о выбранной категории \n')


        except:
            pass

def start():
    txtEdit.insert(tk.END, 'Шаг 1: Войдите в учетную запись в открывшемся окне браузера Chrome \n')
    # driver.get('https://www.wildberries.ru/security/login?returnUrl=https%3A%2F%2Fwww.wildberries.ru%2Fsecurity%2Flogin'
    #            '%3FreturnUrl%3Dhttps%253A%252F%252Fwww.wildberries.ru%252F')
    driver.get('https://www.wildberries.ru/catalog/krasota/aksessuary/aksessuary-dlya-makiyazha')
    txtEdit.insert(tk.END, 'Шаг 2: Выберите категорию товаров \n')
    thread = threading.Thread(target=updateCategoryInfo).start()

def send():


message = 'Здравствуйте! Мы компания, которая предоставляет услуги в сфере фулфилмента. Мы предложим Вам самую лучшую ' \
          'цену на рынке! Если Вы заинтересованы, напишите обратное сообщение на номер WhatsApp: +7 977 447-88-22. ' \
          'Если Вы дадите обратную связь в течение 3-х дней, мы предоставим Вам дополнительную СКИДКУ в размере 10%. ' \
          'Спасибо за внимание! '
# driver = webdriver.Chrome(service=Service("C:\\Users\\Информационный\\Downloads\\chromedriver.exe"))
driver = webdriver.Chrome(service=Service("C:\\Users\\Teacher_34\\Downloads\\chromedriver.exe"));
driver.maximize_window()

window = tk.Tk()
window.title('Спам Wildberries')
window.geometry('700x500')
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