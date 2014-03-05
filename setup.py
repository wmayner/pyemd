#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy as np

import pyemd

extensions = [Extension("pyemd/*", ["pyemd/*.pyx"],
                        language="c++",
                        include_dirs=[np.get_include()])]

with open('README.rst') as f:
    readme = f.read()

setup(
    name=pyemd.__title__,
    version=pyemd.__version__,
    description=("A Python wrapper for Ofir Pele and Michael Werman's " +
                 "implementation of the Earth Mover's Distance."),
    long_description=readme,
    author=pyemd.__author__,
    author_email=pyemd.__author_email__,
    url="https://github.com/wmayner/pyemd",
    license=pyemd.__license__,
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
    ext_modules=cythonize(extensions)
)
