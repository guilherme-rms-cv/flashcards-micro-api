PYTHON ?= python3
VENV ?= .venv

ifeq ($(OS),Windows_NT)
VENV_BIN := $(VENV)/Scripts
else
VENV_BIN := $(VENV)/bin
endif

PIP := $(VENV_BIN)/pip
PYTHON_VENV := $(VENV_BIN)/python

.PHONY: install run test

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(PYTHON_VENV) -m uvicorn app.main:app --reload

test:
	$(PYTHON_VENV) -m pytest -q
