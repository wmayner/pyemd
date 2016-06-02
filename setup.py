#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from distutils.command.sdist import sdist as _sdist
from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext as _build_ext

try:
    from Cython.Build import cythonize
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False


EXTENSIONS = [
    Extension('pyemd.emd',
              sources=['pyemd/emd.pyx'],
              language="c++")
]


class sdist(_sdist):
    def run(self):
        # Make sure the compiled Cython files in the distribution are
        # up-to-date
        from Cython.Build import cythonize
        cythonize(EXTENSIONS)
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


cmdclass = {
    'sdist': sdist,
    'build_ext': build_ext
}


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


if USE_CYTHON:
    ext_modules = cythonize(EXTENSIONS)
else:
    ext_modules = no_cythonize(EXTENSIONS)


with open('README.rst', 'r') as f:
    readme = f.read()

requires = ['numpy >=1.8.0, <2.0.0']

setup(
    name='pyemd',
    version='0.3.0',
    description=("A Python wrapper for Ofir Pele and Michael Werman's " +
                 "implementation of the Earth Mover's Distance."),
    long_description=readme,
    author='Will Mayner',
    author_email='wmayner@gmail.com',
    url="https://github.com/wmayner/pyemd",
    license='MIT',
    packages=['pyemd'],
    package_data={'pyemd': ['emd.pyx', 'lib/*.hpp', '../README.rst']},
    install_requires=requires,
    cmdclass=cmdclass,
    setup_requires=requires,
    ext_modules=ext_modules,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
)
