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

### Запуск
```sh
export TELEGRAM_CHAT_ID=тут айди чата \
export TELEGRAM_TOKEN=Токен \
export AVITO_PARSE_URL="https://www.avito.ru/sankt-peterburg/noutbuki?cd=1&f=ASgCAQECAUDwvA0UiNI0AUXGmgwUeyJmcm9tIjowLCJ0byI6MzAwMH0&s=104&user=1" \

docker run -d --restart always --name parser -v local-folder-db:/usr/src/app/ -e TELEGRAM_CHAT_ID=$TELEGRAM_CHAT_ID -e TELEGRAM_TOKEN=$TELEGRAM_TOKEN -e AVITO_PARSE_URL=$AVITO_PARSE_URL romaxa55/avito
```
### Проверка что все работает
```sh
docker logs parser

2021-11-25 21:48:16,228 - root - INFO - Start application
2021-11-25 21:48:16,229 - root - INFO - User Agent: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.224 Safari/534.10
2021-11-25 21:48:35,696 - root - INFO - GET request for URL: https://www.avito.ru/sankt-peterburg/noutbuki?cd=1&f=ASgCAQECAUDwvA0UiNI0AUXGmgwUeyJmcm9tIjowLCJ0byI6MzAwMH0&s=104&user=1
2021-11-25 21:48:35,909 - root - INFO - Parsed URLS...
2021-11-25 21:48:35,936 - root - INFO - Id 2238304784 found in base, skip...
2021-11-25 21:48:37,939 - root - INFO - Id 1873663031 found in base, skip...
2021-11-25 21:48:39,941 - root - INFO - Id 2283741623 found in base, skip...
```
```sh
docker ps
CONTAINER ID   IMAGE            COMMAND               CREATED         STATUS          PORTS     NAMES
5ef1f05a818d   romaxa55/avito   "python3 ./main.py"   4 minutes ago   Up 14 seconds             parser
```
```sh
sudo tail -f `docker inspect --format='{{.LogPath}}' parser`

{"log":"2021-11-25 21:55:00,649 - root - INFO - Checking 47.243.160.201:59394\n","stream":"stderr","time":"2021-11-25T21:55:00.650066054Z"}
{"log":"2021-11-25 21:55:04,584 - root - ERROR - Bad status code 47.243.160.201:59394\n","stream":"stderr","time":"2021-11-25T21:55:04.588713991Z"}
{"log":"2021-11-25 21:55:04,586 - root - INFO - Checking 47.243.119.209:59394\n","stream":"stderr","time":"2021-11-25T21:55:04.588846193Z"}
{"log":"2021-11-25 21:55:07,591 - root - ERROR - Error!\n","stream":"stderr","time":"2021-11-25T21:55:07.594531502Z"}
{"log":"2021-11-25 21:55:07,592 - root - INFO - Checking 12.218.209.130:53281\n","stream":"stderr","time":"2021-11-25T21:55:07.594793306Z"}
{"log":"2021-11-25 21:55:09,713 - root - ERROR - Bad status code 12.218.209.130:53281\n","stream":"stderr","time":"2021-11-25T21:55:09.715962069Z"}
{"log":"2021-11-25 21:55:09,714 - root - INFO - Checking 113.160.206.37:55138\n","stream":"stderr","time":"2021-11-25T21:55:09.716110671Z"}
{"log":"2021-11-25 21:55:14,826 - root - ERROR - Bad status code 113.160.206.37:55138\n","stream":"stderr","time":"2021-11-25T21:55:14.82940632Z"}
{"log":"2021-11-25 21:55:14,828 - root - INFO - Checking 202.169.244.181:8181\n","stream":"stderr","time":"2021-11-25T21:55:14.829557822Z"}



```



<!--
docker run -it --rm --name Avito_Parser -v local-db:/usr/src/app/ \
-e TELEGRAM_CHAT_ID=-1001550115864 \
-e TELEGRAM_TOKEN=2047879128:AAHjlrjYRxmPFrNJIxbEgw3MLbAsSJhBgHE \
-e AVITO_PARSE_URL="https://www.avito.ru/sankt-peterburg/noutbuki?f=ASgCAQECAUDwvA0UiNI0AUXGmgwWeyJmcm9tIjo1MDAsInRvIjo1MDAwfQ&user=1" \
romaxa55/avito 
 -->
