#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# distutils: language = c++

from libcpp.vector cimport vector
from libcpp.pair cimport pair
import cython

# Import both NumPy and the Cython declarations for NumPy
import numpy as np
cimport numpy as np


# Declare the interface to the C++ EMD library
# ============================================

cdef extern from "lib/emd_hat.hpp":
    cdef pair[double, vector[vector[double]]] emd_hat_gd_metric_double_wrapper(vector[double],
                                                 vector[double],
                                                 vector[vector[double]],
                                                 double) except +

    cdef vector[vector[double]] emd_hat_gd_metric_double_wrapper_vector(vector[double],
                                                 vector[double],
                                                 vector[vector[double]],
                                                 double) except +



# Define the API
# ==============
def emd_with_flows(np.ndarray[np.float64_t, ndim=1, mode="c"] first_signature,
                   np.ndarray[np.float64_t, ndim=1, mode="c"] second_signature,
                   np.ndarray[np.float64_t, ndim=2, mode="c"] distance_matrix,
                   extra_mass_penalty=-1.0):
    """
    Compute the Earth Mover's Distance between the given signature with the
    given distance matrix.
    Return a tuple containing the EMD value and the flows array.

    :param first_signature: A 1D numpy array of ``np.double``, of length
        :math:`N`.
    :param second_signature: A 1D numpy array of ``np.double``, also of length
        :math:`N`..
    :param distance_matrix: A 2D numpy array of ``np.double``, of size
        :math:`N \cross N`.
    :param extra_mass_penalty: The penalty for extra mass. If you want the
        resulting distance to be a metric, it should be at least half the
        diameter of the space (maximum possible distance between any two
        points). If you want partial matching you can set it to zero (but then
        the resulting distance is not guaranteed to be a metric). The default
        value is -1 which means the maximum value in the distance matrix is
        used.
    """
    if (first_signature.shape[0] > distance_matrix.shape[0] or
            second_signature.shape[0] > distance_matrix.shape[0]):
        raise ValueError('Signature dimension cannot be larger than '
                         'dimensions of distance matrix')

    if (first_signature.shape[0] != second_signature.shape[0]):
        raise ValueError("Signature dimensions must be equal")

    return emd_hat_gd_metric_double_wrapper(first_signature,
                                            second_signature,
                                            distance_matrix,
                                            extra_mass_penalty)



def emd(np.ndarray[np.float64_t, ndim=1, mode="c"] first_signature,
        np.ndarray[np.float64_t, ndim=1, mode="c"] second_signature,
        np.ndarray[np.float64_t, ndim=2, mode="c"] distance_matrix,
        extra_mass_penalty=-1.0):
    """
    Compute the Earth Mover's Distance between the given signatures with the
    given distance matrix.

    :param first_signature: A 1D numpy array of ``np.double``, of length
        :math:`N`.
    :param second_signature: A 1D numpy array of ``np.double``, also of length
        :math:`N`..
    :param distance_matrix: A 2D numpy array of ``np.double``, of size
        :math:`N \cross N`.
    :param extra_mass_penalty: The penalty for extra mass. If you want the
        resulting distance to be a metric, it should be at least half the
        diameter of the space (maximum possible distance between any two
        points). If you want partial matching you can set it to zero (but then
        the resulting distance is not guaranteed to be a metric). The default
        value is -1 which means the maximum value in the distance matrix is
        used.
    """

    emd,flows = emd_with_flows(first_signature,
                               second_signature,
                               distance_matrix,
                               extra_mass_penalty)
    return emd
