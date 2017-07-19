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


def validate(first_histogram, second_histogram, distance_matrix):
    """Validate input."""
    if (first_histogram.shape[0] > distance_matrix.shape[0] or
        second_histogram.shape[0] > distance_matrix.shape[0]):
        raise ValueError('Histogram lengths cannot be greater than the '
                         'number of rows or columns of the distance matrix')
    if (first_histogram.shape[0] != second_histogram.shape[0]):
        raise ValueError('Histogram lengths must be equal')


def emd(np.ndarray[np.float64_t, ndim=1, mode="c"] first_histogram,
        np.ndarray[np.float64_t, ndim=1, mode="c"] second_histogram,
        np.ndarray[np.float64_t, ndim=2, mode="c"] distance_matrix,
        extra_mass_penalty=DEFAULT_EXTRA_MASS_PENALTY):
    u"""Return the EMD between two histograms using the given distance matrix.

    The Earth Mover's Distance is the minimal cost of turning one histogram
    into another by moving around the “dirt” in the bins, where the cost of
    moving dirt from one bin to another is given by the amount of dirt times
    the “ground distance” between the bins.

    Arguments:
        first_histogram (np.ndarray): A 1-dimensional array of type np.float64,
            of length N.
        second_histogram (np.ndarray): A 1-dimensional array of np.float64,
            also of length N.
        distance_matrix (np.ndarray): A 2-dimensional array of np.float64, of
            size at least N × N. This defines the underlying metric, or ground
            distance, by giving the pairwise distances between the histogram
            bins. It must represent a metric; there is no warning if it
            doesn't.

    Keyword Arguments:
        extra_mass_penalty: The penalty for extra mass. If you want the
            resulting distance to be a metric, it should be at least half the
            diameter of the space (maximum possible distance between any two
            points). If you want partial matching you can set it to zero (but then
            the resulting distance is not guaranteed to be a metric). The default
            value is -1, which means the maximum value in the distance matrix is
            used.

    Returns:
        float: The EMD value.

    Raises:
        ValueError: If the length of either histogram is greater than the
        number of rows or columns of the distance matrix, or if the histograms
        aren't the same length.
    """
    validate(first_histogram, second_histogram, distance_matrix)
    return emd_hat_gd_metric_double(first_histogram, 
                                    second_histogram,
                                    distance_matrix, 
                                    extra_mass_penalty)


def emd_with_flow(np.ndarray[np.float64_t, ndim=1, mode="c"] first_histogram,
                  np.ndarray[np.float64_t, ndim=1, mode="c"] second_histogram,
                  np.ndarray[np.float64_t, ndim=2, mode="c"] distance_matrix,
                  extra_mass_penalty=DEFAULT_EXTRA_MASS_PENALTY):
    u"""Return the EMD between two histograms using the given distance matrix.

    The Earth Mover's Distance is the minimal cost of turning one histogram
    into another by moving around the “dirt” in the bins, where the cost of
    moving dirt from one bin to another is given by the amount of dirt times
    the “ground distance” between the bins.

    Arguments:
        first_histogram (np.ndarray): A 1-dimensional array of type np.float64,
            of length N.
        second_histogram (np.ndarray): A 1-dimensional array of np.float64,
            also of length N.
        distance_matrix (np.ndarray): A 2-dimensional array of np.float64, of
            size at least N × N. This defines the underlying metric, or ground
            distance, by giving the pairwise distances between the histogram
            bins. It must represent a metric; there is no warning if it
            doesn't.

    Keyword Arguments:
        extra_mass_penalty: The penalty for extra mass. If you want the
            resulting distance to be a metric, it should be at least half the
            diameter of the space (maximum possible distance between any two
            points). If you want partial matching you can set it to zero (but then
            the resulting distance is not guaranteed to be a metric). The default
            value is -1, which means the maximum value in the distance matrix is
            used.

    Returns:
        (float, list(list(float))): The EMD value and the associated
        minimum-cost flow.

    Raises:
        ValueError: If the length of either histogram is greater than the
        number of rows or columns of the distance matrix, or if the histograms
        aren't the same length.
    """
    validate(first_histogram, second_histogram, distance_matrix)
    return emd_hat_gd_metric_double_with_flow_wrapper(first_histogram,
                                                      second_histogram,
                                                      distance_matrix,
                                                      extra_mass_penalty)
