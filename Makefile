
VENV=./venv/bin/activate

test: venv
	. $(VENV) && python -m unittest

run: venv
	. $(VENV) && python get-somalia-activities.py

venv: requirements.txt
	rm -rf venv
	python3 -m venv venv
	. $(VENV) && pip install -r requirements.txt

