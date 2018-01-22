#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext as _build_ext


# Alias ModuleNotFound for Python <= 3.5
if (sys.version_info[0] < 3 or
        (sys.version_info[0] == 3 and sys.version_info[1] < 6)):
    ModuleNotFoundError = ImportError


try:
    from Cython.Build import cythonize
    USE_CYTHON = True
except (ImportError, ModuleNotFoundError):
    USE_CYTHON = False


def no_cythonize(extensions, **_ignore):
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


if USE_CYTHON:
    EXT_MODULES = cythonize(EXTENSIONS)
else:
    EXT_MODULES = no_cythonize(EXTENSIONS)


# See http://stackoverflow.com/a/21621689/1085344
class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        if hasattr(__builtins__, '__NUMPY_SETUP__'):
            __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())


cmdclass = {
    'build_ext': build_ext
}


with open('README.rst', 'r') as f:
    readme = f.read()

about = {}
with open('./pyemd/__about__.py') as f:
    exec(f.read(), about)

requires = ['numpy >=1.9.0, <2.0.0']

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    license=about['__license__'],
    packages=['pyemd'],
    install_requires=requires,
    cmdclass=cmdclass,
    setup_requires=requires,
    ext_modules=EXT_MODULES,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
    ],
)
