.PHONY: setup freeze install test

# source : https://stackoverflow.com/questions/10858261/abort-makefile-if-variable-not-set
check_defined = \
    $(strip $(foreach 1,$1, \
        $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
      $(error Undefined $1$(if $2, ($2))))

setup:
	python3 -m venv venv

freeze:
	$(call check_defined, VIRTUAL_ENV, please use a virtual environment)
	python -m pip freeze > requirements.txt

install:
	$(call check_defined, VIRTUAL_ENV, please use a virtual environment)
	python -m pip install -r requirements.txt

test.before:
	docker-compose up -d

test.after:
	docker-compose down

test.run:
	$(call check_defined, VIRTUAL_ENV, please use a virtual environment)
	python -m pytest -vv

test: test.before test.run test.after
