FROM --platform=linux/amd64 python:3.11-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH ./src

WORKDIR /code

RUN pip3 install poetry==1.4.2 --no-cache-dir

COPY notifications_api/poetry.lock notifications_api/pyproject.toml /code/

RUN poetry config experimental.new-installer false && poetry config virtualenvs.create false && poetry install --no-root

COPY . .

RUN chmod +x /code/notifications_api/run.sh

ENTRYPOINT ["/code/notifications_api/run.sh"]