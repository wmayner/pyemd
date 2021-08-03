#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import os
import platform
import sys
from warnings import warn

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext as _build_ext
from setuptools.command.sdist import sdist as _sdist
from distutils.sysconfig import get_config_var
from distutils.version import LooseVersion


def is_platform_mac():
    return sys.platform == 'darwin'


# Alias ModuleNotFound for Python <= 3.5
if sys.version_info < (3, 6):
    ModuleNotFoundError = ImportError

# For macOS, ensure extensions are built for macOS 10.9 when compiling on a
# 10.9 system or above, overriding distutils behaviour which is to target
# the version that Python was built for. This may be overridden by setting
# MACOSX_DEPLOYMENT_TARGET before calling setup.py
if is_platform_mac():
    if 'MACOSX_DEPLOYMENT_TARGET' not in os.environ:
        current_system = LooseVersion(platform.mac_ver()[0])
        python_target = LooseVersion(
            get_config_var('MACOSX_DEPLOYMENT_TARGET'))
        if python_target < '10.9' and current_system >= '10.9':
            os.environ['MACOSX_DEPLOYMENT_TARGET'] = '10.9'

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
        # Ensure the compiled Cython files in the distribution are up-to-date
        if USE_CYTHON:
            _cythonize(EXTENSIONS)
        else:
            warn('\n\n\033[91m\033[1m  WARNING: '
                 'IF YOU A PREPARING A DISTRIBUTION: Cython is not available! '
                 'The cythonized `*.cpp` files may be out of date. Please '
                 'install Cython and run `sdist` again.'
                 '\033[0m\n')
        _sdist.run(self)


# See https://stackoverflow.com/a/21621689/1085344
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


with io.open('README.rst', encoding='utf-8') as f:
    README = f.read()

ABOUT = {}
with open('./pyemd/__about__.py') as f:
    exec(f.read(), ABOUT)


NUMPY_REQUIREMENT = ['numpy >=1.9.0, <2.0.0']

# Copied from scipy's installer, to solve the same issues they saw:

# Figure out whether to add ``*_requires = ['numpy']``.
# We don't want to do that unconditionally, because we risk updating
# an installed numpy which fails too often.  Just if it's not installed, we
# may give it a try.  See scipy gh-3379.
try:
    import numpy
except ImportError:  # We do not have numpy installed
    REQUIRES = NUMPY_REQUIREMENT
else:
    # If we're building a wheel, assume there already exist numpy wheels
    # for this platform, so it is safe to add numpy to build requirements.
    # See scipy gh-5184.
    REQUIRES = (NUMPY_REQUIREMENT if 'bdist_wheel' in sys.argv[1:] else [])

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
