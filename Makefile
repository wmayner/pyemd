.PHONY: default clean develop test dist-clean build-local build dist-upload dist-test-upload dist-sign dist-check

src = src/pyemd
test = test
dist = dist
wheelhouse = wheelhouse
readme = README.rst

default: test

clean:
	rm -rf $(shell find . -name '__pycache__')
	rm -rf $(shell find . -name '*.so')
	rm -rf .eggs
	rm -rf pyemd.egg-info
	rm -rf build

develop: clean
	python -m pip install -e ".[test,dist]"

test: develop
	py.test

dist-build-local:
	python -m build

dist-build-wheels:
	cibuildwheel --platform linux --config-file pyproject.toml

dist-clean:
	rm -rf $(dist)

dist-upload: dist-sign
	twine upload $(dist)/*

dist-test-upload: dist-check
	twine upload --repository testpypi $(dist)/*

dist-sign: dist-check
	gpg --detach-sign -a $(dist)/*.tar.gz
	gpg --detach-sign -a $(dist)/*.whl

dist-check: dist-build
	twine check --strict $(dist)/*

dist-test-install:
	pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pyemd
