.PHONY: default clean develop test build-wheel dist-clean build-local build dist-upload dist-test-upload dist-sign dist-check legacy-develop

src = src/pyemd
test = test
dist = dist
wheelhouse = wheelhouse

default: test

test: develop
	.venv/bin/pytest

develop: build-wheel
	uv sync --all-extras
	uv pip install --force-reinstall --no-deps dist/pyemd-*.whl

build-wheel: clean
	uv build --wheel

clean:
	rm -rf $(shell find $(src) $(test) -name '__pycache__' 2>/dev/null)
	rm -rf $(shell find $(src) -name '*.so' 2>/dev/null)
	rm -rf .eggs
	rm -rf pyemd.egg-info
	rm -rf build
	rm -rf dist
	rm -rf .mesonpy-*

dist-build-local:
	uv build

dist-build-wheels:
	uv run cibuildwheel --platform linux --config-file pyproject.toml

dist-upload: dist-sign
	uv run twine upload $(dist)/*
	uv run twine upload $(wheelhouse)/*

dist-test-upload: dist-check
	uv run twine upload --repository-url https://test.pypi.org/simple/ $(dist)/*
	uv run twine upload --repository-url https://test.pypi.org/simple/ $(wheelhouse)/*

dist-sign: dist-check
	gpg --detach-sign -a $(dist)/*.tar.gz
	gpg --detach-sign -a $(wheelhouse)/*.whl

dist-check:
	uv run twine check --strict $(wheelhouse)/*.whl

dist-clean:
	rm -rf $(dist)

dist-test-install:
	uv pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pyemd

# Legacy targets (deprecated, for backward compatibility)
legacy-develop:
	python -m pip install -e ".[test,dist]"
