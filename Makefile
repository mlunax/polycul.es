bin/python:
	virtualenv .

.PHONY: deps
deps: bin/python
	bin/pip install -r requirements.txt

.PHONY: run
run:
	python polycules.py

.PHONY: test
test:
	flake8 --config=.flake8
	nosetests --with-coverage --cover-erase --verbosity=2 --cover-package=polycules,model
