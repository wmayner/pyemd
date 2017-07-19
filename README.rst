.. image:: https://img.shields.io/travis/wmayner/pyemd/develop.svg?style=flat-square&maxAge=3600
    :target: https://travis-ci.org/wmayner/pyemd
.. image:: https://img.shields.io/pypi/pyversions/pyemd.svg?style=flat-square&maxAge=86400
    :target: https://wiki.python.org/moin/Python2orPython3
    :alt: Python versions badge

**************************
PyEMD: Fast EMD for Python
**************************

PyEMD is a Python wrapper for `Ofir Pele and Michael Werman's implementation
<http://www.ariel.ac.il/sites/ofirpele/fastemd/code/>`_ of the `Earth Mover's
Distance <http://en.wikipedia.org/wiki/Earth_mover%27s_distance>`_ that allows
it to be used with NumPy. **If you use this code, please cite the papers listed
at the end of this document.**


Installation
~~~~~~~~~~~~

To install the latest release:

.. code:: bash

    pip install pyemd

Before opening an issue related to installation, please try to install PyEMD in
a fresh, empty Python 3 virtual environment and check that the problem
persists.


Usage
~~~~~

.. code:: python

    >>> from pyemd import emd
    >>> import numpy as np
    >>> first_histogram = np.array([0.0, 1.0])
    >>> second_histogram = np.array([5.0, 3.0])
    >>> distance_matrix = np.array([[0.0, 0.5], 
    ...                             [0.5, 0.0]])
    >>> emd(first_histogram, second_histogram, distance_matrix)
    3.5

You can also get the associated minimum-cost flow:

.. code:: python

    >>> from pyemd import emd_with_flow
    >>> emd_with_flow(first_histogram, second_histogram, distance_matrix)
    (3.5, [[0.0, 0.0], [0.0, 1.0]])


API
~~~

.. code:: python

    emd(first_histogram, second_histogram, distance_matrix)

- ``first_histogram``: A 1-dimensional numpy array of type ``np.float64``, of
  length :math:`N`.
- ``second_histogram``: A 1-dimensional numpy array of type ``np.float64``, of
  length :math:`N`.
- ``distance_matrix``: A 2-dimensional array of type ``np.float64``, of size at
  least :math:`N \times N`. This defines the underlying metric, or ground
  distance, by giving the pairwise distances between the histogram bins. It
  must represent a metric; there is no warning if it doesn't.

The arguments to ``emd_with_flow`` are the same.


Limitations and Caveats
~~~~~~~~~~~~~~~~~~~~~~~

- ``distance_matrix`` is assumed to represent a metric; there is no check to
  ensure that this is true. See the documentation in ``pyemd/lib/emd_hat.hpp``
  for more information.
- The flow matrix does not contain the flows to/from the extra mass bin.
- The histograms and distance matrix must be numpy arrays of type
  ``np.float64``. The original C++ template function can accept any numerical
  C++ type, but this wrapper only instantiates the template with ``double``
  (Cython converts ``np.float64`` to ``double``). If there's demand, I can add
  support for other types.


Contributing
~~~~~~~~~~~~

To help develop PyEMD, fork the project on GitHub and install the requirements
with ``pip``.

The ``Makefile`` defines some tasks to help with development:

* ``default``: compile the Cython code into C++ and build the C++ into a Python
  extension, using the ``setup.py`` build command
* ``build``: same as default, but using the ``cython`` command
* ``clean``: remove the build directory and the compiled C++ extension
* ``test``: run unit tests with ``py.test``

Tests for different Python environments can be run by installing ``tox`` with
``pip install tox`` and running the ``tox`` command.

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

Ofir Pele and Michael Werman, "A linear time histogram metric for improved SIFT
matching," in *Computer Vision - ECCV 2008*, Marseille, France, 2008, pp.
495-508.

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

Ofir Pele and Michael Werman, "Fast and robust earth mover's distances," in
*Proc. 2009 IEEE 12th Int. Conf. on Computer Vision*, Kyoto, Japan, 2009, pp.
460-467.

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
