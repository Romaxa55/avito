FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt db.py main.py  ./
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "./main.py" ]