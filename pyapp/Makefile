.PHONY: clean data jupyter lint requirements venv

#################################################################################
# GLOBALS                                                                       #
#################################################################################
PROJECT_NAME = lem_sim
PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
VENV_DIR =  $(PROJECT_DIR)/env

PYTHON_INTERPRETER = $(VENV_DIR)/bin/python3
PIP = $(VENV_DIR)/bin/pip

#################################################################################
# STANDARD COMMANDS                                                             #
#################################################################################

## Install Python Dependencies
requirements: venv
	$(PIP) install -U pip setuptools wheel
	$(PIP) install -r requirements.txt

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8
lint:
	@$(PYTHON_INTERPRETER) -m flake8 --config=$(PROJECT_DIR)/.flake8 src

## Install virtual environment
venv:
ifeq ($(wildcard $(VENV_DIR)/*),)
	@echo "Did not find $(VENV_DIR), creating..."
	mkdir -p $(VENV_DIR)
	python3 -m venv $(VENV_DIR)
endif

#################################################################################
# CUSTOM COMMANDS                                                               #
#################################################################################

simulate:
	@$(PYTHON_INTERPRETER) src/$(PROJECT_NAME)/simulate.py --connection=port

test:
	@$(PYTHON_INTERPRETER) src/$(PROJECT_NAME)/linear_optimization/decompose.py --connection=port