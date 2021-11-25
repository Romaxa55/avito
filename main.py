#!/usr/bin/python3
import json
import logging
import os
import random
import re

import urllib3
import socket
from time import sleep

import requests
import telegram
from bs4 import BeautifulSoup

from db import DB

socket.setdefaulttimeout(30)
global_proxy = ""
user_agent_now = ""
DB_FILE="database.db"
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.INFO)



def check_proxy(proxy):
    URL = "https://www.avito.ru"
    TIMEOUT = (3, 20)
    try:
        session = requests.Session()
        session.headers['User-Agent'] = user_agent_now
        session.max_redirects = 300

        logger.info('Checking ' + proxy)
        r = session.get(URL, proxies={'https':'http://' + proxy}, timeout=TIMEOUT,allow_redirects=True)

        if r.ok:
            logger.info('Code  200 for ' + proxy )
            if "7iEzRRMJ2_0p66pVS7wTYYvhZZSFBdzL5FVml4IKUS0" in r.text:
                logger.info('Nice work with Avito proxy is ' + proxy)
                return True
            else:
                logger.info('Cant load page Avito, bad proxy ' + proxy)
        else:
            logger.error('Bad status code ' + proxy )

    except requests.exceptions.ConnectionError as e:
        logger.error('Error!')
        return False
    except requests.exceptions.ConnectTimeout as e:
        logger.error('Error,Timeout!')
        return False
    except requests.exceptions.HTTPError as e:
        logger.error('HTTP ERROR!')
        return False
    except requests.exceptions.Timeout as e:
        logger.error('Error! Connection Timeout!')
        return False
    except urllib3.exceptions.ProxySchemeUnknown as e:
        logger.error('ERROR unkown Proxy Scheme!')
        return False
    except requests.exceptions.TooManyRedirects as e:
        logger.error('ERROR! Too many redirects!')
        return False

def get_my_env_var(env_var):
    if env_var in os.environ:
        return os.environ[env_var]
    else:
        logger.error(env_var + ' env does not exist')
        exit(0)

def validator_config_env():
    try:
        if not bool(re.match(r'^[\-|\d][0-9]+$', get_my_env_var('TELEGRAM_CHAT_ID'))):
            exit("Error Telegram chat_id " + get_my_env_var('TELEGRAM_CHAT_ID'))
        elif not bool(re.match(r'^[\d]+:[\w]{1,45}$', get_my_env_var('TELEGRAM_TOKEN'))):
            exit("Error Telegram token " + get_my_env_var('TELEGRAM_TOKEN') + "\nget token on https://t.me/BotFather")
        elif get_my_env_var('AVITO_PARSE_URL') is None:
            exit("Error Avito url " + get_my_env_var('AVITO_PARSE_URL') + "\nget token on https://t.me/BotFather")
    except RuntimeError:
        print("!!Environment variable does not exist")


"""Функция get запроса, возвращает объект html страницы, готовый для парсинга"""


def get_url(url,use_proxy=False):
    headers = {"User-Agent": user_agent_now}
    s = requests.session()
    s.headers.update(headers)
    if use_proxy:
        r = s.get(url, proxies={'https':'http://' + global_proxy},allow_redirects=True)
    else:
        r = s.get(url)
    logger.info("GET request for URL: " + url)
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
    """обявил переменную result как объект словарь"""
    for id in soup.keys():
        global DB_FILE
        db = DB(DB_FILE)
        if db.record_exist(id):
            logger.info('Id ' + id + ' found in base, skip...')
            result = {}
        else:
            logger.info("Parsed url id: " + id)
            price = 0
            description = "Описания нет"
            tmp = []  # Динамический список
            url = soup[id]
            logger.info("RESULT NUM:" + str(num))
            result = {}
            try:
                data = get_url(url, True)
                title = data.find(class_="title-info-main").text.strip()
                if data.find(class_="js-item-price").get('content'):
                    price = data.find(class_="js-item-price").get('content')
                if data.find(class_="item-description-text"):
                    description = data.find(class_="item-description-text").text.strip()
                for image in data.find_all("div", class_="gallery-img-frame"):
                    tmp.append(image['data-url'])
                images = ', '.join(str(x) for x in tmp)
                list_params = '\n'.join([str(x.text.strip()) for x in data.find(class_="item-params-list").find_all("li")])
                result[id] = {'url': url, 'title': title, 'price': price, 'list': list_params, 'description': description,
                              'img': images}
                """Добавление объявления в базу данных,  отправка в бот"""
                SQLite3_Database(DB_FILE, result)

                print("\n".join("{}:\t{}".format(k, v) for k, v in result[id].items()))
            except(BeautifulSoup, EnvironmentError) as e:
                print("Exception is :", e)
                print()
        """Закрыли соединение с базой"""
        db.close()
        i += 1
        num += 1
        if i == 10:
            break
        sleep(2)
    return result


"""Функция отправки через телеграмм"""


def TelegramSend(data):
    images = data['img'].split(', ')
    bot = telegram.Bot(token=os.environ.get('TELEGRAM_TOKEN'))
    try:
        bot.sendPhoto(os.environ.get('TELEGRAM_CHAT_ID'), images[0],
                      "" + data['price'] + "руб\n" + data['url'] + "\n" + data['list'] + "\n" + data['description'])
    except:
        logger.error("Ошибка")
    sleep(1)


def SQLite3_Database(db_file, data):
    """Иницилизация базы, создание базы (файла)"""
    db = DB(db_file)

    """Создаем таблицу в базе, если она не создана"""
    db.create_tables()

    """Удаляем старые записи старше CONST_ARCHIVE_DAYS дней (по умолчанию стоит 5)"""
    db.clearOld_record()

    for id in data:

        """Если нет, добавляю в базу"""
        if not db.record_exist(id):
            logger.info("Id " + id + " not found, add in base")
            db.record_add(id, data[id])

            """Отправляем сообщение через бота"""
            TelegramSend(data[id])

        else:
            logger.info('Id ' + id + ' found in base, skip...')

    """Закрыли соединение с базой"""
    db.close()

def proxy_parse():
    proxy_page_html = get_url("https://www.sslproxies.org")
    proxies = []
    for tag in proxy_page_html.find_all("tr"):
        cells = tag.findAll("td")
        if len(cells) == 8:
            ip_address = cells[0].find(text=True)
            ip_port = cells[1].find(text=True)
            proxies = ip_address + ":" + ip_port
            if check_proxy(proxies):
                return proxies
    return ""
def main():
    try:
        f = open('user_agents.json')
        # returns JSON object as
        global user_agent_now
        global global_proxy

        db = DB(DB_FILE)

        """Создаем таблицу в базе, если она не создана"""
        db.create_tables()
        db.close()

        user_agent_now = random.choice(json.load(f))
        global_proxy = proxy_parse()
        # Closing file
        f.close()

        logger.info("Start application")
        logger.info("User Agent: " + user_agent_now)
        """Получили html код страницы и запихнули в переменную soup"""

        validator_config_env()
        soup = get_url(os.environ.get('AVITO_PARSE_URL'),True)

        """Получили список ссылок в виде id = url"""
        get_list_urls = get_urls_objects(soup)

        """Проверяем, не пришел ли пустой ответ, не забанили ли нас по ip"""
        if not get_list_urls:
            logger.error('Пришел пустой ответ, завершаю аварийную работу')
        else:
            """ Получил словарь с объявлениями"""

            get_one_from_list_objects(get_list_urls)  # список параметров

    except RuntimeError:
        print("!!Environment variable does not exist")


if __name__ == '__main__':
    while 1:
        main()
        sleep(10)
