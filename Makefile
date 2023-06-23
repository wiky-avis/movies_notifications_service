flake8:
	flake8 --config=.flake8

black:
	black . --config pyproject.toml

isort:
	isort .

mypy:
	mypy notifications_api --explicit-package-bases
	mypy admin_panel --explicit-package-bases
	mypy templates_service --explicit-package-bases
	mypy notification_controller --explicit-package-bases


linters: isort black flake8 mypy

poetry-export:
	poetry export --without-hashes --with dev -f requirements.txt -o .github/requirements/requirements.txt

unit-tests-admin-panel:
	python3 -m pytest admin_panel/tests/src/unit

unit-tests-notifications-api:
	python3 -m pytest notifications_api/tests

unit-tests-notification-controller:
	python3 -m pytest notification_controller/tests

unit-tests: unit-tests-admin-panel unit-tests-notifications-api unit-tests-notification-controller

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
