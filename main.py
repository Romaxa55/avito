#!/usr/bin/python3
import requests

CONST_URL = "https://www.avito.ru/sankt-peterburg/noutbuki?f=ASgCAQECAUDwvA0UiNI0AUXGmgwWeyJmcm9tIjo1MDAsInRvIjo1MDAwfQ&user=1"

headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36",
}

s = requests.session()
s.headers.update(headers)
r = s.get(CONST_URL, headers=headers)

print(r.url)
print(r.text)
with open('abc.html', 'wb') as f:
    f.write(r.content)


