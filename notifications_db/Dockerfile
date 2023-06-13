FROM python:3.11-slim

WORKDIR /opt/app

RUN mkdir /notifications_db
RUN pip3 install psycopg2-binary yoyo-migrations==8.2.0
WORKDIR /notifications_db

COPY ./notifications_db/migrations ./migrations/