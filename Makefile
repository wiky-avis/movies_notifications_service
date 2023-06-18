flake8:
	flake8 --config=.flake8

black:
	black . --config pyproject.toml

isort:
	isort .

mypy:
	mypy notifications_api --explicit-package-bases
	mypy templates_service --explicit-package-bases


linters: isort black flake8 mypy

unit-tests:
	python3 -m pytest tests/src/unit

up-prod:
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml up --build

up-prod-d:
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml up -d --build

down-prod: 
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml down

up-local:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml up --build

up-local-d:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml up -d --build

down-local:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml down -v
