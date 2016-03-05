bin/python:
	virtualenv .

.PHONY: deps
deps: bin/python
	bin/pip install -r requirements.txt

.PHONY: run
run:
	bin/python polycules.py
