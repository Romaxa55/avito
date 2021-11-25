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

### Рапуск
```sh
export TELEGRAM_CHAT_ID=тут айди чата \
export TELEGRAM_TOKEN=Токен \
AVITO_PARSE_URL="https://www.avito.ru/sankt-peterburg/noutbuki?cd=1&f=ASgCAQECAUDwvA0UiNI0AUXGmgwUeyJmcm9tIjowLCJ0byI6MzAwMH0&s=104&user=1" \

docker run -d --restart always --name parser -v local-folder-db:/usr/src/app/ -e TELEGRAM_CHAT_ID=$TELEGRAM_CHAT_ID -e TELEGRAM_TOKEN=$TELEGRAM_TOKEN -e AVITO_PARSE_URL=$AVITO_PARSE_URL romaxa55/avito
```


<!--
docker run -it --rm --name Avito_Parser -v local-db:/usr/src/app/ \
-e TELEGRAM_CHAT_ID=-1001550115864 \
-e TELEGRAM_TOKEN=2047879128:AAHjlrjYRxmPFrNJIxbEgw3MLbAsSJhBgHE \
-e AVITO_PARSE_URL="https://www.avito.ru/sankt-peterburg/noutbuki?f=ASgCAQECAUDwvA0UiNI0AUXGmgwWeyJmcm9tIjo1MDAsInRvIjo1MDAwfQ&user=1" \
romaxa55/avito 
 -->
