SHELL := /bin/bash
PY = python3
# Makefile for managing a Python project with Poetry

# Variables
POETRY := poetry
PYTHON := $(POETRY) run python
SERVICE_NAME := $(shell git remote get-url origin | sed 's/.*\/\([^\/]*\)\.git/\1/')
RANDOM_NUM := $(shell echo $$((RANDOM)))
# Default target
.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo " setup        	    Install dependencies using Poetry"
	@echo " run                Run the application"
	@echo " docker-run         Run the application using Docker detached"
	@echo " docker-run-log     Run the application using Docker with Logs"
	@echo " compose-run        Run the application with Compose"
	@echo " compose-run-logs   Run the application with Compose and show logs"
	@echo " update       	    Update dependencies using Poetry"
	@echo " lock         	    Generate Poetry lock file"
	@echo " test         	    Run tests"
	@echo " test-coverage      Run tests to get coverage"
	@echo " lint         	    Lint the code using flake8"
	@echo " format       	    Format the code using black"
	@echo " clean        	    Clean the project"

.PHONY: docker-run
docker-run:
	docker rm -f $(SERVICE_NAME) 2>/dev/null || true
	docker build --pull --rm -f infra/snatcher/Dockerfile -t ${SERVICE_NAME}:latest .
	docker run -d --name $(SERVICE_NAME)_$(RANDOM_NUM) -p 8000:8000 $(SERVICE_NAME):latest

.PHONY: docker-run-logs
docker-run-log:
	docker rm -f $(SERVICE_NAME) 2>/dev/null || true
	docker build --pull --rm -f infra/snatcher/Dockerfile -t ${SERVICE_NAME}:latest .
	docker run --name $(SERVICE_NAME)_$(RANDOM_NUM) -p 8000:8000 $(SERVICE_NAME):latest


.PHONY: compose-run-logs
compose-run-logs:
	docker-compose -f infra/docker-compose.yml --env-file .env up --build

.PHONY: compose-run
compose-run:
	docker-compose -d -f infra/docker-compose.yml --env-file .env up --build

.PHONY: run
run:
	$(PYTHON) src/snatcher/main.py

.PHONY: setup
setup:
	$(PY) -m venv .venv && source .venv/bin/activate && $(PY) -m pip install --upgrade pip && $(PY) -m pip install poetry && $(PY) -m poetry config virtualenvs.create true && $(PY) -m poetry config virtualenvs.in-project true && $(PY) -m poetry config virtualenvs.path .venv && $(PY) -m poetry install && pre-commit install -f && pre-commit install --hook-type commit-msg -f
	@echo "To activate the virtual environment in your terminal, run: source .venv/bin/activate |OR| run: poetry shell"

# Update dependencies
.PHONY: update
update:
	$(POETRY) update

# Generate lock file
.PHONY: lock
lock:
	$(POETRY) lock

# Run tests
.PHONY: test
test:
	$(PYTHON) -m pytest

.PHONY: test-coverage
test-coverage:
	$(PYTHON) -m pytest --cov=src --cov-report=term tests/


# Lint the code
.PHONY: lint
lint:
	$(PYTHON) -m flake8 .

# Format the code
.PHONY: format
format:
	$(PYTHON) -m black .

# Clean the project
.PHONY: clean
clean:
	@rm -rf .pytest_cache
	@rm -rf __pycache__
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@find . -name "*.pyc" -delete
	@find . -name "*.pyo" -delete
	@find . -name "*~" -delete