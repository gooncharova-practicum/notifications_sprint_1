.PHONY : help clean lint

COMPOSE = docker compose
COMPOSE_FILE = docker-compose.yml
COMPOSE_FILE_DEV = docker-compose.dev.yml
COMPOSE_FILE_TEST = tests/functional/docker-compose.yml

help: ## Show this help
	@printf "\033[33m%s:\033[0m\n" 'Available commands'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[32m%-11s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

clean: ## Remove python compiled cache
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

lint: ## Make lint with ruff and type check with mypy
	ruff .
	mypy .
	black . --check
	isort . --check

format: ## Trigger black formatter and isort util
	black .
	isort .

lints: ## Trigger ruff lint, black formatter, isort util and mypy
	black .
	isort .
	ruff .
	mypy .

migrate: ## Initialize mongo sharded cluster
	docker exec -it app-admin python manage.py migrate
	docker exec -it app-admin python manage.py collectstatic
	docker exec -it app-admin python manage.py createsuperuser

install: ## Prepare prod env
	cp .env.example .env
	cp ./app/.env.example ./app/.env
	cp ./etl/.env.example ./etl/.env

up: ## UP prod containers
	${COMPOSE} up -d $(c) --build

stop: ## Stop prod container
	${COMPOSE} stop $(c)
	${COMPOSE} rm -f $(c)

down: ## Down prod containers
	${COMPOSE} down

restart: ## Restart prod containers
	${COMPOSE} down
	${COMPOSE} up -d

dev-up: ## UP dev containers
	${COMPOSE} -f ${COMPOSE_FILE} -f ${COMPOSE_FILE_DEV} up -d $(c) --build

dev-stop: ## Stop dev container
	${COMPOSE} -f ${COMPOSE_FILE} -f ${COMPOSE_FILE_DEV} stop $(c) \
		&& ${COMPOSE} -f ${COMPOSE_FILE} -f ${COMPOSE_FILE_DEV} rm -f $(c)

dev-down: ## Down dev containers
	${COMPOSE} -f ${COMPOSE_FILE} -f ${COMPOSE_FILE_DEV} down

dev-logs: ## Logs on dev containers
	${COMPOSE} -f ${COMPOSE_FILE} -f ${COMPOSE_FILE_DEV} logs -f $(c)

migrate-test: ## Initialize admin app
	docker exec -it test-app-admin python manage.py migrate

test: ## Run functional tests
	${COMPOSE} -f ${COMPOSE_FILE_TEST} run --quiet-pull --rm --build \
		docker exec -it test-app-admin python manage.py migrate \
		pytest bash -c 'pytest -vv -s'; \
		${COMPOSE} -f ${COMPOSE_FILE_TEST} down
