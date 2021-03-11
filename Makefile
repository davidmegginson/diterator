
VENV=./venv/bin/activate

test: venv
	. $(VENV) && python -m unittest

run: venv
	. $(VENV) && python -m diterator.iterator

venv: requirements.txt
	rm -rf venv
	python3 -m venv venv
	. $(VENV) && pip install -r requirements.txt

