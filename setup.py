#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from warnings import warn

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext as _build_ext
from setuptools.command.sdist import sdist as _sdist


# Alias ModuleNotFound for Python <= 3.5
if (sys.version_info[0] < 3 or
        (sys.version_info[0] == 3 and sys.version_info[1] < 6)):
    ModuleNotFoundError = ImportError


try:
    from Cython.Build import cythonize as _cythonize
    USE_CYTHON = True
except (ImportError, ModuleNotFoundError):
    USE_CYTHON = False


def cythonize(extensions, **_ignore):
    # Attempt to use Cython
    if USE_CYTHON:
        return _cythonize(extensions)
    # Cython is not available
    for extension in extensions:
        sources = []
        for sfile in extension.sources:
            path, ext = os.path.splitext(sfile)
            if ext in ('.pyx', '.py'):
                if extension.language == 'c++':
                    ext = '.cpp'
                else:
                    ext = '.c'
                sfile = path + ext
            sources.append(sfile)
        extension.sources[:] = sources
    return extensions


EXTENSIONS = [
    Extension('pyemd.emd',
              sources=['pyemd/emd.pyx'],
              language="c++")
]

EXT_MODULES = cythonize(EXTENSIONS)


class sdist(_sdist):
    def run(self):
        # Make sure the compiled Cython files in the distribution are up-to-date
        if USE_CYTHON:
            _cythonize(EXTENSIONS)
        else:
            warn('\n\n\033[91m\033[1m  WARNING: '
                 'IF YOU A PREPARING A DISTRIBUTION: Cython is not available! '
                 'The cythonized `*.cpp` files may be out of date. Please '
                 'install Cython and run `sdist` again.'
                 '\033[0m\n')
        _sdist.run(self)


# See http://stackoverflow.com/a/21621689/1085344
class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        if hasattr(__builtins__, '__NUMPY_SETUP__'):
            __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())


CMDCLASS = {
    'sdist': sdist,
    'build_ext': build_ext
}


with open('README.rst', 'r') as f:
    README = f.read()

ABOUT = {}
with open('./pyemd/__about__.py') as f:
    exec(f.read(), ABOUT)


REQUIRES = [
    'numpy >=1.9.0, <2.0.0'
]

setup(
    name=ABOUT['__title__'],
    version=ABOUT['__version__'],
    description=ABOUT['__description__'],
    long_description=README,
    author=ABOUT['__author__'],
    author_email=ABOUT['__author_email__'],
    url=ABOUT['__url__'],
    license=ABOUT['__license__'],
    packages=['pyemd'],
    install_requires=REQUIRES,
    cmdclass=CMDCLASS,
    setup_requires=REQUIRES,
    ext_modules=EXT_MODULES,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
