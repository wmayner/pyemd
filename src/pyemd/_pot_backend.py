"""POT-based EMD implementation - matches PyEMD's C++ behavior exactly."""

import numpy as np
import ot
import ot.partial


def _preflow_same_bins(a, b):
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


def _pot_emd(first_histogram, second_histogram, distance_matrix, extra_mass_penalty=-1.0):
    """Compute EMD using POT, matching PyEMD's C++ behavior exactly.

    This implementation replicates the exact behavior of PyEMD's C++ backend:
    1. Pre-flow mass within same bins at zero cost (metric property)
    2. Transport remaining mass using optimal transport
    3. Add penalty for unmatched extra mass
    """
    a = np.asarray(first_histogram, dtype=np.float64)
    b = np.asarray(second_histogram, dtype=np.float64)
    M = np.asarray(distance_matrix, dtype=np.float64)

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


def _pot_emd_with_flow(first_histogram, second_histogram, distance_matrix, extra_mass_penalty=-1.0):
    """Compute EMD and flow matrix using POT.

    Returns the same format as PyEMD's C++ backend: (emd_value, flow_matrix)
    where flow_matrix is a list of lists.

    Note: Like the C++ implementation, the flow matrix does not include flows
    to/from the extra mass bin.
    """
    a = np.asarray(first_histogram, dtype=np.float64)
    b = np.asarray(second_histogram, dtype=np.float64)
    M = np.asarray(distance_matrix, dtype=np.float64)

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
