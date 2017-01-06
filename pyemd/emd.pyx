#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# distutils: language = c++
# emd.pyx

from libcpp.vector cimport vector
from libcpp.pair cimport pair
import cython

# Import both NumPy and the Cython declarations for NumPy
import numpy as np
cimport numpy as np


# Declare the interface to the C++ EMD library
# ============================================

cdef extern from "lib/emd_hat.hpp":

    cdef double \
        emd_hat_gd_metric_double(vector[double], 
                                 vector[double],
                                 vector[vector[double]], 
                                 double) except +

    cdef pair[double, vector[vector[double]]] \
        emd_hat_gd_metric_double_with_flow_wrapper(vector[double], 
                                                   vector[double],
                                                   vector[vector[double]],
                                                   double) except +


# Define the API
# ==============

DEFAULT_EXTRA_MASS_PENALTY = -1.0


def validate(first_signature, second_signature, distance_matrix):
    """Validate input."""
    if (first_signature.shape[0] > distance_matrix.shape[0] or
            second_signature.shape[0] > distance_matrix.shape[0]):
        raise ValueError('Signature dimension cannot be larger than '
                         'dimensions of distance matrix')
    if (first_signature.shape[0] != second_signature.shape[0]):
        raise ValueError('Signature dimensions must be equal')


def emd(np.ndarray[np.float64_t, ndim=1, mode="c"] first_signature,
        np.ndarray[np.float64_t, ndim=1, mode="c"] second_signature,
        np.ndarray[np.float64_t, ndim=2, mode="c"] distance_matrix,
        extra_mass_penalty=DEFAULT_EXTRA_MASS_PENALTY):
    """
    Compute the EMD between signatures with the given distance matrix.

    Args:
        first_signature (np.ndarray): A 1-dimensional array of type
            ``np.double``, of length :math:`N`.
        second_signature (np.ndarray): A 1-dimensional array of ``np.double``,
            also of length :math:`N`.
        distance_matrix (np.ndarray): A 2-dimensional  array of ``np.double``,
            of size :math:`N \cross N`.
        extra_mass_penalty: The penalty for extra mass. If you want the
            resulting distance to be a metric, it should be at least half the
            diameter of the space (maximum possible distance between any two
            points). If you want partial matching you can set it to zero (but then
            the resulting distance is not guaranteed to be a metric). The default
            value is -1, which means the maximum value in the distance matrix is
            used.

    Returns:
        float: The EMD value.
    """
    validate(first_signature, second_signature, distance_matrix)
    return emd_hat_gd_metric_double(first_signature, 
                                    second_signature,
                                    distance_matrix, 
                                    extra_mass_penalty)


def emd_with_flow(np.ndarray[np.float64_t, ndim=1, mode="c"] first_signature,
                  np.ndarray[np.float64_t, ndim=1, mode="c"] second_signature,
                  np.ndarray[np.float64_t, ndim=2, mode="c"] distance_matrix,
                  extra_mass_penalty=DEFAULT_EXTRA_MASS_PENALTY):
    """
    Compute the EMD between signatures with the given distance matrix.

    Args:
        first_signature (np.ndarray): A 1-dimensional array of type
            ``np.double``, of length :math:`N`.
        second_signature (np.ndarray): A 1-dimensional array of ``np.double``,
            also of length :math:`N`.
        distance_matrix (np.ndarray): A 2-dimensional  array of ``np.double``,
            of size :math:`N \cross N`.
        extra_mass_penalty: The penalty for extra mass. If you want the
            resulting distance to be a metric, it should be at least half the
            diameter of the space (maximum possible distance between any two
            points). If you want partial matching you can set it to zero (but then
            the resulting distance is not guaranteed to be a metric). The default
            value is -1, which means the maximum value in the distance matrix is
            used.

    Returns:
        (float, list(float)): The EMD value and the associated minimum-cost flow.
    """
    validate(first_signature, second_signature, distance_matrix)
    return emd_hat_gd_metric_double_with_flow_wrapper(first_signature,
                                                      second_signature,
                                                      distance_matrix,
                                                      extra_mass_penalty)
