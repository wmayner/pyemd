#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as _build_ext


# See http://stackoverflow.com/a/21621689/1085344
class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())


with open('README.rst') as f:
    readme = f.read()


__version__ = '0.0.5'
__author__ = 'Will Mayner'
__author_email__ = 'wmayner@gmail.com'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014 Will Mayner'


setup(
    name='pyemd',
    version=__version__,
    description=("A Python wrapper for Ofir Pele and Michael Werman's " +
                 "implementation of the Earth Mover's Distance."),
    long_description=readme,
    author=__author__,
    author_email=__author_email__,
    url="https://github.com/wmayner/pyemd",
    license=__license__,
    packages=['pyemd'],
    install_requires=[],
    cmdclass={'build_ext':build_ext},
    setup_requires=['numpy'],
    ext_modules=[Extension("pyemd/emd", ["pyemd/emd.cpp"],
                           language="c++")],
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3'
    ),
)
