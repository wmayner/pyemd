.. image:: https://img.shields.io/github/actions/workflow/status/wmayner/pyemd/build_wheels.yml?style=flat-square&maxAge=86400
    :target: https://github.com/wmayner/pyemd/actions/workflows/build_wheels.yml
    :alt: Build status badge
.. image:: https://img.shields.io/pypi/pyversions/pyemd.svg?style=flat-square&maxAge=86400
    :target: https://pypi.org/project/pyemd/
    :alt: Python versions badge

PyEMD: Fast EMD for Python
==========================

PyEMD is a Python wrapper for `Ofir Pele and Michael Werman's implementation
<https://ofirpele.droppages.com/>`_ of the `Earth Mover's
Distance <https://en.wikipedia.org/wiki/Earth_mover%27s_distance>`_ that allows
it to be used with NumPy. **If you use this code, please cite the papers listed
at the end of this document.**


Usage
-----

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

You can also calculate the EMD directly from two arrays of observations:

.. code:: python

    >>> from pyemd import emd_samples
    >>> first_array = [1, 2, 3, 4]
    >>> second_array = [2, 3, 4, 5]
    >>> emd_samples(first_array, second_array, bins=2)
    0.5


API Documentation
-----------------

emd()
~~~~~

.. code:: python

    emd(first_histogram,
        second_histogram,
        distance_matrix,
        extra_mass_penalty=-1.0)

*Arguments:*

- ``first_histogram`` *(np.ndarray)*: A 1D array of type ``np.float64`` of
  length *N*.
- ``second_histogram`` *(np.ndarray)*: A 1D array of ``np.float64`` of length
  *N*.
- ``distance_matrix`` *(np.ndarray)*: A 2D array of ``np.float64,`` of size at
  least *N* × *N*. This defines the underlying metric, or ground distance, by
  giving the pairwise distances between the histogram bins.
  **NOTE: It must represent a metric; there is no warning if it doesn't.**

*Keyword Arguments:*

- ``extra_mass_penalty`` *(float)*: The penalty for extra mass. If you want the
  resulting distance to be a metric, it should be at least half the diameter of
  the space (maximum possible distance between any two points). If you want
  partial matching you can set it to zero (but then the resulting distance is
  not guaranteed to be a metric). The default value is ``-1.0``, which means
  the maximum value in the distance matrix is used.

*Returns:* *(float)* The EMD value.

----

emd_with_flow()
~~~~~~~~~~~~~~~

.. code:: python

    emd_with_flow(first_histogram,
                  second_histogram,
                  distance_matrix,
                  extra_mass_penalty=-1.0)

Arguments are the same as for ``emd()``.

*Returns:* *(tuple(float, list(list(float))))* The EMD value and the associated
minimum-cost flow.

----

emd_samples()
~~~~~~~~~~~~~

.. code:: python

    emd_samples(first_array,
                second_array,
                extra_mass_penalty=-1.0,
                distance='euclidean',
                normalized=True,
                bins='auto',
                range=None)

*Arguments:*

- ``first_array`` *(Iterable)*: An array of samples used to generate a
  histogram.
- ``second_array`` *(Iterable)*: An array of samples used to generate a
  histogram.

*Keyword Arguments:*

- ``extra_mass_penalty`` *(float)*: Same as for ``emd()``.
- ``distance`` *(string or function)*: A string or function implementing
  a metric on a 1D ``np.ndarray``. Defaults to the Euclidean distance.
  Currently limited to 'euclidean' or your own function, which must take
  a 1D array and return a square 2D array of pairwise distances.
- ``normalized`` (*boolean*): If true (default), treat histograms as fractions
  of the dataset. If false, treat histograms as counts. In the latter case the
  EMD will vary greatly by array length.
- ``bins`` *(int or string)*: The number of bins to include in the generated
  histogram. If a string, must be one of the bin selection algorithms accepted
  by ``np.histogram()``. Defaults to ``'auto'``, which gives the maximum of the
  'sturges' and 'fd' estimators.
- ``range`` *(tuple(int, int))*: The lower and upper range of the bins, passed
  to ``numpy.histogram()``. Defaults to the range of the union of
  ``first_array`` and ``second_array``. Note: if the given range is not a
  superset of the default range, no warning will be given.

*Returns:* *(float)* The EMD value between the histograms of ``first_array``
and ``second_array``.

----


Limitations and Caveats
-----------------------

- ``emd()`` and ``emd_with_flow()``:

  - The ``distance_matrix`` is assumed to represent a metric; there is no check
    to ensure that this is true. See the documentation in
    ``pyemd/lib/emd_hat.hpp`` for more information.
  - The histograms and distance matrix must be numpy arrays of type
    ``np.float64``. The original C++ template function can accept any numerical
    C++ type, but this wrapper only instantiates the template with ``double``
    (Cython converts ``np.float64`` to ``double``). If there's demand, I can
    add support for other types.

- ``emd_with_flow()``:

  - The flow matrix does not contain the flows to/from the extra mass bin.

- ``emd_samples()``:

  - With ``numpy < 1.15.0``, using the default ``bins='auto'`` results in an
    extra call to ``np.histogram()`` to determine the bin lengths, since `the
    NumPy bin-selectors are not exposed in the public API
    <https://github.com/numpy/numpy/issues/10183>`_. For performance, you may
    want to set the bins yourself. If ``numpy >= 1.15`` is available,
    ``np.histogram_bin_edges()`` is called instead, which is more efficient.


Credit
------

- All credit for the actual algorithm and implementation goes to `Ofir Pele
  <https://ofirpele.droppages.com/>`_ and `Michael Werman
  <https://www.cs.huji.ac.il/~werman/>`_. See the `relevant paper
  <https://doi.org/10.1109/ICCV.2009.5459199>`_.
- Thanks to the Cython developers for making this kind of wrapper relatively
  easy to write.

Please cite these papers if you use this code:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ofir Pele and Michael Werman. Fast and robust earth mover's distances. *Proc.
2009 IEEE 12th Int. Conf. on Computer Vision*, Kyoto, Japan, 2009, pp. 460-467.

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

Ofir Pele and Michael Werman. A linear time histogram metric for improved SIFT
matching. *Computer Vision - ECCV 2008*, Marseille, France, 2008, pp. 495-508.

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
