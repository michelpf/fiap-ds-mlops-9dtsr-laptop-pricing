#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = fiap-ds-mlops-9dtsr-laptop-pricing
PYTHON_VERSION = 3.10
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Install Python dependencies
.PHONY: requirements
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt
	



## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete


## Lint using flake8, black, and isort (use `make format` to do formatting)
.PHONY: lint
lint:
	flake8 fiap_ds_mlops_9dtsr_laptop_pricing
	isort --check --diff fiap_ds_mlops_9dtsr_laptop_pricing
	black --check fiap_ds_mlops_9dtsr_laptop_pricing

## Format source code with black
.PHONY: format
format:
	isort fiap_ds_mlops_9dtsr_laptop_pricing
	black fiap_ds_mlops_9dtsr_laptop_pricing



## Run tests
.PHONY: test
test:
	python -m pytest tests




#################################################################################
# PROJECT RULES                                                                 #
#################################################################################


## Make dataset
.PHONY: data
data: requirements
	$(PYTHON_INTERPRETER) fiap_ds_mlops_9dtsr_laptop_pricing/dataset.py


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
