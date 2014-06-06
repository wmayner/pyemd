build:
	cython -v -t --cplus pyemd/emd.pyx
	python setup.py build_ext --inplace

clean:
	rm -rf pyemd/emd.so

test:
	make buildcython
	py.test
