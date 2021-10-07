# avito
Avito Parser Messages
Приложение парсит первые 10 объявлений, собирает информацию по предложению и направляет о новых предложениях в телеграм бот
Хранение базы индификаторов производится в db SQLite3

Запуск скрипта в контейнере:
docker run -it --rm --name Avito_Parser -e TELEGRAM_CHAT_ID=test -e TELEGRAM_TOKEN=12345 -e AVITO_PARSE_URL="https://www.avito.ru/sankt-peterburg/noutbuki?f=ASgCAQECAUDwvA0UiNI0AUXGmgwWeyJmcm9tIjo1MDAsInRvIjo1MDAwfQ&user=1" romaxa55/avito 