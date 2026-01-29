project('pyemd', 'cpp', 'cython',
    version: '0.0.0',  # Actual version set by setuptools_scm via meson-python
    default_options: ['warning_level=2', 'cpp_std=c++11']
)

py = import('python').find_installation(pure: false)
py_dep = py.dependency()
fs = import('fs')

# Get NumPy dependency and include directories
incdir_numpy = run_command(py,
    ['-c', 'import numpy; print(numpy.get_include())'],
    check: true
).stdout().strip()

inc_numpy = include_directories(incdir_numpy)
inc_pyemd = include_directories('src/pyemd')
inc_lib = include_directories('src/pyemd/lib')

# Cython extension module
py.extension_module(
    'emd',
    'src/pyemd/emd.pyx',
    include_directories: [inc_numpy, inc_pyemd, inc_lib],
    dependencies: [py_dep],
    install: true,
    subdir: 'pyemd',
    override_options: ['cython_language=cpp']
)

# Install pure Python files
py.install_sources(
    ['src/pyemd/__init__.py', 'src/pyemd/_pot_backend.py'],
    subdir: 'pyemd'
)

# Install C++ header library (for reference/distribution)
install_subdir('src/pyemd/lib', install_dir: py.get_install_dir() / 'pyemd')
