*********************************************
PyEMD: Fast Earth Mover's Distance for Python
*********************************************

PyEMD is a Python wrapper for `Ofir Pele and Michael Werman's implementation of
the Earth Mover's Distance
<http://www.seas.upenn.edu/~ofirpele/FastEMD/code/>`_ that integrates it with
NumPy.

It does not expose the full functionality of that library; it can only be with
the ``np.float`` data type, and with a symmetric distance matrix that
represents a true metric. See the documentation for the Pele and Werman library
for the other options it provides.


Usage
=====

Use PyEMD like so:

.. code-block:: python

    >>> from pyemd import emd
    >>> import numpy as np
    >>> first_signature = np.array([0.0, 1.0])
    >>> second_signature = np.array([5.0, 3.0])
    >>> distance_matrix = np.ones([[0.0, 0.5], [0.5, 0.0])
    >>> emd(first_signature, second_signature, distance_matrix)
    3.5


Limitations and Caveats:
========================

- ``distance_matrix`` must be symmetric.
- ``distance_matrix`` must represent a true metric. This must be enforced by
  the caller. See the documentation in ``emd_hat.hpp``.
- The signatures and distance matrix must be numpy arrays of ``np.float``. The
  original C++ template function can accept any numerical C++ type, but this
  wrapper only instantiates the template with ``double`` (Cython converts
  ``np.float`` to ``double``).
- The original C++ functions have optional parameters ``extra_mass_penalty``
  and ``F`` (for flows); this wrapper does not expose those parameters. See
  inline documentation in emd_hat.hpp.


Credits
=======

- All credit for the actual algorithm and implementation goes to Ofir Pele and
  Michael Werman. See the `relevant paper
  <http://www.seas.upenn.edu/~ofirpele/publications/ICCV2009.pdf>`.
- Thanks to the Cython devlopers for making this kind of wrapper relatively
  easy to write.
