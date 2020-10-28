FROM python:3.8.6-slim-buster

ADD . /app

WORKDIR /app

RUN apt-get update -y \
 && apt-get autoremove -y \
 && apt-get autoclean \
 && apt-get clean \
 && rm -rf /tmp/* /var/tmp/*

RUN pip --no-cache-dir install -U pip \
 && pip --no-cache-dir install -r /app/requirements.txt

RUN adduser --disabled-password --gecos '' myuser \
 && chown -R myuser /app

ENV PYTHONOPTIMIZE=2

EXPOSE 80
