FROM --platform=linux/amd64 python:3.11-buster

WORKDIR /opt/app/notifications_api

RUN pip3 install poetry==1.4.2 --no-cache-dir

COPY notifications_api/poetry.lock notifications_api/pyproject.toml /opt/app/notifications_api/

RUN poetry config experimental.new-installer false && poetry config virtualenvs.create false && poetry install --no-root

COPY . .

RUN chmod +x notifications_api/run.sh

ENTRYPOINT ["notifications_api/run.sh"]
