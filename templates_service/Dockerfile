FROM --platform=linux/amd64 python:3.10-buster

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/opt/app"

COPY pyproject.toml .

RUN pip3 install poetry==1.4.2 --no-cache-dir
RUN poetry config virtualenvs.create false && poetry install

COPY . .

RUN chmod +x templates_service/run.sh

ENTRYPOINT ["/opt/app/template_serice/run.sh"]
