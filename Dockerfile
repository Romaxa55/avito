FROM python:3.7-slim
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip3 install --no-cache-dir -r /usr/src/app/requirements.txt
COPY . /usr/src/app/
WORKDIR /usr/src/app
CMD [ "python", "./main.py" ]
