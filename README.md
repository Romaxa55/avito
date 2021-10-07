# Avito Porser
=============

### Avito Parser Messages

_Этот репозиторий еще в работе._  

Приложение для парсинга с доски объявлений Авито и отправка интересующих объявление в телеграм бот

###  Установка

`docker pull ellerbrock/bash-it`

### Пример использлвания

**Запусти команду**
```console
docker run -it --rm --name Avito_Parser \ 
-e TELEGRAM_CHAT_ID=test \ 
-e TELEGRAM_TOKEN=12345 \ 
-e AVITO_PARSE_URL="https://www.avito.ru/sankt-peterburg/noutbuki?f=ASgCAQECAUDwvA0UiNI0AUXGmgwWeyJmcm9tIjo1MDAsInRvIjo1MDAwfQ&user=1" \ 
romaxa55/avito
```
