#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# emd.py

"""PyEMD: Earth Mover's Distance using POT (Python Optimal Transport)."""

from collections.abc import Callable, Sequence

import numpy as np
from numpy.typing import ArrayLike
import ot
import ot.partial


DEFAULT_EXTRA_MASS_PENALTY = -1.0


def _preflow_same_bins(
    a: np.ndarray, b: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Pre-flow mass within same bins (C++ emd_hat_gd_metric optimization).

    For a metric distance matrix, mass can be transported within the same bin
    at zero cost. This pre-processing step cancels out the minimum mass in
    each bin before computing the actual transport.

    Returns:
        a_reduced, b_reduced: Modified histograms with same-bin mass removed
        preflow: Matrix of pre-flowed mass (diagonal only)
    """
    a_reduced = a.copy()
    b_reduced = b.copy()
    n = len(a)
    preflow = np.zeros((n, n))

    for i in range(n):
        if a_reduced[i] < b_reduced[i]:
            preflow[i, i] = a_reduced[i]
            b_reduced[i] -= a_reduced[i]
            a_reduced[i] = 0
        else:
            preflow[i, i] = b_reduced[i]
            a_reduced[i] -= b_reduced[i]
            b_reduced[i] = 0

    return a_reduced, b_reduced, preflow


def _validate_emd_input(
    first_histogram: np.ndarray,
    second_histogram: np.ndarray,
    distance_matrix: np.ndarray,
) -> None:
    """Validate EMD input."""
    if (
        first_histogram.shape[0] > distance_matrix.shape[0]
        or second_histogram.shape[0] > distance_matrix.shape[0]
    ):
        raise ValueError(
            "Histogram lengths cannot be greater than the "
            "number of rows or columns of the distance matrix"
        )
    if first_histogram.shape[0] != second_histogram.shape[0]:
        raise ValueError("Histogram lengths must be equal")


def emd(
    first_histogram: np.ndarray,
    second_histogram: np.ndarray,
    distance_matrix: np.ndarray,
    extra_mass_penalty: float = DEFAULT_EXTRA_MASS_PENALTY,
) -> float:
    """Return the EMD between two histograms using the given distance matrix.

    The Earth Mover's Distance is the minimal cost of turning one histogram into
    another by moving around the "dirt" in the bins, where the cost of moving
    dirt from one bin to another is given by the amount of dirt times the
    "ground distance" between the bins.

    Arguments:
        first_histogram (np.ndarray): A 1D array of type np.float64 of length N.
        second_histogram (np.ndarray): A 1D array of np.float64 of length N.
        distance_matrix (np.ndarray): A 2D array of np.float64, of size at least
            N × N. This defines the underlying metric, or ground distance, by
            giving the pairwise distances between the histogram bins. It must
            represent a metric; there is no warning if it doesn't.

    Keyword Arguments:
        extra_mass_penalty (float): The penalty for extra mass. If you want the
            resulting distance to be a metric, it should be at least half the
            diameter of the space (maximum possible distance between any two
            points). If you want partial matching you can set it to zero (but
            then the resulting distance is not guaranteed to be a metric). The
            default value is -1, which means the maximum value in the distance
            matrix is used.

    Returns:
        float: The EMD value.

    Raises:
        ValueError: If the length of either histogram is greater than the number
        of rows or columns of the distance matrix, or if the histograms aren't
        the same length.
    """
    a = np.asarray(first_histogram)
    b = np.asarray(second_histogram)
    M = np.asarray(distance_matrix)

    _validate_emd_input(a, b, M)

    # Default penalty = max distance (same as PyEMD's C++ implementation)
    if extra_mass_penalty == -1.0:
        extra_mass_penalty = M.max()

    # Pre-flow: cancel mass within same bins (zero-cost transport)
    a_reduced, b_reduced, _ = _preflow_same_bins(a, b)

    sum_a = a_reduced.sum()
    sum_b = b_reduced.sum()
    extra_mass = abs(a.sum() - b.sum())

    # Edge case: all mass was pre-flowed
    if sum_a == 0 or sum_b == 0:
        return float(extra_mass * extra_mass_penalty)

    # Compute transport for remaining mass using partial transport
    # This matches C++ behavior: transport min_sum units from original distributions
    min_sum = min(sum_a, sum_b)

    # Use partial transport to move exactly min_sum units
    # POT's partial_wasserstein transports exactly m mass
    G = ot.partial.partial_wasserstein(a_reduced, b_reduced, M, m=min_sum)
    transport_cost = np.sum(G * M)

    # Add penalty for extra mass
    return float(transport_cost + extra_mass * extra_mass_penalty)


def emd_with_flow(
    first_histogram: np.ndarray,
    second_histogram: np.ndarray,
    distance_matrix: np.ndarray,
    extra_mass_penalty: float = DEFAULT_EXTRA_MASS_PENALTY,
) -> tuple[float, list[list[float]]]:
    """Return the EMD and flow between two histograms using the given distance matrix.

    The Earth Mover's Distance is the minimal cost of turning one histogram into
    another by moving around the "dirt" in the bins, where the cost of moving
    dirt from one bin to another is given by the amount of dirt times the
    "ground distance" between the bins.

    Arguments:
        first_histogram (np.ndarray): A 1D array of type np.float64 of length N.
        second_histogram (np.ndarray): A 1D array of np.float64 of length N.
        distance_matrix (np.ndarray): A 2D array of np.float64, of size at least
            N × N. This defines the underlying metric, or ground distance, by
            giving the pairwise distances between the histogram bins. It must
            represent a metric; there is no warning if it doesn't.

    Keyword Arguments:
        extra_mass_penalty (float): The penalty for extra mass. If you want the
            resulting distance to be a metric, it should be at least half the
            diameter of the space (maximum possible distance between any two
            points). If you want partial matching you can set it to zero (but
            then the resulting distance is not guaranteed to be a metric). The
            default value is -1, which means the maximum value in the distance
            matrix is used.

    Returns:
        (tuple(float, list(list(float)))): The EMD value and the associated
        minimum-cost flow.

    Raises:
        ValueError: If the length of either histogram is greater than the number
        of rows or columns of the distance matrix, or if the histograms aren't
        the same length.
    """
    a = np.asarray(first_histogram)
    b = np.asarray(second_histogram)
    M = np.asarray(distance_matrix)

    _validate_emd_input(a, b, M)

    if extra_mass_penalty == -1.0:
        extra_mass_penalty = M.max()

    # Pre-flow: cancel mass within same bins
    a_reduced, b_reduced, preflow = _preflow_same_bins(a, b)

    sum_a = a_reduced.sum()
    sum_b = b_reduced.sum()
    extra_mass = abs(a.sum() - b.sum())

    # Edge case: all mass was pre-flowed
    if sum_a == 0 or sum_b == 0:
        return float(extra_mass * extra_mass_penalty), preflow.tolist()

    # Use partial transport to move exactly min_sum units
    min_sum = min(sum_a, sum_b)
    G = ot.partial.partial_wasserstein(a_reduced, b_reduced, M, m=min_sum)
    transport_cost = np.sum(G * M)

    # Combine preflow and actual transport
    flow = preflow + G

    total_cost = float(transport_cost + extra_mass * extra_mass_penalty)
    return total_cost, flow.tolist()


def euclidean_pairwise_distance_matrix(x: np.ndarray) -> np.ndarray:
    """Calculate the Euclidean pairwise distance matrix for a 1D array."""
    distance_matrix = np.abs(np.repeat(x, len(x)) - np.tile(x, len(x)))
    return distance_matrix.reshape(len(x), len(x))


get_bins = np.histogram_bin_edges


def emd_samples(
    first_array: ArrayLike,
    second_array: ArrayLike,
    extra_mass_penalty: float = DEFAULT_EXTRA_MASS_PENALTY,
    distance: str | Callable[[np.ndarray], np.ndarray] = "euclidean",
    normalized: bool = True,
    bins: int | str = "auto",
    range: tuple[float, float] | None = None,
) -> float:
    """Return the EMD between the histograms of two arrays.

    See ``emd()`` for more information about the EMD.

    Note:
        Pairwise ground distances are taken from the center of the bins.

    Arguments:
        first_array (Iterable): An array of samples used to generate a
            histogram.
        second_array (Iterable): An array of samples used to generate a
            histogram.

    Keyword Arguments:
        extra_mass_penalty (float): The penalty for extra mass. If you want the
            resulting distance to be a metric, it should be at least half the
            diameter of the space (maximum possible distance between any two
            points). If you want partial matching you can set it to zero (but
            then the resulting distance is not guaranteed to be a metric). The
            default value is -1, which means the maximum value in the distance
            matrix is used.
        distance (string or function): A string or function implementing
            a metric on a 1D ``np.ndarray``. Defaults to the Euclidean distance.
            Currently limited to 'euclidean' or your own function, which must
            take a 1D array and return a square 2D array of pairwise distances.
        normalized (boolean): If true (default), treat histograms as fractions
            of the dataset. If false, treat histograms as counts. In the latter
            case the EMD will vary greatly by array length.
        bins (int or string): The number of bins to include in the generated
            histogram. If a string, must be one of the bin selection algorithms
            accepted by ``np.histogram()``. Defaults to 'auto', which gives the
            maximum of the 'sturges' and 'fd' estimators.
        range (tuple(int, int)): The lower and upper range of the bins, passed
            to ``numpy.histogram()``. Defaults to the range of the union of
            ``first_array`` and `second_array``.` Note: if the given range is
            not a superset of the default range, no warning will be given.

    Returns:
        float: The EMD value between the histograms of ``first_array`` and
        ``second_array``.

    Raises:
        ValueError: If arrays are empty or distance matrix is invalid.
    """
    first_array = np.array(first_array)
    second_array = np.array(second_array)
    # Validate arrays
    if not (first_array.size > 0 and second_array.size > 0):
        raise ValueError("Arrays of samples cannot be empty.")
    # Get the default range
    if range is None:
        range = (
            min(np.min(first_array), np.min(second_array)),
            max(np.max(first_array), np.max(second_array)),
        )
    # Get bin edges using both arrays
    # Convert to float64 to avoid NumPy 2.1+ integer bin width constraint
    # (bin width is forced to >= 1 for integer dtypes, causing too few bins)
    bins = get_bins(
        np.concatenate([first_array, second_array]).astype(np.float64),
        range=range,
        bins=bins,
    )
    # Compute histograms
    first_histogram, bin_edges = np.histogram(first_array, range=range, bins=bins)
    second_histogram, _ = np.histogram(second_array, range=range, bins=bins)
    # Cast to float64
    first_histogram = first_histogram.astype(np.float64)
    second_histogram = second_histogram.astype(np.float64)
    # Normalize histograms to represent fraction of dataset in each bin
    if normalized:
        first_histogram = first_histogram / np.sum(first_histogram)
        second_histogram = second_histogram / np.sum(second_histogram)
    # Compute the distance matrix between the center of each bin
    bin_locations = np.mean([bin_edges[:-1], bin_edges[1:]], axis=0)
    if distance == "euclidean":
        distance = euclidean_pairwise_distance_matrix
    distance_matrix = distance(bin_locations)
    # Validate distance matrix
    if len(distance_matrix) != len(distance_matrix[0]):
        raise ValueError(
            "Distance matrix must be square; check your `distance` function."
        )
    if (
        first_histogram.shape[0] > len(distance_matrix)
        or second_histogram.shape[0] > len(distance_matrix)
    ):
        raise ValueError(
            "Distance matrix must have at least as many rows/columns as there "
            "are bins in the histograms; check your `distance` function."
        )
    # Return the EMD
    return emd(first_histogram, second_histogram, distance_matrix, extra_mass_penalty)
