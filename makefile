SHELL := /bin/bash

# Colour coding for output
COLOUR_NONE=\033[0m
COLOUR_GREEN=\033[32;01m
COLOUR_YELLOW=\033[33;01m
COLOUR_RED='\033[0;31m'

# Help output
.PHONY: help test
help:
	@echo -e "$(COLOUR_YELLOW)make setup$(COLOUR_NONE) : Initalise the poetry environment"
	@echo -e "$(COLOUR_YELLOW)make cleanup-code$(COLOUR_NONE) : Run flake8, black, isort, mypy"
	@echo -e "$(COLOUR_YELLOW)make tox$(COLOUR_NONE) : Run tests with tox"
	@echo -e "$(COLOUR_YELLOW)make build-package$(COLOUR_NONE) : Build the package"
	@echo -e "$(COLOUR_YELLOW)make push-pypi-test$(COLOUR_NONE) : Push the build package to https://test.pypi.org/project/django-hawk/"
	@echo -e "$(COLOUR_YELLOW)make push-pypi$(COLOUR_NONE) : Push the built package to https://pypi.org/project/django-hawk/"

setup:
	poetry install --with testing,utils

cleanup-code:
	poetry run black .
	poetry run isort .
	poetry run mypy .
	poetry run flake8 .

tox:
	poetry run tox

build-package:
	poetry build

push-pypi-test:
	poetry publish -r test-pypi

push-pypi:
	poetry publish
