
VENV=./venv/bin/activate

test: venv
	. $(VENV) && python setup.py test

run: venv
	. $(VENV) && python -m diterator

distro: venv
	. $(VENV) && rm -f dist/* && python setup.py sdist

publish: distro
	. $(VENV) && pip install twine && twine upload dist/*

venv: requirements.txt
	rm -rf venv
	python3 -m venv venv
	. $(VENV) && pip install -r requirements.txt

