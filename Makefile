bin/python:
	virtualenv .

.PHONY: deps
deps: bin/python
	bin/pip install -r requirements.txt

.PHONY: run
run:
	bin/python polycules.py

.PHONY: test
test:
	bin/flake8 --config=.flake8
	bin/nosetests --with-coverage --cover-erase --verbosity=2 --cover-package=polycules,model,migrations.hashify
