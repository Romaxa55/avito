FROM python:3
ARG TELEGRAM_CHAT_ID
ARG TELEGRAM_TOKEN
ARG AVITO_PARSE_URL
WORKDIR /usr/src/app
COPY requirements.txt db.py main.py .env  ./
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "./main.py" ]