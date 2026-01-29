#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __init__.py

"""
PyEMD
=====

PyEMD computes the `Earth Mover's Distance
<https://en.wikipedia.org/wiki/Earth_mover%27s_distance>`_ between histograms
using NumPy arrays.

**If you use this code, please cite the papers listed at the end of the
README.**

Use PyEMD like so:

Usage
~~~~~

    >>> from pyemd import emd
    >>> import numpy as np
    >>> first_signature = np.array([0.0, 1.0])
    >>> second_signature = np.array([5.0, 3.0])
    >>> distance_matrix = np.array([[0.0, 0.5], [0.5, 0.0]])
    >>> emd(first_signature, second_signature, distance_matrix)
    3.5

You can also get the associated minimum-cost flow:

    >>> from pyemd import emd_with_flow
    >>> emd_with_flow(first_signature, second_signature, distance_matrix)
    (3.5, [[0.0, 0.0], [0.0, 1.0]])

You can also calculate the EMD directly from two arrays of observations:

    >>> from pyemd import emd_samples
    >>> first_array = [1,2,3,4]
    >>> second_array = [2,3,4,5]
    >>> emd_samples(first_array, second_array, bins=2)
    0.5


Backends
~~~~~~~~

PyEMD supports two computation backends:

- ``'pot'`` (default): Uses the `POT (Python Optimal Transport)
  <https://pythonot.github.io/>`_ library. This backend is faster for large
  problems and supports multi-threading.
- ``'cpp'``: Uses the original C++ implementation by Ofir Pele and Michael
  Werman.

You can select the backend using the ``backend`` parameter:

    >>> emd(first_signature, second_signature, distance_matrix, backend='cpp')
    3.5

Both backends produce equivalent results (within floating-point precision).


Limitations and Caveats
~~~~~~~~~~~~~~~~~~~~~~~

- ``distance_matrix`` must be symmetric.
- ``distance_matrix`` is assumed to represent a true metric. This must be
  enforced by the caller. See the documentation in ``pyemd/lib/emd_hat.hpp``.
- The flow matrix does not contain the flows to/from the extra mass bin.
- The signatures and distance matrix must be numpy arrays of ``np.float64``.


Credit
~~~~~~

- The POT backend uses the `POT library <https://pythonot.github.io/>`_ by
  Rémi Flamary et al.
- The C++ backend uses `Ofir Pele <https://ofirpele.droppages.com/>`_ and
  `Michael Werman's <https://www.cs.huji.ac.il/~werman/>`_ implementation.
  See the `relevant paper <https://doi.org/10.1109/ICCV.2009.5459199>`_.
- Thanks to the Cython developers for making the C++ wrapper relatively easy
  to write.


:copyright: Copyright (c) 2014-2018 Will Mayner.
:license: See the LICENSE file.
"""

from .emd import emd, emd_with_flow, emd_samples

try:
    from importlib.metadata import version
    __version__ = version("pyemd")
except Exception:
    __version__ = "unknown version"
