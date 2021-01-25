.PHONY : clean help install venv coverage
SHELL := /bin/zsh
BIN=venv/bin/

## make tests : run all test cases
tests: install coverage
	$(BIN)coverage run --omit 'venv/*' -m pytest
	coverage html

coverage: ./venv/bin/coverage

./venv/bin/coverage:
	$(BIN)pip install coverage

## make install: create virtual environment and install requirment
install : ./venv/installed

./venv/installed : requirements.txt
	$(BIN)pip install -r requirements.txt
	$(BIN)pip install -e .
	touch ./venv/installed

## make venv : make the virtual environment,
## : : attention you are not enter virtual environments
venv: ./venv/bin/activate
	python -m venv venv

## make clean: clean the temp files
clean:
	git clean -fXd

## make help : show this message.
help :
	@grep -h -E '^##' ${MAKEFILE_LIST} | sed -e 's/## //g' \
		| column -t -s ':'
