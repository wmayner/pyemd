=========
Changelog
=========

.. towncrier release notes start

1.1.0 (2026-01-28)
==================

Features
--------

- Added POT (Python Optimal Transport) as the default backend. All three functions (``emd()``, ``emd_with_flow()``, ``emd_samples()``) now accept a ``backend`` parameter with values ``'pot'`` (default, faster, multi-threaded) or ``'cpp'`` (original C++ implementation). Both backends produce equivalent results.


Bug Fixes
---------

- Fixed ``emd_samples`` returning incorrect results with ``bins='auto'`` on NumPy 2.1+ when using integer input arrays. NumPy 2.1 introduced a constraint that histogram bin widths must be at least 1 for integer dtypes, which caused too few bins to be created for small datasets (e.g., ``emd_samples([1], [2])`` incorrectly returned 0.0 instead of 0.5). (`#68 <https://github.com/wmayner/pyemd/issues/68>`_)
- Added ``ninja`` to build dependencies to fix build failures when ninja is not installed system-wide.


Documentation
-------------

- Updated README to document POT as the default backend, explain that PyEMD is now maintained as a wrapper around POT for backward compatibility, and recommend POT directly for new projects.


Miscellaneous
-------------

- Bumped minimum NumPy version from 1.9.0 to 1.15.0 (released 2018).
