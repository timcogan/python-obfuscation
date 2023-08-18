.PHONY: check clean deploy init reset quality style test types help

PROJECT=python_obfuscation
TEST_DIR=tests
QUALITY_DIRS=$(PROJECT) $(TEST_DIR)
CLEAN_DIRS=$(PROJECT) $(TEST_DIR)
PYTHON=pdm run python

check:
	$(MAKE) style
	$(MAKE) quality
	$(MAKE) types
	$(MAKE) test

clean:
	find $(CLEAN_DIRS) -path '*/__pycache__/*' -delete
	find $(CLEAN_DIRS) -type d -name '__pycache__' -empty -delete
	find $(CLEAN_DIRS) -name '*.pyc' -type f -delete
	find $(CLEAN_DIRS) -name '*.cover' -type f -delete
	pdm venv remove -y $(PROJECT)

deploy:
	which pdm || pip install --user pdm
	pdm venv create -n $(PROJECT)-deploy
	pdm install --production --no-lock

init:
	which pdm || pip install --user pdm
	pdm venv create -n $(PROJECT)
	pdm install -d

reset:
	$(MAKE) clean
	$(MAKE) init
	$(MAKE) check

node_modules: 
ifeq (, $(shell which npm))
	$(error "No npm in $(PATH), please install it to run pyright type checking")
else
	npm install
endif

quality:
	$(PYTHON) -m black --check $(QUALITY_DIRS)
	$(PYTHON) -m autopep8 -a $(QUALITY_DIRS)

style:
	$(PYTHON) -m autoflake -r -i $(QUALITY_DIRS)
	$(PYTHON) -m isort $(QUALITY_DIRS)
	$(PYTHON) -m autopep8 -a $(QUALITY_DIRS)
	$(PYTHON) -m black $(QUALITY_DIRS)

test:
	$(PYTHON) -m pytest \
		-rs \
		--cov=./$(PROJECT) \
		--cov-report=term \
		./tests/ \
		-s

types: node_modules
	pdm run npx --no-install pyright tests $(PROJECT)

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'
