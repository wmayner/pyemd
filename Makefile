.PHONY: default test build clean upload-dist test-dist sign-dist check-dist build-dist clean-dist

src = pyemd
dist_dir = dist

default: build

test: build
	py.test

build: clean
	python -m pip install -e .
	# setup.py build_ext -b .

clean:
	rm -f pyemd/*.so
	rm -rf **/__pycache__
	rm -rf build
	rm -rf pyemd.egg-info

upload-dist: sign-dist
	twine upload $(dist_dir)/*

test-dist: check-dist
	twine upload --repository testpypi $(dist_dir)/*

sign-dist: check-dist
	gpg --detach-sign -a dist/*.tar.gz
	gpg --detach-sign -a dist/*.whl

check-dist: build-dist
	twine check --strict dist/*

build-dist: clean-dist
	python -m build
	# python -m setup.py sdist bdist_wheel --dist-dir=$(dist_dir)

clean-dist:
	rm -r $(dist_dir)
