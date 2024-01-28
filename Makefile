DOCKER_COMPOSE=docker compose
DOCKER_ENVIRONMENT=docker-compose.yml
PRE_RUN_API_COMMAND=${DOCKER_COMPOSE} -f ${DOCKER_ENVIRONMENT} run --rm chat-cleaner-app
PACKAGE_NAME=chatcleaner
VENV_FOLDER=.venv
LAUNCH_IN_VENV=source ${VENV_FOLDER}/bin/activate &&
PYTHON_VERSION=python3.11
PYTHON=./.venv/bin/python

PHONY = help install install-dev test format lint type-check secure migrations migrate

# target: help - Display callable targets.
help:
	@echo "---------------HELP-----------------"
	@egrep "^# target:" [Mm]akefile
	@echo "------------------------------------"

# target: install - Install the project locally
install:
	${PYTHON} -m flit install --env --deps=production

# target: install-dev - Install the project for development locally
install-dev:
	${PYTHON} -m flit install -s --env --deps=develop --symlink

# target: Test commands

# target: test - Run tests
test:
	${PRE_RUN_API_COMMAND} test

# target: test-last-failed - Run last failed tests
test-last-failed:
	${PRE_RUN_API_COMMAND} test-last-failed

# target: test-current-v - Run tests with pytest mark current
test-current:
	${PRE_RUN_API_COMMAND} test-current

# target: test-current - Run tests with pytest mark current -verbose
test-current-v:
	${PRE_RUN_API_COMMAND} test-current-v

# target: test-domain - Run tests with in domain folder
test-domain:
	${PRE_RUN_API_COMMAND} test-domain

# target: test-int - Run tests with in integrations folder
test-int:
	${PRE_RUN_API_COMMAND} test-int

# target: test-repos - Run tests with in repositories folder
test-repos:
	${PRE_RUN_API_COMMAND} test-repos

# target: test-services - Run tests with in services folder
test-services:
	${PRE_RUN_API_COMMAND} test-services

# target: test-uows - Run tests with in uows folder
test-uows:
	${PRE_RUN_API_COMMAND} test-uows


# target: test-cov - Run tests with coverage
test-cov:
	${PRE_RUN_API_COMMAND} test-cov

# target: format - Format the code
format:
	${PYTHON} -m isort src tests --force-single-line-imports
	${PYTHON} -m autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place src --exclude=__init__.py
	${PYTHON} -m black src tests --config pyproject.toml
	${PYTHON} -m isort src tests

# target: lint - Run linter
lint:
	${PYTHON} -m flake8 --max-complexity 5 --max-cognitive-complexity=3 src
	${PYTHON} -m black src tests --check --diff --config pyproject.toml
	${PYTHON} -m isort src tests --check --diff

# target: type-check - Run type checker
type-check:
	${PYTHON} -m pytype --config=pytype.cfg src

# target: secure - Run all security related commands
secure:
	${PYTHON} -m bandit -r src --config pyproject.toml

# target: migrations - Create database migrations
migrations:
	${PRE_RUN_API_COMMAND} migrations

# target: migrate - Run database migrations
migrate:
	${PRE_RUN_API_COMMAND} migrate

# target: run - Run the server
server:
	${PRE_RUN_API_COMMAND} server

# target: bash - Open bash
bash:
	${PRE_RUN_API_COMMAND} bash

# target: setup - Setup the project locally
setup:
	rm -rf ${VENV_FOLDER}
	${PYTHON_VERSION} -m venv ${VENV_FOLDER}
	${LAUNCH_IN_VENV} pip install flit

# target: Docker targets

# target: build - Build the docker images
build:
	${DOCKER_COMPOSE} -f ${DOCKER_ENVIRONMENT} build

# target: run - Run the project
run:
	${DOCKER_COMPOSE} -f ${DOCKER_ENVIRONMENT} up -d

# taget: down - Stop the project
down:
	${DOCKER_COMPOSE} -f ${DOCKER_ENVIRONMENT} down

# target: clean-volumes - Stop the project and clean all volumes
clean-volumes:
	${DOCKER_COMPOSE} -f ${DOCKER_ENVIRONMENT} down -v

# target: logs - Show project logs
logs:
	${DOCKER_COMPOSE} -f ${DOCKER_ENVIRONMENT} logs -f


