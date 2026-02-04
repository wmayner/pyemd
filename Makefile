.PHONY: default clean develop test build dist-clean dist-build dist-upload dist-test-upload dist-sign dist-check

src = src/pyemd
test = test
dist = dist

default: test

test: develop
	uv run pytest

develop:
	uv sync --all-extras
	uv pip install -e .

build:
	uv build --wheel

clean:
	rm -rf $(shell find $(src) $(test) -name '__pycache__' 2>/dev/null)
	rm -rf .eggs
	rm -rf pyemd.egg-info
	rm -rf build
	rm -rf dist
	rm -rf src/pyemd.egg-info

dist-build:
	uv build

dist-upload: dist-sign
	uv run twine upload $(dist)/*

dist-test-upload: dist-check
	uv run twine upload --repository-url https://test.pypi.org/simple/ $(dist)/*

dist-sign: dist-check
	gpg --detach-sign -a $(dist)/*.tar.gz
	gpg --detach-sign -a $(dist)/*.whl

dist-check:
	uv run twine check --strict $(dist)/*.whl

dist-clean:
	rm -rf $(dist)

dist-test-install:
	uv pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pyemd
