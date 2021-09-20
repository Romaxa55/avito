#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup

CONST_URL = "https://www.avito.ru/sankt-peterburg/noutbuki?f=ASgCAQECAUDwvA0UiNI0AUXGmgwWeyJmcm9tIjo1MDAsInRvIjo1MDAwfQ&user=1"

headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36",
}

def get_urls_objects(soup):
    result = {}
    for tag in soup.find_all("div", attrs={"data-marker": "item"}):
        id = tag.get('data-item-id')
        result[id] = 'https://www.avito.ru' + tag.find('a').get('href')
    return result

def get_one_from_list_objects(soup):
    for id in soup.keys():
        url = soup[id]
        print(url)
    # print(soup)


s = requests.session()
s.headers.update(headers)
r = s.get(CONST_URL, headers=headers)
# with open('abc.html', 'wb') as f:
#     f.write(r.content)

soup = BeautifulSoup(r.content, 'lxml')
get_one_from_list_objects(get_urls_objects(soup))  #list new obgects