FROM python:3.7-alpine
MAINTAINER Aaron Harris

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
run pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user