#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# test/test_pyemd.py
"""Tests for PyEMD"""

import numpy as np
import pytest

from pyemd import emd, emd_samples, emd_with_flow


EMD_PRECISION = 5
FLOW_PRECISION = 4


def emd_assert(got, expected):
    assert round(got, EMD_PRECISION) == expected


def emd_flow_assert(got, expected):
    got_value, got_flow = got
    expected_value, expected_flow = expected
    assert round(got_value, EMD_PRECISION) == expected_value
    assert np.array_equal(np.round(got_flow, FLOW_PRECISION), expected_flow)


# `emd()`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def test_emd_1():
    first_signature = np.array([0.0, 1.0])
    second_signature = np.array([5.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5], [0.5, 0.0]])
    emd_assert(emd(first_signature, second_signature, distance_matrix), 3.5)


def test_emd_2():
    first_signature = np.array([1.0, 1.0])
    second_signature = np.array([1.0, 1.0])
    distance_matrix = np.array([[0.0, 1.0], [1.0, 0.0]])
    emd_assert(emd(first_signature, second_signature, distance_matrix), 0.0)


def test_emd_3():
    first_signature = np.array([6.0, 1.0])
    second_signature = np.array([1.0, 7.0])
    distance_matrix = np.array([[0.0, 0.0], [0.0, 0.0]])
    emd_assert(emd(first_signature, second_signature, distance_matrix), 0.0)


def test_emd_4():
    first_signature = np.array([1.0, 2.0, 1.0, 2.0])
    second_signature = np.array([2.0, 1.0, 2.0, 1.0])
    distance_matrix = np.array(
        [
            [0.0, 1.0, 1.0, 2.0],
            [1.0, 0.0, 2.0, 1.0],
            [1.0, 2.0, 0.0, 1.0],
            [2.0, 1.0, 1.0, 0.0],
        ]
    )
    emd_assert(emd(first_signature, second_signature, distance_matrix), 2.0)


def test_emd_extra_mass_penalty():
    first_signature = np.array([0.0, 2.0, 1.0, 2.0])
    second_signature = np.array([2.0, 1.0, 2.0, 1.0])
    distance_matrix = np.array(
        [
            [0.0, 1.0, 1.0, 2.0],
            [1.0, 0.0, 2.0, 1.0],
            [1.0, 2.0, 0.0, 1.0],
            [2.0, 1.0, 1.0, 0.0],
        ]
    )
    emd_assert(
        emd(first_signature, second_signature, distance_matrix, extra_mass_penalty=2.5),
        4.5,
    )


# Validation


def test_emd_validate_larger_signatures_1():
    first_signature = np.array([0.0, 1.0, 2.0])
    second_signature = np.array([5.0, 3.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5], [0.5, 0.0]])
    with pytest.raises(ValueError):
        emd(first_signature, second_signature, distance_matrix)


def test_emd_validate_larger_signatures_2():
    first_signature = np.array([0.0, 1.0, 2.0])
    second_signature = np.array([5.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5], [0.5, 0.0]])
    with pytest.raises(ValueError):
        emd_with_flow(first_signature, second_signature, distance_matrix)


def test_emd_validate_larger_signatures_3():
    first_signature = np.array([0.0, 1.0])
    second_signature = np.array([5.0, 3.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5], [0.5, 0.0]])
    with pytest.raises(ValueError):
        emd(first_signature, second_signature, distance_matrix)


def test_emd_validate_different_signature_dims():
    first_signature = np.array([0.0, 1.0])
    second_signature = np.array([5.0, 3.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5, 0.0], [0.5, 0.0, 0.0], [0.5, 0.0, 0.0]])
    with pytest.raises(ValueError):
        emd(first_signature, second_signature, distance_matrix)


def test_emd_validate_symmetric_distance_matrix():
    first_signature = np.array([0.0, 1.0])
    second_signature = np.array([5.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5, 3.0], [0.5, 0.0]], dtype=object)
    with pytest.raises(ValueError):
        emd(first_signature, second_signature, distance_matrix)


# `emd_with_flow()`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def test_emd_with_flow_1():
    first_signature = np.array([0.0, 1.0])
    second_signature = np.array([5.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5], [0.5, 0.0]])
    emd_flow_assert(
        emd_with_flow(first_signature, second_signature, distance_matrix),
        (3.5, [[0.0, 0.0], [0.0, 1.0]]),
    )


def test_emd_with_flow_2():
    first_signature = np.array([1.0, 1.0])
    second_signature = np.array([1.0, 1.0])
    distance_matrix = np.array([[0.0, 1.0], [1.0, 0.0]])
    emd_flow_assert(
        emd_with_flow(first_signature, second_signature, distance_matrix),
        (0.0, [[1.0, 0.0], [0.0, 1.0]]),
    )


def test_emd_with_flow_3():
    first_signature = np.array([6.0, 1.0])
    second_signature = np.array([1.0, 7.0])
    distance_matrix = np.array([[0.0, 0.0], [0.0, 0.0]])
    emd_flow_assert(
        emd_with_flow(first_signature, second_signature, distance_matrix),
        (0.0, [[1.0, 5.0], [0.0, 1.0]]),
    )


def test_emd_with_flow_4():
    first_signature = np.array([1.0, 7.0])
    second_signature = np.array([6.0, 1.0])
    distance_matrix = np.array([[0.0, 0.0], [0.0, 0.0]])
    emd_flow_assert(
        emd_with_flow(first_signature, second_signature, distance_matrix),
        (0.0, [[1.0, 0.0], [5.0, 1.0]]),
    )


def test_emd_with_flow_5():
    first_signature = np.array([3.0, 5.0])
    second_signature = np.array([6.0, 2.0])
    distance_matrix = np.array([[0.0, 0.0], [0.0, 0.0]])
    emd_flow_assert(
        emd_with_flow(first_signature, second_signature, distance_matrix),
        (0.0, [[3.0, 0.0], [3.0, 2.0]]),
    )


def test_emd_with_flow_6():
    first_signature = np.array([1.0, 2.0, 1.0, 2.0])
    second_signature = np.array([2.0, 1.0, 2.0, 1.0])
    distance_matrix = np.array(
        [
            [0.0, 1.0, 1.0, 2.0],
            [1.0, 0.0, 2.0, 1.0],
            [1.0, 2.0, 0.0, 1.0],
            [2.0, 1.0, 1.0, 0.0],
        ]
    )
    emd_flow_assert(
        emd_with_flow(first_signature, second_signature, distance_matrix),
        (
            2.0,
            [
                [1.0, 0.0, 0.0, 0.0],
                [1.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0, 1.0],
            ],
        ),
    )


def test_emd_with_flow_extra_mass_penalty():
    first_signature = np.array([0.0, 2.0, 1.0, 2.0])
    second_signature = np.array([2.0, 1.0, 2.0, 1.0])
    distance_matrix = np.array(
        [
            [0.0, 1.0, 1.0, 2.0],
            [1.0, 0.0, 2.0, 1.0],
            [1.0, 2.0, 0.0, 1.0],
            [2.0, 1.0, 1.0, 0.0],
        ]
    )
    emd_flow_assert(
        emd_with_flow(
            first_signature, second_signature, distance_matrix, extra_mass_penalty=2.5
        ),
        (
            4.5,
            [
                [0.0, 0.0, 0.0, 0.0],
                [1.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0, 1.0],
            ],
        ),
    )


# Validation


def test_emd_with_flow_validate_larger_signatures_1():
    first_signature = np.array([0.0, 1.0, 2.0])
    second_signature = np.array([5.0, 3.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5], [0.5, 0.0]])
    with pytest.raises(ValueError):
        emd_with_flow(first_signature, second_signature, distance_matrix)


def test_emd_with_flow_validate_larger_signatures_2():
    first_signature = np.array([0.0, 1.0, 2.0])
    second_signature = np.array([5.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5], [0.5, 0.0]])
    with pytest.raises(ValueError):
        emd(first_signature, second_signature, distance_matrix)


def test_emd_with_flow_validate_larger_signatures_3():
    first_signature = np.array([0.0, 1.0])
    second_signature = np.array([5.0, 3.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5], [0.5, 0.0]])
    with pytest.raises(ValueError):
        emd_with_flow(first_signature, second_signature, distance_matrix)


def test_emd_with_flow_validate_different_signature_dims():
    first_signature = np.array([0.0, 1.0])
    second_signature = np.array([5.0, 3.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5, 0.0], [0.5, 0.0, 0.0], [0.5, 0.0, 0.0]])
    with pytest.raises(ValueError):
        emd_with_flow(first_signature, second_signature, distance_matrix)


def test_emd_with_flow_validate_square_distance_matrix():
    first_signature = np.array([0.0, 1.0])
    second_signature = np.array([5.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5, 3.0], [0.5, 0.0]], dtype=object)
    with pytest.raises(ValueError):
        emd_with_flow(first_signature, second_signature, distance_matrix)


# `emd_samples()`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def test_emd_samples_1():
    first_array = [1, 2, 3, 4]
    second_array = [2, 3, 4, 5]
    emd_assert(emd_samples(first_array, second_array, bins=4), 0.75)


def test_emd_samples_1_binsize():
    first_array = [1, 2, 3, 4]
    second_array = [2, 3, 4, 5]
    emd_assert(emd_samples(first_array, second_array, bins=2), 0.5)


def test_emd_samples_1_manual_range():
    first_array = [1, 2, 3, 4]
    second_array = [2, 3, 4, 5]
    emd_assert(emd_samples(first_array, second_array, bins=10, range=(0, 10)), 1.0)


def test_emd_samples_1_not_normalized():
    first_array = [1, 2, 3, 4]
    second_array = [2, 3, 4, 5]
    emd_assert(emd_samples(first_array, second_array, bins=4, normalized=False), 3.0)


def test_emd_samples_1_custom_distance():
    def dist(x):
        return np.array([[0.0 if i == j else 1.0 for i in x] for j in x])

    first_array = [1, 2, 3, 4]
    second_array = [2, 3, 4, 5]
    emd_assert(emd_samples(first_array, second_array, bins=4, distance=dist), 0.25)


def test_emd_samples_all_kwargs():
    # Regression only; not checked by hand
    def dist(x):
        return [[(i - j) ** 3 for i in range(len(x))] for j in range(len(x))]

    first_array = [1, 2, 3, 4, 5]
    second_array = [2, 3, 4, 5]
    emd_assert(
        emd_samples(
            first_array,
            second_array,
            bins=30,
            normalized=False,
            range=(-5, 15),
            distance=dist,
        ),
        24389.0,
    )


def test_emd_samples_2():
    first_array = [1]
    second_array = [2]
    # Use explicit bins=2 since bins='auto' gives only 1 bin for this small dataset
    emd_assert(emd_samples(first_array, second_array, bins=2), 0.5)


def test_emd_samples_3():
    first_array = [1, 1, 1, 2, 3]
    second_array = [1, 2, 2, 2, 3]
    # Use explicit bins=5 since bins='auto' behavior varies across NumPy versions
    emd_assert(emd_samples(first_array, second_array, bins=5), 0.32)


def test_emd_samples_4():
    first_array = [1, 2, 3, 4, 5]
    second_array = [99, 98, 97, 96, 95]
    emd_assert(emd_samples(first_array, second_array, bins=5), 78.4)


def test_emd_samples_5():
    first_array = [1]
    second_array = [1, 2, 3, 4, 5]
    emd_assert(emd_samples(first_array, second_array, bins=4), 1.8)


# bins='auto' with integer inputs (regression tests for GitHub issue #68)
# NumPy 2.1+ enforces bin width >= 1 for integer dtypes, which can cause
# too few bins. The fix converts to float64 before computing bin edges.


def test_emd_samples_auto_bins_integer_input():
    """bins='auto' should produce nonzero EMD for distinct integer samples."""
    first_array = [1]
    second_array = [2]
    # Without the fix, this returns 0.0 (only 1 bin, so histograms are identical)
    result = emd_samples(first_array, second_array)
    assert result > 0, f"EMD should be nonzero for distinct samples, got {result}"


def test_emd_samples_auto_bins_integer_vs_float_consistency():
    """bins='auto' should give same result for integer and float inputs."""
    int_result = emd_samples([1, 2, 3], [4, 5, 6])
    float_result = emd_samples([1.0, 2.0, 3.0], [4.0, 5.0, 6.0])
    assert abs(int_result - float_result) < 1e-10, (
        f"Integer and float inputs should give same EMD: {int_result} vs {float_result}"
    )


# Validation


def test_emd_samples_validate_empty():
    first_array = []
    second_array = [1]
    with pytest.raises(ValueError):
        emd_samples(first_array, second_array)


def test_emd_samples_validate_distance_matrix_square():
    def dist(x):
        return [[1, 2, 3]]

    first_array = [1, 2, 3]
    second_array = [1, 2, 3]
    with pytest.raises(ValueError):
        emd_samples(first_array, second_array, distance=dist)


def test_emd_samples_validate_distance_matrix_size():
    def dist(x):
        return [[0, 1], [1, 0]]

    first_array = [1, 2, 3, 4]
    second_array = [1, 2, 3, 4]
    with pytest.raises(ValueError):
        emd_samples(first_array, second_array, distance=dist)


# Backend tests
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@pytest.fixture
def balanced_inputs():
    """Balanced histograms (same sum) for testing."""
    first = np.array([0.25, 0.25, 0.25, 0.25])
    second = np.array([0.1, 0.2, 0.3, 0.4])
    dist = np.array([
        [0.0, 1.0, 2.0, 3.0],
        [1.0, 0.0, 1.0, 2.0],
        [2.0, 1.0, 0.0, 1.0],
        [3.0, 2.0, 1.0, 0.0],
    ])
    return first, second, dist


@pytest.fixture
def unbalanced_inputs():
    """Unbalanced histograms (different sums) for testing."""
    first = np.array([0.0, 2.0, 1.0, 2.0])
    second = np.array([2.0, 1.0, 2.0, 1.0])
    dist = np.array([
        [0.0, 1.0, 1.0, 2.0],
        [1.0, 0.0, 2.0, 1.0],
        [1.0, 2.0, 0.0, 1.0],
        [2.0, 1.0, 1.0, 0.0],
    ])
    return first, second, dist


# Test backend parameter


def test_emd_backend_pot(balanced_inputs):
    """Test emd() with POT backend."""
    first, second, dist = balanced_inputs
    result = emd(first, second, dist, backend='pot')
    assert isinstance(result, float)
    assert result >= 0


def test_emd_backend_cpp(balanced_inputs):
    """Test emd() with C++ backend."""
    first, second, dist = balanced_inputs
    result = emd(first, second, dist, backend='cpp')
    assert isinstance(result, float)
    assert result >= 0


def test_emd_with_flow_backend_pot(balanced_inputs):
    """Test emd_with_flow() with POT backend."""
    first, second, dist = balanced_inputs
    result, flow = emd_with_flow(first, second, dist, backend='pot')
    assert isinstance(result, float)
    assert result >= 0
    assert len(flow) == len(first)


def test_emd_with_flow_backend_cpp(balanced_inputs):
    """Test emd_with_flow() with C++ backend."""
    first, second, dist = balanced_inputs
    result, flow = emd_with_flow(first, second, dist, backend='cpp')
    assert isinstance(result, float)
    assert result >= 0
    assert len(flow) == len(first)


def test_emd_samples_backend_pot():
    """Test emd_samples() with POT backend."""
    first = [1, 2, 3, 4]
    second = [2, 3, 4, 5]
    result = emd_samples(first, second, bins=4, backend='pot')
    assert isinstance(result, float)
    assert result >= 0


def test_emd_samples_backend_cpp():
    """Test emd_samples() with C++ backend."""
    first = [1, 2, 3, 4]
    second = [2, 3, 4, 5]
    result = emd_samples(first, second, bins=4, backend='cpp')
    assert isinstance(result, float)
    assert result >= 0


def test_emd_invalid_backend(balanced_inputs):
    """Test that invalid backend raises ValueError."""
    first, second, dist = balanced_inputs
    with pytest.raises(ValueError):
        emd(first, second, dist, backend='invalid')


def test_emd_with_flow_invalid_backend(balanced_inputs):
    """Test that invalid backend raises ValueError for emd_with_flow."""
    first, second, dist = balanced_inputs
    with pytest.raises(ValueError):
        emd_with_flow(first, second, dist, backend='invalid')


def test_emd_samples_invalid_backend():
    """Test that invalid backend raises ValueError for emd_samples."""
    with pytest.raises(ValueError):
        emd_samples([1, 2], [3, 4], backend='invalid')


# Backend equivalence tests


def test_emd_backend_equivalence_balanced(balanced_inputs):
    """Test that POT and C++ backends give same result for balanced histograms."""
    first, second, dist = balanced_inputs
    result_pot = emd(first, second, dist, backend='pot')
    result_cpp = emd(first, second, dist, backend='cpp')
    assert abs(result_pot - result_cpp) < 1e-6, (
        f"POT ({result_pot}) and C++ ({result_cpp}) should give same result"
    )


def test_emd_backend_equivalence_unbalanced(unbalanced_inputs):
    """Test that POT and C++ backends give same result for unbalanced histograms."""
    first, second, dist = unbalanced_inputs
    result_pot = emd(first, second, dist, backend='pot')
    result_cpp = emd(first, second, dist, backend='cpp')
    assert abs(result_pot - result_cpp) < 1e-5, (
        f"POT ({result_pot}) and C++ ({result_cpp}) should give same result"
    )


def test_emd_backend_equivalence_extra_mass_penalty(unbalanced_inputs):
    """Test equivalence with custom extra_mass_penalty."""
    first, second, dist = unbalanced_inputs
    result_pot = emd(first, second, dist, extra_mass_penalty=2.5, backend='pot')
    result_cpp = emd(first, second, dist, extra_mass_penalty=2.5, backend='cpp')
    assert abs(result_pot - result_cpp) < 1e-5, (
        f"POT ({result_pot}) and C++ ({result_cpp}) should give same result with extra_mass_penalty"
    )


def test_emd_with_flow_backend_equivalence_cost(balanced_inputs):
    """Test that POT and C++ backends give same EMD cost for emd_with_flow."""
    first, second, dist = balanced_inputs
    cost_pot, _ = emd_with_flow(first, second, dist, backend='pot')
    cost_cpp, _ = emd_with_flow(first, second, dist, backend='cpp')
    assert abs(cost_pot - cost_cpp) < 1e-6, (
        f"POT ({cost_pot}) and C++ ({cost_cpp}) should give same cost"
    )


def test_emd_samples_backend_equivalence():
    """Test that POT and C++ backends give same result for emd_samples."""
    first = [1, 2, 3, 4, 5]
    second = [2, 3, 4, 5, 6]
    result_pot = emd_samples(first, second, bins=5, backend='pot')
    result_cpp = emd_samples(first, second, bins=5, backend='cpp')
    assert abs(result_pot - result_cpp) < 1e-6, (
        f"POT ({result_pot}) and C++ ({result_cpp}) should give same result"
    )
