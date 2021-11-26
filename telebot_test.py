import requests
import json
bot_token = '2047879128:AAHjlrjYRxmPFrNJIxbEgw3MLbAsSJhBgHE'
chat_id = "-1001680954808"
files = {
    'photo': 'https://04.img.avito.st/640x480/12143919204.jpg'
}
message = ('https://api.telegram.org/bot'+ bot_token + '/sendPhoto?chat_id='
           + chat_id)
send = requests.post(message, data = files)