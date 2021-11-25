# Avito Parser
=============

### Avito Parser Messages

_Этот репозиторий еще в работе._  

Приложение для парсинга с доски объявлений Авито и отправка интересующих объявление в телеграм бот

### Пример использования

####  Установка из докера

```sh
docker pull romaxa55/avito
```
###ИЛИ

####  Установка из репозитория
```sh
git clone https://github.com/Romaxa55/avito.git
cd avito
docker build -t avito .
```

**Запусти команду**
```sh
# Запуск контейнера
docker run -it --rm --name Avito_Parser -v local-db:/usr/src/app/ \
-e TELEGRAM_CHAT_ID=test \
-e TELEGRAM_TOKEN=12345 \
-e AVITO_PARSE_URL="https://www.avito.ru/sankt-peterburg/noutbuki?f=ASgCAQECAUDwvA0UiNI0AUXGmgwWeyJmcm9tIjo1MDAsInRvIjo1MDAwfQ&user=1" \
avito
```




**Запусти команду**
```sh
docker run -it --rm --name Avito_Parser -v local-db:/usr/src/app/ \
-e TELEGRAM_CHAT_ID=test \
-e TELEGRAM_TOKEN=12345 \
-e AVITO_PARSE_URL="https://www.avito.ru/sankt-peterburg/noutbuki?f=ASgCAQECAUDwvA0UiNI0AUXGmgwWeyJmcm9tIjo1MDAsInRvIjo1MDAwfQ&user=1" \
romaxa55/avito
```

<!--
docker run -it --rm --name Avito_Parser -v local-db:/usr/src/app/ \
-e TELEGRAM_CHAT_ID=-1001550115864 \
-e TELEGRAM_TOKEN=2047879128:AAHjlrjYRxmPFrNJIxbEgw3MLbAsSJhBgHE \
-e AVITO_PARSE_URL="https://www.avito.ru/sankt-peterburg/noutbuki?f=ASgCAQECAUDwvA0UiNI0AUXGmgwWeyJmcm9tIjo1MDAsInRvIjo1MDAwfQ&user=1" \
romaxa55/avito 
 -->
