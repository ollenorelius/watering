FROM python:3.6-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get -y install gcc curl make

RUN pip3 install RPi.GPIO gpiozero

ENV NAME water_world

CMD ["python", "water_daemon.py"]
