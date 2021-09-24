#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
from time import sleep
import logging
from db import DB
import telegram
try:
    import configparser # Python 2
except ImportError:
    import ConfigParser as configparser # Python 3


#hello Roma
#hello Roman
#hello guys!!!

'''Ссылка, с которой будем работать, строка в ссылке ASgCAQECA... -
это base64, в ней зашифрованы параметры поиска от 500руб до 5000руб'''

CONST_URL = "https://www.avito.ru/sankt-peterburg/noutbuki?f=ASgCAQECAUDwvA0UiNI0A" \
           "UXGmgwWeyJmcm9tIjo1MDAsInRvIjo1MDAwfQ&user=1"

CONST_TOKEN_TELEGRAM = "2047879128:AAHjlrjYRxmPFrNJIxbEgw3MLbAsSJhBgHE"
TELEGRAM_CHAT_ID = '294577419'

"""Колличество обявлений который спарим за раз, от 1 до 50"""
CONST_NUM = 2

"""режим отладки вкл/выкл"""
DEBUG = False
UserAgentNow = "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36"



"""Добавил логер для отладки приложения, пишется все в app.log"""

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
if DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

"""Функция get запроса, возвращает объект html страницы, готовый для парсинга"""

def get_url(url):
    headers = {"User-Agent": UserAgentNow}
    s = requests.session()
    s.headers.update(headers)
    r = s.get(url, headers=headers)
    ("PARSED URL: ", url)
    if DEBUG:
        Path("tmp/").mkdir(parents=True, exist_ok=True)
        with open(f'tmp/{url[-10:]}.html', 'wb') as f:
            f.write(r.content)
    s.cookies.clear()
    return BeautifulSoup(r.content, 'lxml')

"""Функция возвращает ссылки для каждого найденного объявления"""
def get_urls_objects(soup):
    result = {}
    logger.info("Parsed URLS...")
    for tag in soup.find_all("div", attrs={"data-marker": "item"}):
        id = tag.get('data-item-id')
        result[id] = 'https://www.avito.ru' + tag.find('a').get('href')
    return result

"""Функция парсит объявление и возращает в виде списка параметров, смотри result[id] ниже"""
def get_one_from_list_objects(soup):
    """в переменую soup передается лист"""
    i = 0
    num = 1
    result = {}  # обявил переменную ресульт как обект словарь
    for id in soup.keys():
        logger.info("Parsed url id: " + id)
        price = 0
        description = "Описание нет"
        tmp = [] #Динамический список
        url = soup[id]
        logger.info("RESULT NUM:" + str(num))
        try:
            data = get_url(url)
            title = data.find(class_="title-info-main").text.strip()
            if data.find(class_="js-item-price").get('content'):
                price = data.find(class_="js-item-price").get('content')
            if data.find(class_="item-description-text"):
                description = data.find(class_="item-description-text").text.strip()
            for image in data.find_all("div", class_="gallery-img-frame"):
                tmp.append(image['data-url'])
            images = ', '.join(str(x) for x in tmp)
            list_params = '\n'.join([str(x.text.strip()) for x in data.find(class_="item-params-list").find_all("li")])
            result[id] = {'url': url, 'title': title, 'price': price, 'list': list_params, 'description': description, 'img': images}
            print("\n".join("{}:\t{}".format(k, v) for k, v in result[id].items()))
        except(BeautifulSoup, EnvironmentError) as e:
            print("Exception is :", e)
            print()
        i += 1
        num += 1
        if i == CONST_NUM:
            break
        sleep(3)
    return result

"""Функци отправки через телеграмм"""
def TelegramSend(data):
    images = data['img'].split(', ')
    bot = telegram.Bot(token=CONST_TOKEN_TELEGRAM)
    try:
        bot.sendPhoto(TELEGRAM_CHAT_ID, images[0], "" + data['price'] + "руб\n" + data['url'] + "\n" + data['list'] + "\n" + data['description'])
    except:
        logger.error("Ощибка")
    sleep(1)

def SQLite3_Database(db_file, data):
    """Иницилизация базы, созданые базы (файла)"""
    db = DB(db_file)

    """Создаем таблицу в базе, если она не создана"""
    db.create_tables()

    """Удаляем старый записи старше CONST_ARCHIVE_DAYS дней (по умолчанию стоит 5)"""
    db.clearOld_record()

    for id in data:

        """Если нет, добавляю в базу"""
        if not db.record_exist(id):
            logger.info("Id" + id + "not found, add in base")
            db.record_add(data)

            """Отправляем сообщение через бота"""
            TelegramSend(data[id])

        else:
            logger.info('Id' + id + 'found in base, skip...')

    """Закрыли соединение с базой"""
    db.close()


logger.info("Start application")
logger.info("User Agent: " + UserAgentNow)
"""Получили html код страницы и запихнули в переменую soup"""
soup = get_url(CONST_URL)

"""Получили список ссылок в виде id = url"""
get_list_urls = get_urls_objects(soup)

"""Проверяем, не пришел ли пустой ответ, не забанил ли нас по ip"""
if not get_list_urls:
    logger.error('Пришел пустой ответ, завершаю аварийную работу')
else:
    """ Получил словарь с объявлениями"""

    array_objects = get_one_from_list_objects(get_list_urls)  #список параметров
    SQLite3_Database("database.db",array_objects)
    if DEBUG:
        print(array_objects)

