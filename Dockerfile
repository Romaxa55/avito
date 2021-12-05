FROM python:3
ARG TELEGRAM_CHAT_ID
ARG TELEGRAM_TOKEN
ARG AVITO_PARSE_URL
WORKDIR /usr/src/app
COPY requirements.txt db.py main.py user_agents.json test_main.py  ./
RUN pip3 install --no-cache-dir -r requirements.txt
CMD [ "python", "./main.py" ]
