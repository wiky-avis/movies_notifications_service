FROM python:3.10-slim

ENV LANG C.UTF-8

RUN mkdir /notifications_db
RUN pip install psycopg2-binary yoyo-migrations==8.2.0
WORKDIR /notifications_db

ADD ./notifications_db/migrations ./migrations/
