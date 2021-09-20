#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
from time import sleep

CONST_URL = "https://www.avito.ru/sankt-peterburg/noutbuki?f=ASgCAQECAUDwvA0UiNI0AUXGmgwWeyJmcm9tIjo1MDAsInRvIjo1MDAwfQ&user=1"
DEBUG = True


def get_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 "
                      "Safari/605.1.15",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    s = requests.session()
    s.headers.update(headers)
    r = s.get(url, headers=headers)
    if DEBUG:
        with open(f'tmp/{url[-10:]}.html', 'wb') as f:
            f.write(r.content)
    s.cookies.clear()
    return BeautifulSoup(r.content, 'lxml')


def get_urls_objects(soup):
    result = {}
    for tag in soup.find_all("div", attrs={"data-marker": "item"}):
        id = tag.get('data-item-id')
        result[id] = 'https://www.avito.ru' + tag.find('a').get('href')
    return result


def get_one_from_list_objects(soup):
    for id in soup.keys():
        result = {}
        url = soup[id]
        data = get_url(url)
        title = data.find(class_="title-info-main").text.strip()
        price = data.find(class_="js-item-price").get('content')
        description = data.find(class_="item-description-text").text.strip()
        list_params = '\n'.join([str(x.text.strip()) for x in data.find(class_="item-params-list").find_all("li")])
        result[id] = {'url': url, 'title': title, 'price': price, 'list': list_params, 'description': description}
        print(id)
        sleep(50)
        break
#    return result


soup = get_url(CONST_URL)
get_list_urls = get_urls_objects(soup) # Список обявлений
if not get_list_urls:
    print("Пришел пустой ответ")
else:
    get_one_from_list_objects(get_list_urls)  # список параметров
