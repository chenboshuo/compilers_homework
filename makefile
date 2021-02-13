# .PHONY : clean help install venv coverage tests notebook
.INTERMEDIATE : clean help install venv coverage tests notebook
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
install : ./venv/touch_installed

./venv/touch_installed : requirements.txt venv
	$(BIN)pip install -r requirements.txt
	$(BIN)pip install -e .
	touch ./venv/touch_installed

## make venv : make the virtual environment,
## : : attention you are not enter virtual environments
venv: ./venv/bin/activate
./venv/bin/activate:
	python -m venv venv

## make notebook: open a jupyter notebook
notebook: ./venv/touch_ipython_installed
	$(BIN)jupyter notebook

./venv/touch_ipython_installed: ./venv/touch_installed
	$(BIN)python -m pip install ipykernel
	$(BIN)ipython kernel install --user --name=venv
	touch ./venv/touch_ipython_installed
## make clean: clean the temp files
clean:
	git clean -fXd

## make help : show this message.
help :
	@grep -h -E '^##' ${MAKEFILE_LIST} | sed -e 's/## //g' \
		| column -t -s ':'
