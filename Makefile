.PHONY: default clean develop test dist-clean build-local build dist-upload dist-test-upload dist-sign dist-check

src = src/pyemd
test = test
dist = wheelhouse
readme = README.rst

default: develop

clean:
	rm -rf $(shell find . -name '__pycache__')
	rm -rf $(shell find . -name '*.so')
	rm -rf .eggs
	rm -rf pyemd.egg-info
	rm -rf dist
	rm -rf build

develop: clean
	python -m pip install -e ".[test,dist]"

test: develop
	py.test

build-local: clean
	python -m build

dist-clean:
	rm -rf $(dist)

build: dist-clean
	cibuildwheel --platform linux --config-file pyproject.toml --output-dir $(dist)

dist-upload: dist-sign
	twine upload $(dist)/*

dist-test-upload: dist-check
	twine upload --repository testpypi $(dist)/*

dist-sign: dist-check
	gpg --detach-sign -a $(dist)/*.tar.gz
	gpg --detach-sign -a $(dist)/*.whl

dist-check: dist-build
	twine check --strict $(dist)/*
