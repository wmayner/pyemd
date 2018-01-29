.PHONY: default test build clean upload-dist test-dist sign-dist check-dist build-dist clean-dist

src = pyemd
dist_dir = dist

default: build

test: build
	py.test

build: clean
	python setup.py build_ext -b .

clean:
	rm -f pyemd/*.so

upload-dist: sign-dist
	twine upload $(dist_dir)/*

test-dist: check-dist
	twine upload --repository-url https://test.pypi.org/legacy/ $(dist_dir)/*

sign-dist: check-dist
	gpg --detach-sign -a dist/*.tar.gz
	gpg --detach-sign -a dist/*.whl

check-dist: build-dist
	python setup.py check --restructuredtext --strict

build-dist: clean-dist
	python setup.py sdist bdist_wheel --dist-dir=$(dist_dir)

clean-dist:
	rm -rf $(dist_dir)
