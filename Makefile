
VENV=./venv/bin/activate

test: venv
	. $(VENV) && python setup.py test

run: venv
	. $(VENV) && python -m diterator

publish: venv
	. $(VENV) && pip install twine && rm -f dist/* && python setup.py sdist && twine upload dist/*

venv: requirements.txt
	rm -rf venv
	python3 -m venv venv
	. $(VENV) && pip install -r requirements.txt

