# Makefile variables
APP_NAME := $(shell grep 'APP_NAME' config.toml | sed 's/.*= *//')
DOCKER_COMPOSE := $(shell grep 'COMPOSE_COMMAND' config.toml | sed 's/.*= *//;s/"//g')
DOCKER_COMPOSE_FILE := $(shell grep 'COMPOSE_FILE' config.toml | sed 's/.*= *//')
#
ROOT_PATH := $(shell pwd)
SRC_DIR := $(shell grep 'SRC_DIR' config.toml | sed 's/.*= *//')/
TESTS_DIR := $(shell grep 'TESTS_DIR' config.toml | sed 's/.*= *//')/
PYPROJECT_TOML := $(shell grep 'PYPROJECT_TOML' config.toml | sed 's/.*= *//')
#
SCRIPT_HELP := scripts/makefile/help.sh
SCRIPT_DOTENV_FROM_TOML := scripts/makefile/dotenv_from_toml.sh
SCRIPT_DOCKER_COMPOSE_LOGS := scripts/makefile/docker_logs.sh
SCRIPT_DOCKER_COMPOSE_SHELL := scripts/makefile/docker_shell.sh
SCRIPT_DOCKER_COMPOSE_PRUNE := scripts/makefile/docker_prune.sh
SCRIPT_DOCKER_COMPOSE_RMVOLUMES := scripts/makefile/docker_rmvolumes.sh
SCRIPT_ALEMBIC_INI := scripts/makefile/alembic_ini.sh
SCRIPT_ALEMBIC_ENV := scripts/makefile/alembic_env.sh

# Display help info
.PHONY: help

help:
	@$(SCRIPT_HELP)

# Source code formatting, linting and testing
.PHONY: code.format \
		code.lint \
		code.test \
		code.cov \
		code.covrep \
		code.check

code.format:
	isort $(SRC_DIR)
	black $(SRC_DIR)

code.lint: code.format
	bandit -r $(SRC_DIR) -c $(PYPROJECT_TOML)
	ruff check $(SRC_DIR)
	pylint $(SRC_DIR)
	mypy $(SRC_DIR)

code.test: code.lint
	pytest $(TESTS_DIR) -v

code.cov:
	coverage run --source=$(SRC_DIR) -m pytest $(TESTS_DIR)
	@echo "Ignore CoverageWarning. Run \"make code.covrep\""

code.covrep:
	coverage report

code.check: code.test

# Docker Compose controls
.PHONY: compose.build.docker \
		compose.build.local \
		compose.check-dotenv \
		compose.create_dotenv.docker \
		compose.create_dotenv.local \
		compose.down \
		compose.logs \
		compose.postgres.dotenv.docker \
		compose.postgres.dotenv.local \
		compose.postgres.down \
		compose.postgres.up.docker \
		compose.postgres.up.local \
		compose.prune \
		compose.ps \
		compose.rmvolumes \
		compose.shell \
		compose.test.postgres.down \
		compose.test.postgres.up \
		compose.up.new \
		compose.up.old

compose.build.docker: compose.create_dotenv.docker
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) build

compose.build.local: compose.create_dotenv.local
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) build

compose.check-dotenv:
	$(DOCKER_COMPOSE) run --rm check_dotenv

compose.create_dotenv.docker:
	@$(SCRIPT_DOTENV_FROM_TOML) docker

compose.create_dotenv.local:
	@$(SCRIPT_DOTENV_FROM_TOML) local

compose.down:
	@$(DOCKER_COMPOSE) down

compose.logs:
	@$(SCRIPT_DOCKER_COMPOSE_LOGS) "$(DOCKER_COMPOSE)" $(DOCKER_COMPOSE_FILE)

compose.postgres.dotenv.docker: compose.create_dotenv.docker
	@echo
	@$(MAKE) --no-print-directory compose.check-dotenv

compose.postgres.dotenv.local: compose.create_dotenv.local
	@echo
	@$(MAKE) --no-print-directory compose.check-dotenv

compose.postgres.down:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down db_postgres

compose.postgres.up.docker: compose.create_dotenv.docker
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d db_postgres

compose.postgres.up.local: compose.create_dotenv.local
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d db_postgres

compose.prune:
	@$(SCRIPT_DOCKER_COMPOSE_PRUNE)

compose.ps:
	@docker ps --format "table {{.Names}}\t{{.ID}}\t{{.Status}}\t{{.Ports}}"

compose.rmvolumes:
	@$(SCRIPT_DOCKER_COMPOSE_RMVOLUMES)

compose.shell:
	@$(SCRIPT_DOCKER_COMPOSE_SHELL)

compose.up.new: compose.build.docker
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d db_postgres web_app

compose.up.old:
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d db_postgres web_app

# Testing
compose.test.postgres.up: compose.postgres.dotenv.local
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d db_postgres_test

compose.test.postgres.down: compose.postgres.dotenv.local
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down db_postgres_test

# Alembic database migrations
.PHONY: alembic.async \
		alembic.migration \
		alembic.migrate \
		alembic.downgrade.prev \
		alembic.downgrade.base

alembic.async:
	alembic init -t async alembic
	@$(SCRIPT_ALEMBIC_INI) || echo "SCRIPT_ALEMBIC_INI failed" && true
	@$(SCRIPT_ALEMBIC_ENV) || echo "SCRIPT_ALEMBIC_INI failed" && true
	touch alembic/versions/.keep || echo "SCRIPT_ALEMBIC_INI failed" && true
	@echo "!!! Don't forget to revise alembic.ini and alembic/env.py !!!"
	@echo "!!! At best, you just have to register the models in alembic/env.py !!!"

alembic.migration:
	@if [ -z "$(message)" ]; then \
		echo "Error: message is required. Usage: make alembic.migration message='your message'"; \
		exit 1; \
	fi
	alembic revision --autogenerate -m "$(message)"

alembic.migrate:
	alembic upgrade head

alembic.downgrade.prev:
	alembic downgrade -1

alembic.downgrade.base:
	alembic downgrade base
