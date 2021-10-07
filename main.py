#!/usr/bin/python3
import os

import requests
from bs4 import BeautifulSoup
from time import sleep
import logging
from db import DB
import telegram
import re

UserAgentNow = "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36"
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# hello Roma
# hello Roman
# hello guys!!!

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
        elif not bool(re.match(r'^[\d]+:[\w]{1,45}$', get_my_env_var('TELEGRAM_CHAT_ID'))):
            exit("Error Telegram token " + get_my_env_var('TELEGRAM_TOKEN') + "\nget token on https://t.me/BotFather")
        elif get_my_env_var('AVITO_PARSE_URL') is None:
            exit("Error Avito url " + get_my_env_var('AVITO_PARSE_URL') + "\nget token on https://t.me/BotFather")
    except RuntimeError:
        print("!!Environment variable does not exist")


"""Функция get запроса, возвращает объект html страницы, готовый для парсинга"""


def get_url(url):
    headers = {"User-Agent": UserAgentNow}
    s = requests.session()
    s.headers.update(headers)
    r = s.get(url, headers=headers)
    logger.info("PARSED URL: " + url)
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
        logger.info("Parsed url id: " + id)
        price = 0
        description = "Описания нет"
        tmp = []  # Динамический список
        url = soup[id]
        logger.info("RESULT NUM:" + str(num))
        result = {}
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
            result[id] = {'url': url, 'title': title, 'price': price, 'list': list_params, 'description': description,
                          'img': images}
            """Добавление объявления в базу данных,  отправка в бот"""
            SQLite3_Database("database.db", result)

            print("\n".join("{}:\t{}".format(k, v) for k, v in result[id].items()))
        except(BeautifulSoup, EnvironmentError) as e:
            print("Exception is :", e)
            print()
        i += 1
        num += 1
        if i == 30:
            break
        sleep(3)
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


def main():
    try:
        logger.info("Start application")
        logger.info("User Agent: " + UserAgentNow)
        """Получили html код страницы и запихнули в переменную soup"""

        validator_config_env()
        soup = get_url(os.environ.get('AVITO_PARSE_URL'))

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
    main()
