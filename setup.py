#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.extension import Extension
import numpy as np

with open('README.rst') as f:
    readme = f.read()

setup(
    name='pyemd',
    version='0.0.4',
    description=("A Python wrapper for Ofir Pele and Michael Werman's " +
                 "implementation of the Earth Mover's Distance."),
    long_description=readme,
    author='Will Mayner',
    author_email='wmayner@gmail.com',
    url="https://github.com/wmayner/pyemd",
    license= 'MIT',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3'
    ),
    packages=['pyemd'],
    ext_modules=[Extension("pyemd/emd", ["pyemd/emd.cpp"],
                           language="c++",
                           include_dirs=[np.get_include()])]
)
