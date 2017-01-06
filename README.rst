.. image:: https://travis-ci.org/wmayner/pyemd.svg?branch=develop
    :target: https://travis-ci.org/wmayner/pyemd
.. image:: http://img.shields.io/badge/Python%203%20-compatible-brightgreen.svg
    :target: https://wiki.python.org/moin/Python2orPython3
    :alt: Python 3 compatible

**************************
PyEMD: Fast EMD for Python
**************************

PyEMD is a Python wrapper for `Ofir Pele and Michael Werman's implementation
<http://www.ariel.ac.il/sites/ofirpele/fastemd/code/>`_ of the `Earth Mover's
Distance <http://en.wikipedia.org/wiki/Earth_mover%27s_distance>`_ that allows
it to be used with NumPy. **If you use this code, please cite the papers listed
at the end of this document.**

This wrapper does not expose the full functionality of the underlying
implementation; it can only used be with the ``np.float`` data type, and with a
symmetric distance matrix that represents a true metric. See the documentation
for the original Pele and Werman library for the other options it provides.

Installation
~~~~~~~~~~~~

To install the latest release:

.. code:: bash

    pip install pyemd

To install the latest development version:

.. code:: bash

    pip install "git+https://github.com/wmayner/pyemd@develop#egg=pyemd"

Usage
~~~~~

.. code:: python

    >>> from pyemd import emd
    >>> import numpy as np
    >>> first_signature = np.array([0.0, 1.0])
    >>> second_signature = np.array([5.0, 3.0])
    >>> distance_matrix = np.array([[0.0, 0.5], [0.5, 0.0]])
    >>> emd(first_signature, second_signature, distance_matrix)
    3.5

You can also get the associated minimum-cost flow:

.. code:: python

    >>> from pyemd import emd_with_flow
    >>> emd_with_flow(first_signature, second_signature, distance_matrix)
    (3.5, [[0.0, 0.0], [0.0, 1.0]])

API
~~~

.. code:: python

    emd(first_signature, second_signature, distance_matrix)

- ``first_signature``: A 1-dimensional numpy array of ``np.float``, of size N.
- ``second_signature``: A 1-dimensional numpy array of ``np.float``, of size N.
- ``distance_matrix``: A 2-dimensional array of ``np.float``, of size NxN. Must
  be symmetric and represent a metric.


.. code:: python

    emd, flow = emd_with_flow(first_signature, second_signature, distance_matrix)

- ``first_signature``: A 1-dimensional numpy array of ``np.float``, of size N.
- ``second_signature``: A 1-dimensional numpy array of ``np.float``, of size N.
- ``distance_matrix``: A 2-dimensional array of ``np.float``, of size NxN. Must
  be symmetric and represent a metric.


Limitations and Caveats
~~~~~~~~~~~~~~~~~~~~~~~

- ``distance_matrix`` must be symmetric.
- ``distance_matrix`` is assumed to represent a true metric. This must be
  enforced by the user. See the documentation in ``pyemd/lib/emd_hat.hpp``.
- The flow matrix does not contain the flows to/from the extra mass bin.
- The signatures and distance matrix must be numpy arrays of ``np.float``. The
  original C++ template function can accept any numerical C++ type, but this
  wrapper only instantiates the template with ``double`` (Cython converts
  ``np.float`` to ``double``). If there's demand, I can add support for other
  types.

Contributing
~~~~~~~~~~~~

To help develop PyEMD, fork the project on GitHub and install the requirements with ``pip``.

The ``Makefile`` defines some tasks to help with development:

* ``default``: compile the Cython code into C++ and build the C++ into a Python
  extension, using the ``setup.py`` build command
* ``build``: same as default, but using the ``cython`` command
* ``clean``: remove the build directory and the compiled C++ extension
* ``test``: run unit tests with ``py.test``


Credit
~~~~~~

- All credit for the actual algorithm and implementation goes to `Ofir Pele
  <http://www.ariel.ac.il/sites/ofirpele/>`_ and `Michael Werman
  <http://www.cs.huji.ac.il/~werman/>`_. See the `relevant paper
  <http://www.seas.upenn.edu/~ofirpele/publications/ICCV2009.pdf>`_.
- Thanks to the Cython devlopers for making this kind of wrapper relatively
  easy to write.

Please cite these papers if you use this code:
``````````````````````````````````````````````

Ofir Pele and Michael Werman, "A linear time histogram metric for improved SIFT matching," in *Computer Vision - ECCV 2008*, Marseille, France, 2008, pp. 495-508.

.. code-block:: latex

    @INPROCEEDINGS{pele2008,
      title={A linear time histogram metric for improved sift matching},
      author={Pele, Ofir and Werman, Michael},
      booktitle={Computer Vision--ECCV 2008},
      pages={495--508},
      year={2008},
      month={October},
      publisher={Springer}
    }

Ofir Pele and Michael Werman, "Fast and robust earth mover's distances," in *Proc. 2009 IEEE 12th Int. Conf. on Computer Vision*, Kyoto, Japan, 2009, pp. 460-467.

.. code-block:: latex

    @INPROCEEDINGS{pele2009,
      title={Fast and robust earth mover's distances},
      author={Pele, Ofir and Werman, Michael},
      booktitle={2009 IEEE 12th International Conference on Computer Vision},
      pages={460--467},
      year={2009},
      month={September},
      organization={IEEE}
    }
