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


def euclidean_pairwise_distance_matrix(x):
    """Calculate the Euclidean pairwise distance matrix for a 1D array."""
    distance_matrix = np.abs(np.repeat(x, len(x)) - np.tile(x, len(x)))
    return distance_matrix.reshape(len(x), len(x))


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


def emd_samples(first_array,
                second_array,
                extra_mass_penalty=DEFAULT_EXTRA_MASS_PENALTY,
                distance='euclidean',
                normalized=True,
                bins='auto',
                range=None):
    u"""Return the EMD between the histograms of two arrays.

    Arguments:
        first_array (np.ndarray): A 1-dimensional array of type np.float64.
        second_array (np.ndarray): A 1-dimensional array of type np.float64.

    Keyword Arguments:
        extra_mass_penalty: The penalty for extra mass. If you want the
            resulting distance to be a metric, it should be at least half the
            diameter of the space (maximum possible distance between any two
            points). If you want partial matching you can set it to zero (but then
            the resulting distance is not guaranteed to be a metric). The default
            value is -1, which means the maximum value in the distance matrix is
            used.
        bins (int or string): The number of bins to include in the generated
            histogram. If a string, must be one of the bin selection algorithms
            accepted by `np.histogram`. Defaults to 'auto', which gives the
            maximum of the ‘sturges’ and ‘fd’ estimators.
        distance (string or function): A string or function implementing a
            metric on a 1D np.ndarray. Default to euclidean distance.
            Currently limited to 'euclidean' or your own function which takes
            for input a 1D array and returns a square 2D array of pairwise
            distances.
        normalized (boolean): If true, treat histograms as fractions of the
            dataset. If false, treat histograms as counts. In the latter case
            the EMD will vary greatly by array length.
        range (int min, int max): A tuple of minimum and maximum values for
            histogram. Defaults to the range of the union of `first_array`
            and `second_array`. Note: if the given range is not a superset
            of the default range, no warning will be given.

    Returns:
        float: The EMD value.
    """
    # Get the default range
    if range is None:
        range = (min(np.min(first_array), np.min(second_array)),
                 max(np.max(first_array), np.max(second_array)))
    # Use automatic binning from `np.histogram()`
    # TODO: Use `np.histogram_bin_edges()` when it's available;
    # see https://github.com/numpy/numpy/issues/10183
    if isinstance(bins, str):
        hist, _ = np.histogram(np.concatenate([first_array,
                                               second_array]),
                               range=range,
                               bins=bins)
        bins = len(hist)

    if distance == 'euclidean':
        distance = euclidean_pairwise_distance_matrix

    # Compute histograms
    first_histogram, bin_edges = np.histogram(first_array,
                                              range=range,
                                              bins=bins)
    second_histogram, _ = np.histogram(second_array,
                                       range=range,
                                       bins=bins)
    # Cast to C++ long
    first_histogram = first_histogram.astype(np.float64)
    second_histogram = second_histogram.astype(np.float64)
    # Normalize histograms to represent fraction of dataset in each bin
    if normalized:
        first_histogram = first_histogram/np.sum(first_histogram)
        second_histogram = second_histogram/np.sum(second_histogram)

    # Compute the distance matrix between the center of each bin
    bin_locations = np.mean([bin_edges[:-1], bin_edges[1:]], axis=0)
    distance_matrix = distance(bin_locations)

    return emd(first_histogram,
               second_histogram,
               distance_matrix,
               extra_mass_penalty=extra_mass_penalty)


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
