.PHONY: default clean develop test dist-clean build-local build dist-upload dist-test-upload dist-sign dist-check

src = src/pyemd
test = test
dist = dist
wheelhouse = wheelhouse

default: test

test: develop
	py.test

develop: clean
	python -m pip install -e ".[test,dist]"

clean:
	rm -rf $(shell find . -name '__pycache__')
	rm -rf $(shell find . -name '*.so')
	rm -rf .eggs
	rm -rf pyemd.egg-info
	rm -rf build

dist-build-local:
	python -m build

dist-build-wheels:
	cibuildwheel --platform linux --config-file pyproject.toml

dist-upload: dist-sign
	twine upload $(dist)/*
	twine upload $(wheelhouse)/*

dist-test-upload: dist-check
	twine upload --repository-url https://test.pypi.org/simple/ testpypi $(dist)/*
	twine upload --repository-url https://test.pypi.org/simple/ testpypi $(wheelhouse)/*

dist-sign: dist-check
	gpg --detach-sign -a $(dist)/*.tar.gz
	gpg --detach-sign -a $(wheelhouse)/*.whl

dist-check:
	twine check --strict $(dist)/*
	twine check --strict $(wheelhouse)/*

dist-clean:
	rm -rf $(dist)

dist-test-install:
	pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pyemd
