#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import platform
import sys
from distutils.sysconfig import get_config_var

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext as _build_ext

from packaging.version import Version, parse as parse_version


def is_platform_mac():
    return sys.platform == "darwin"


# For macOS, ensure extensions are built for macOS 10.9 when compiling on a
# 10.9 system or above, overriding distutils behaviour which is to target
# the version that Python was built for. This may be overridden by setting
# MACOSX_DEPLOYMENT_TARGET before calling setup.py
if is_platform_mac() and "MACOSX_DEPLOYMENT_TARGET" not in os.environ:
    current_system = parse_version(platform.mac_ver()[0])
    python_target = parse_version(get_config_var("MACOSX_DEPLOYMENT_TARGET"))
    mac_deployment_target = Version("10.9")
    if (
        python_target < mac_deployment_target
        and current_system >= mac_deployment_target
    ):
        os.environ["MACOSX_DEPLOYMENT_TARGET"] = str(mac_deployment_target)

try:
    from Cython.Build import cythonize as _cythonize

    USE_CYTHON = True
except (ImportError, ModuleNotFoundError):
    USE_CYTHON = False


def cythonize(extensions, **kwargs):
    # Attempt to use Cython
    if USE_CYTHON:
        return _cythonize(extensions, **kwargs)
    # Cython is not available
    for extension in extensions:
        sources = []
        for sfile in extension.sources:
            path, ext = os.path.splitext(sfile)
            if ext in (".pyx", ".py"):
                if extension.language == "c++":
                    ext = ".cpp"
                else:
                    ext = ".c"
                sfile = path + ext
            sources.append(sfile)
        extension.sources[:] = sources
    return extensions


EXTENSIONS = [
    Extension(
        "pyemd.emd",
        sources=["src/pyemd/emd.pyx"],
        language="c++",
    )
]

EXT_MODULES = cythonize(EXTENSIONS, language_level=3)


# See https://stackoverflow.com/a/21621689/1085344
class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        if hasattr(__builtins__, "__NUMPY_SETUP__"):
            __builtins__.__NUMPY_SETUP__ = False
        import numpy

        self.include_dirs.append(numpy.get_include())


CMDCLASS = {"build_ext": build_ext}


SETUP_REQUIRES = ["setuptools_scm", "packaging"]

setup(
    name="pyemd",
    packages=["pyemd", "pyemd.lib"],
    package_dir={
        "pyemd": "src/pyemd",
        "pyemd.lib": "src/pyemd/lib",
    },
    include_package_data=True,
    ext_modules=EXT_MODULES,
    cmdclass=CMDCLASS,
    setup_requires=SETUP_REQUIRES,
    use_scm_version=True,
)
