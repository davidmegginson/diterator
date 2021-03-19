
VENV=./venv/bin/activate

test: venv
	. $(VENV) && python setup.py test

run: venv
	. $(VENV) && python -m diterator

venv: requirements.txt
	rm -rf venv
	python3 -m venv venv
	. $(VENV) && pip install -r requirements.txt

