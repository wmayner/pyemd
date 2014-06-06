buildcython:
	cython -v -t --cplus pyemd/emd.pyx
	python setup.py build_ext --inplace

clean:
	rm -rf pyemd/emd.so

runtests:
	make buildcython
	py.test
