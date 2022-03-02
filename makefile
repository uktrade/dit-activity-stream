SHELL := /bin/bash

# Colour coding for output
COLOUR_NONE=\033[0m
COLOUR_GREEN=\033[32;01m
COLOUR_YELLOW=\033[33;01m
COLOUR_RED='\033[0;31m'

# Help output
.PHONY: help test
help:
	@echo -e "$(COLOUR_YELLOW)make cleanup-code$(COLOUR_NONE) : Run flake8, black, isort, mypy"
	@echo -e "$(COLOUR_YELLOW)make tests$(COLOUR_NONE) : Run tests"
	@echo -e "$(COLOUR_YELLOW)make build-test$(COLOUR_NONE) : Build the package and push to https://github.com/uktrade/dit-activity-stream/"
	@echo -e "$(COLOUR_YELLOW)make build$(COLOUR_NONE) : Build the package and push to https://github.com/uktrade/dit-activity-stream/"

cleanup-code:
	flake8 .
	black .
	isort .
	mypy .

tests:
	tox

build:
	pip install --upgrade build twine
	python -m build

push-pypi-test:
	twine upload --repository testpypi dist/*

push-pypi:
	twine upload dist/*
