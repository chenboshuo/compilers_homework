.PHONY : clean help install venv
SHELL := /bin/zsh

## make install: create virtual environment and install requirment
install : ./venv/installed

./venv/installed : requirements.txt venv
	pip install -r requirements.txt
	pip install -e .
	touch ./venv/installed

## make venv : make the virtual environment
venv: ./venv/bin/activate
	source ./venv/bin/activate
	# bash -c "venv/bin/activate"


./venv/bin/activate :
	python -m venv venv

exit:
	deactivate

clean:
	git clean -fXd

## make help : show this message.
help :
	@grep -h -E '^##' ${MAKEFILE_LIST} | sed -e 's/## //g' \
		| column -t -s ':'
