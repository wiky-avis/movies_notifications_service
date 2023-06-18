FROM --platform=linux/amd64 python:3.11-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH ./src

WORKDIR /code

RUN pip3 install poetry==1.4.2 --no-cache-dir

COPY notification_controller/poetry.lock notification_controller/pyproject.toml /code/

RUN poetry config experimental.new-installer false && poetry config virtualenvs.create false && poetry install --no-root

COPY . .
