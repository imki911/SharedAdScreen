FROM python:3.7-alpine

WORKDIR /usr/src/app

COPY publish.py ./
RUN pip install --no-cache-dir paho-mqtt


ENTRYPOINT [ "python", "./publish.py" ]
