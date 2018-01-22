.PHONY: default test build clean dist test-dist check-dist build-dist clean-dist

src = pyemd
dist_dir = dist

default: build

test: build
	py.test

build: clean
	python setup.py build_ext -b .

clean:
	rm -f pyemd/*.so

dist: build-dist check-dist
	twine upload $(dist_dir)/*

test-dist: build-dist check-dist
	twine upload --repository-url https://test.pypi.org/legacy/ $(dist_dir)/*

check-dist:
	python setup.py check --restructuredtext --strict

build-dist: clean-dist
	python setup.py sdist bdist_wheel --dist-dir=$(dist_dir)

clean-dist:
	rm -r $(dist_dir)
