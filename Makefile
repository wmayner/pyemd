default:
	python setup.py build_ext -b .

build:
	cython -v -t --cplus pyemd/emd.pyx

clean:
	rm -rf build
	rm -rf pyemd/emd.so

test: default
	py.test
