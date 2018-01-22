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
    distance_matrix = np.array([[0.0, 0.5],
                                [0.5, 0.0]])
    emd_assert(
        emd(first_signature, second_signature, distance_matrix),
        3.5
    )


def test_emd_2():
    first_signature = np.array([1.0, 1.0])
    second_signature = np.array([1.0, 1.0])
    distance_matrix = np.array([[0.0, 1.0],
                                [1.0, 0.0]])
    emd_assert(
        emd(first_signature, second_signature, distance_matrix),
        0.0
    )


def test_emd_3():
    first_signature = np.array([6.0, 1.0])
    second_signature = np.array([1.0, 7.0])
    distance_matrix = np.array([[0.0, 0.0],
                                [0.0, 0.0]])
    emd_assert(
        emd(first_signature, second_signature, distance_matrix),
        0.0
    )


def test_emd_4():
    first_signature = np.array([1.0, 2.0, 1.0, 2.0])
    second_signature = np.array([2.0, 1.0, 2.0, 1.0])
    distance_matrix = np.array([[0.0, 1.0, 1.0, 2.0],
                                [1.0, 0.0, 2.0, 1.0],
                                [1.0, 2.0, 0.0, 1.0],
                                [2.0, 1.0, 1.0, 0.0]])
    emd_assert(
        emd(first_signature, second_signature, distance_matrix),
        2.0
    )


def test_emd_extra_mass_penalty():
    first_signature = np.array([0.0, 2.0, 1.0, 2.0])
    second_signature = np.array([2.0, 1.0, 2.0, 1.0])
    distance_matrix = np.array([[0.0, 1.0, 1.0, 2.0],
                                [1.0, 0.0, 2.0, 1.0],
                                [1.0, 2.0, 0.0, 1.0],
                                [2.0, 1.0, 1.0, 0.0]])
    emd_assert(
        emd(first_signature, second_signature, distance_matrix,
            extra_mass_penalty=2.5),
        4.5
    )


# Validation


def test_emd_validate_larger_signatures_1():
    first_signature = np.array([0.0, 1.0, 2.0])
    second_signature = np.array([5.0, 3.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5],
                                [0.5, 0.0]])
    with pytest.raises(ValueError):
        emd(first_signature, second_signature, distance_matrix)


def test_emd_validate_larger_signatures_2():
    first_signature = np.array([0.0, 1.0, 2.0])
    second_signature = np.array([5.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5],
                                [0.5, 0.0]])
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
    distance_matrix = np.array([[0.0, 0.5, 0.0],
                                [0.5, 0.0, 0.0],
                                [0.5, 0.0, 0.0]])
    with pytest.raises(ValueError):
        emd(first_signature, second_signature, distance_matrix)


def test_emd_validate_symmetric_distance_matrix():
    first_signature = np.array([0.0, 1.0])
    second_signature = np.array([5.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5, 3.0],
                                [0.5, 0.0]])
    with pytest.raises(ValueError):
        emd(first_signature, second_signature, distance_matrix)


# `emd_with_flow()`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def test_emd_with_flow_1():
    first_signature = np.array([0.0, 1.0])
    second_signature = np.array([5.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5],
                                [0.5, 0.0]])
    emd_flow_assert(
        emd_with_flow(first_signature, second_signature, distance_matrix),
        (3.5, [[0.0, 0.0],
               [0.0, 1.0]])
    )


def test_emd_with_flow_2():
    first_signature = np.array([1.0, 1.0])
    second_signature = np.array([1.0, 1.0])
    distance_matrix = np.array([[0.0, 1.0],
                                [1.0, 0.0]])
    emd_flow_assert(
        emd_with_flow(first_signature, second_signature, distance_matrix),
        (0.0, [[1.0, 0.0],
               [0.0, 1.0]])
    )


def test_emd_with_flow_3():
    first_signature = np.array([6.0, 1.0])
    second_signature = np.array([1.0, 7.0])
    distance_matrix = np.array([[0.0, 0.0],
                                [0.0, 0.0]])
    emd_flow_assert(
        emd_with_flow(first_signature, second_signature, distance_matrix),
        (0.0, [[1.0, 5.0],
               [0.0, 1.0]])
    )


def test_emd_with_flow_4():
    first_signature = np.array([1.0, 7.0])
    second_signature = np.array([6.0, 1.0])
    distance_matrix = np.array([[0.0, 0.0],
                                [0.0, 0.0]])
    emd_flow_assert(
        emd_with_flow(first_signature, second_signature, distance_matrix),
        (0.0, [[1.0, 0.0],
               [5.0, 1.0]])
    )


def test_emd_with_flow_5():
    first_signature = np.array([3.0, 5.0])
    second_signature = np.array([6.0, 2.0])
    distance_matrix = np.array([[0.0, 0.0],
                                [0.0, 0.0]])
    emd_flow_assert(
        emd_with_flow(first_signature, second_signature, distance_matrix),
        (0.0, [[3.0, 0.0],
               [3.0, 2.0]])
    )


def test_emd_with_flow_6():
    first_signature = np.array([1.0, 2.0, 1.0, 2.0])
    second_signature = np.array([2.0, 1.0, 2.0, 1.0])
    distance_matrix = np.array([[0.0, 1.0, 1.0, 2.0],
                                [1.0, 0.0, 2.0, 1.0],
                                [1.0, 2.0, 0.0, 1.0],
                                [2.0, 1.0, 1.0, 0.0]])
    emd_flow_assert(
        emd_with_flow(first_signature, second_signature, distance_matrix),
        (2.0, [[1.0, 0.0, 0.0, 0.0],
               [1.0, 1.0, 0.0, 0.0],
               [0.0, 0.0, 1.0, 0.0],
               [0.0, 0.0, 1.0, 1.0]])
    )


def test_emd_with_flow_extra_mass_penalty():
    first_signature = np.array([0.0, 2.0, 1.0, 2.0])
    second_signature = np.array([2.0, 1.0, 2.0, 1.0])
    distance_matrix = np.array([[0.0, 1.0, 1.0, 2.0],
                                [1.0, 0.0, 2.0, 1.0],
                                [1.0, 2.0, 0.0, 1.0],
                                [2.0, 1.0, 1.0, 0.0]])
    emd_flow_assert(
        emd_with_flow(first_signature, second_signature, distance_matrix,
                      extra_mass_penalty=2.5),
        (4.5, [[0.0, 0.0, 0.0, 0.0],
               [1.0, 1.0, 0.0, 0.0],
               [0.0, 0.0, 1.0, 0.0],
               [0.0, 0.0, 1.0, 1.0]])
    )


# Validation


def test_emd_with_flow_validate_larger_signatures_1():
    first_signature = np.array([0.0, 1.0, 2.0])
    second_signature = np.array([5.0, 3.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5],
                                [0.5, 0.0]])
    with pytest.raises(ValueError):
        emd_with_flow(first_signature, second_signature, distance_matrix)


def test_emd_with_flow_validate_larger_signatures_2():
    first_signature = np.array([0.0, 1.0, 2.0])
    second_signature = np.array([5.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5],
                                [0.5, 0.0]])
    with pytest.raises(ValueError):
        emd(first_signature, second_signature, distance_matrix)


def test_emd_with_flow_validate_larger_signatures_3():
    first_signature = np.array([0.0, 1.0])
    second_signature = np.array([5.0, 3.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5],
                                [0.5, 0.0]])
    with pytest.raises(ValueError):
        emd_with_flow(first_signature, second_signature, distance_matrix)


def test_emd_with_flow_validate_different_signature_dims():
    first_signature = np.array([0.0, 1.0])
    second_signature = np.array([5.0, 3.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5, 0.0],
                                [0.5, 0.0, 0.0],
                                [0.5, 0.0, 0.0]])
    with pytest.raises(ValueError):
        emd_with_flow(first_signature, second_signature, distance_matrix)


def test_emd_with_flow_validate_square_distance_matrix():
    first_signature = np.array([0.0, 1.0])
    second_signature = np.array([5.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5, 3.0],
                                [0.5, 0.0]])
    with pytest.raises(ValueError):
        emd_with_flow(first_signature, second_signature, distance_matrix)


# `emd_samples()`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def test_emd_samples_1():
    first_array = [1, 2, 3, 4]
    second_array = [2, 3, 4, 5]
    emd_assert(emd_samples(first_array, second_array), 0.75)


def test_emd_samples_1_binsize():
    first_array = [1, 2, 3, 4]
    second_array = [2, 3, 4, 5]
    emd_assert(emd_samples(first_array, second_array, bins=2), 0.5)


def test_emd_samples_1_manual_range():
    first_array = [1, 2, 3, 4]
    second_array = [2, 3, 4, 5]
    emd_assert(emd_samples(first_array, second_array, range=(0, 10)), 1.0)


def test_emd_samples_1_not_normalized():
    first_array = [1, 2, 3, 4]
    second_array = [2, 3, 4, 5]
    emd_assert(emd_samples(first_array, second_array, normalized=False), 3.0)


def test_emd_samples_1_custom_distance():
    dist = lambda x: np.array([[0.0 if i == j else 1.0 for i in x] for j in x])
    first_array = [1, 2, 3, 4]
    second_array = [2, 3, 4, 5]
    emd_assert(emd_samples(first_array, second_array, distance=dist), 0.25)


def test_emd_samples_all_kwargs():
    # Regression only; not checked by hand
    dist = lambda x: [
        [(i - j)**3 for i in range(len(x))] for j in range(len(x))
    ]
    first_array = [1, 2, 3, 4, 5]
    second_array = [2, 3, 4, 5]
    emd_assert(
        emd_samples(first_array, second_array,
                    bins=30,
                    normalized=False,
                    range=(-5, 15),
                    distance=dist),
        24389.0
    )


def test_emd_samples_2():
    first_array = [1]
    second_array = [2]
    emd_assert(emd_samples(first_array, second_array), 0.5)


def test_emd_samples_3():
    first_array = [1, 1, 1, 2, 3]
    second_array = [1, 2, 2, 2, 3]
    emd_assert(emd_samples(first_array, second_array), 0.32)


def test_emd_samples_4():
    first_array = [1, 2, 3, 4, 5]
    second_array = [99, 98, 97, 96, 95]
    emd_assert(emd_samples(first_array, second_array), 78.4)


def test_emd_samples_5():
    first_array = [1]
    second_array = [1, 2, 3, 4, 5]
    emd_assert(emd_samples(first_array, second_array), 1.8)


# Validation


def test_emd_samples_validate_empty():
    first_array = []
    second_array = [1]
    with pytest.raises(ValueError):
        emd_samples(first_array, second_array)


def test_emd_samples_validate_distance_matrix_square():
    dist = lambda x: [[1, 2, 3]]
    first_array = [1, 2, 3]
    second_array = [1, 2, 3]
    with pytest.raises(ValueError):
        emd_samples(first_array, second_array, distance=dist)


def test_emd_samples_validate_distance_matrix_size():
    dist = lambda x: [[0, 1],
                      [1, 0]]
    first_array = [1, 2, 3, 4]
    second_array = [1, 2, 3, 4]
    with pytest.raises(ValueError):
        emd_samples(first_array, second_array, distance=dist)
