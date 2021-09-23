#!/usr/bin/python3
import logging

import requests     #Люба для выполнения Get запросов
from bs4 import BeautifulSoup   #Модуль для парсингша html
from time import sleep      # Модуль для функции sleep
from pathlib import Path    # Модуль для манипуляция с директориями
# import module
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
# from fake_useragent import UserAgent

#hello Roma
#hello Roman
#hello guys!!!

# Ссылка, с которой будем работать, строка в ссылке ASgCAQECA... -
# это base64 в ней зашифрованы параметры поиска от 500руб до 5000руб
# CONST_URL = "https://www.avito.ru/sankt-peterburg/noutbuki?f=ASgCAQECAUDwvA0UiNI0A" \
#            "UXGmgwWeyJmcm9tIjo1MDAsInRvIjo1MDAwfQ&user=1"
CONST_URL = "https://www.avito.ru/sankt-peterburg/avtomobili/audi/a4-ASgBAgICAkTgtg3elyjitg3inSg?cd=1&radius=0"


# режим отладки вкл/выкл
DEBUG = False
UserAgentNow = "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36"
# Добавил логер для отладки приложения, пишется все в app.log
# get named logger
logger = logging.getLogger(__name__)

# create handler
handler = TimedRotatingFileHandler(filename='app.log', when='D', interval=1, backupCount=90, encoding='utf-8', delay=False)

# create formatter and add to handler
formatter = Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handler to named logger
logger.addHandler(handler)

# set the logging level
logger.setLevel(logging.DEBUG)

# Функция get запроса, возвращает объект  html страницы готовый для парсинга
def get_url(url):
    headers = {"User-Agent": UserAgentNow}
    s = requests.session()
    s.headers.update(headers)
    r = s.get(url, headers=headers)
    print("PARSED URL: ", url)
    if DEBUG:
        Path("tmp/").mkdir(parents=True, exist_ok=True)
        with open(f'tmp/{url[-10:]}.html', 'wb') as f:
            f.write(r.content)
    s.cookies.clear()
    return BeautifulSoup(r.content, 'lxml')

#Функия возращает ссылки для каждого найденого обявления
def get_urls_objects(soup):
    result = {}
    print("Parsed URLS...")
    for tag in soup.find_all("div", attrs={"data-marker": "item"}):
        id = tag.get('data-item-id')
        result[id] = 'https://www.avito.ru' + tag.find('a').get('href')
    return result

# Функция парсит обявление и возращает в виде списка параметра см result[id] ниже
def get_one_from_list_objects(soup):
    # в переменую soup передается лист
    if DEBUG:
        i = 0
    result = {}  # обявил переменную ресульт как обект словарь
    for id in soup.keys():
        print("Parsed url id: ", id)
        price = "Цена не указана"
        description = "Описание нет"
        url = soup[id]
        try:
            data = get_url(url)
            title = data.find(class_="title-info-main").text.strip()
            if data.find(class_="js-item-price").get('content'):
                price = data.find(class_="js-item-price").get('content')
            if data.find(class_="item-description-text"):
                description = data.find(class_="item-description-text").text.strip()
            list_params = '\n'.join([str(x.text.strip()) for x in data.find(class_="item-params-list").find_all("li")])
            result[id] = {'url': url, 'title': title, 'price': price, 'list': list_params, 'description': description}
            print("\nRESULT:")
            print("\n".join("{}:\t{}".format(k, v) for k, v in result[id].items()))
            print("\n")
        except(BeautifulSoup, EnvironmentError) as e:
            print("Exception is :", e)
            print()
        if DEBUG: # если включен дебаг, то сбрасываем цикл на 2-м объявлении
            i += 1
            if i ==2:
                break
        sleep(10)
    return result

logger.info("\n\nStart application")
print("\nStart app wuth UserAgent: ", UserAgentNow)

# Получили html код страницы и запихнули в переменую soup
soup = get_url(CONST_URL)

# Получили список ссылк в виде id = url
get_list_urls = get_urls_objects(soup) # Список обявлений

#Проверяем, не пришел ли пустой ответ, не забанил ли нас по ip
if not get_list_urls:
    logger.error('Пришел пустой ответ, завершаю аварийную работу')
else:
    # Получил словарь с обявлениемя
    array_objects = get_one_from_list_objects(get_list_urls)  # список параметров
    if DEBUG:
        print(array_objects)

