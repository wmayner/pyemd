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


# `emd()` and `emd_with_flow()` testing
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_case_1():
    first_signature = np.array([0.0, 1.0])
    second_signature = np.array([5.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5],
                                [0.5, 0.0]])
    emd_assert(
        emd(first_signature, second_signature, distance_matrix),
        3.5
    )

def test_case_1_flow():
    first_signature = np.array([0.0, 1.0])
    second_signature = np.array([5.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5],
                                [0.5, 0.0]])
    emd_flow_assert(
        emd_with_flow(first_signature, second_signature, distance_matrix),
        (3.5, [[0.0, 0.0],
               [0.0, 1.0]])
    )


def test_case_2():
    first_signature = np.array([1.0, 1.0])
    second_signature = np.array([1.0, 1.0])
    distance_matrix = np.array([[0.0, 1.0],
                                [1.0, 0.0]])
    emd_assert(
        emd(first_signature, second_signature, distance_matrix),
        0.0
    )


def test_case_2_flow():
    first_signature = np.array([1.0, 1.0])
    second_signature = np.array([1.0, 1.0])
    distance_matrix = np.array([[0.0, 1.0],
                                [1.0, 0.0]])

    emd_flow_assert(
        emd_with_flow(first_signature, second_signature, distance_matrix),
        (0.0, [[1.0, 0.0],
               [0.0, 1.0]])
    )


def test_case_3():
    first_signature = np.array([6.0, 1.0])
    second_signature = np.array([1.0, 7.0])
    distance_matrix = np.array([[0.0, 0.0],
                                [0.0, 0.0]])
    emd_assert(
        emd(first_signature, second_signature, distance_matrix),
        0.0
    )


def test_case_3_flow():
    first_signature = np.array([6.0, 1.0])
    second_signature = np.array([1.0, 7.0])
    distance_matrix = np.array([[0.0, 0.0],
                                [0.0, 0.0]])
    emd_flow_assert(
        emd_with_flow(first_signature, second_signature, distance_matrix),
        (0.0, [[1.0, 5.0],
               [0.0, 1.0]])
    )


def test_case_4_flow():
    first_signature = np.array([1.0, 7.0])
    second_signature = np.array([6.0, 1.0])
    distance_matrix = np.array([[0.0, 0.0],
                                [0.0, 0.0]])
    emd_flow_assert(
        emd_with_flow(first_signature, second_signature, distance_matrix),
        (0.0, [[1.0, 0.0],
               [5.0, 1.0]])
    )


def test_case_5_flow():
    first_signature = np.array([3.0, 5.0])
    second_signature = np.array([6.0, 2.0])
    distance_matrix = np.array([[0.0, 0.0],
                                [0.0, 0.0]])
    emd_flow_assert(
        emd_with_flow(first_signature, second_signature, distance_matrix),
        (0.0, [[3.0, 0.0],
               [3.0, 2.0]])
    )


def test_case_6():
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


def test_case_6_flow():
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


def test_extra_mass_penalty():
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


def test_extra_mass_penalty_flow():
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


# `emd_samples()` testing
# ~~~~~~~~~~~~~~~~~~~~~


def test_case_samples_1():
    first_array = [1, 2, 3, 4]
    second_array = [2, 3, 4, 5]
    emd_assert(emd_samples(first_array, second_array), 0.75)


def test_case_samples_1_binsize():
    first_array = [1, 2, 3, 4]
    second_array = [2, 3, 4, 5]
    emd_assert(emd_samples(first_array, second_array, bins=2), 0.5)


def test_case_samples_1_manual_range():
    first_array = [1, 2, 3, 4]
    second_array = [2, 3, 4, 5]
    emd_assert(emd_samples(first_array, second_array, range=(0, 10)), 1.0)


def test_case_samples_1_not_normalized():
    first_array = [1, 2, 3, 4]
    second_array = [2, 3, 4, 5]
    emd_assert(emd_samples(first_array, second_array, normalized=False), 3.0)


def test_case_samples_1_custom_distance():
    dist = lambda x: np.array([[0.0 if i == j else 1.0 for i in x] for j in x])
    first_array = [1, 2, 3, 4]
    second_array = [2, 3, 4, 5]
    emd_assert(emd_samples(first_array, second_array, distance=dist), 0.25)


def test_case_samples_2():
    first_array = [1]
    second_array = [2]
    emd_assert(emd_samples(first_array, second_array), 0.5)


def test_case_samples_3():
    first_array = [1, 1, 1, 2, 3]
    second_array = [1, 2, 2, 2, 3]
    emd_assert(emd_samples(first_array, second_array), 0.32)


def test_case_samples_4():
    first_array = [1, 2, 3, 4, 5]
    second_array = [99, 98, 97, 96, 95]
    emd_assert(emd_samples(first_array, second_array), 78.4)


# Validation testing
# ~~~~~~~~~~~~~~~~~~


def test_larger_signatures():
    first_signature = np.array([0.0, 1.0, 2.0])
    second_signature = np.array([5.0, 3.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5],
                                [0.5, 0.0]])
    with pytest.raises(ValueError):
        emd(first_signature, second_signature, distance_matrix)


def test_larger_signatures_flow():
    first_signature = np.array([0.0, 1.0, 2.0])
    second_signature = np.array([5.0, 3.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5],
                                [0.5, 0.0]])
    with pytest.raises(ValueError):
        emd_with_flow(first_signature, second_signature, distance_matrix)


def test_larger_signatures_1():
    first_signature = np.array([0.0, 1.0, 2.0])
    second_signature = np.array([5.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5],
                                [0.5, 0.0]])
    with pytest.raises(ValueError):
        emd_with_flow(first_signature, second_signature, distance_matrix)


def test_larger_signatures_1_flow():
    first_signature = np.array([0.0, 1.0, 2.0])
    second_signature = np.array([5.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5],
                                [0.5, 0.0]])
    with pytest.raises(ValueError):
        emd(first_signature, second_signature, distance_matrix)


def test_larger_signatures_2():
    first_signature = np.array([0.0, 1.0])
    second_signature = np.array([5.0, 3.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5], [0.5, 0.0]])
    with pytest.raises(ValueError):
        emd(first_signature, second_signature, distance_matrix)


def test_larger_signatures_2_flow():
    first_signature = np.array([0.0, 1.0])
    second_signature = np.array([5.0, 3.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5],
                                [0.5, 0.0]])
    with pytest.raises(ValueError):
        emd_with_flow(first_signature, second_signature, distance_matrix)


def test_different_signature_dims():
    first_signature = np.array([0.0, 1.0])
    second_signature = np.array([5.0, 3.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5, 0.0],
                                [0.5, 0.0, 0.0],
                                [0.5, 0.0, 0.0]])
    with pytest.raises(ValueError):
        emd(first_signature, second_signature, distance_matrix)


def test_different_signature_dims_flow():
    first_signature = np.array([0.0, 1.0])
    second_signature = np.array([5.0, 3.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5, 0.0],
                                [0.5, 0.0, 0.0],
                                [0.5, 0.0, 0.0]])
    with pytest.raises(ValueError):
        emd_with_flow(first_signature, second_signature, distance_matrix)


def test_symmetric_distance_matrix():
    first_signature = np.array([0.0, 1.0])
    second_signature = np.array([5.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5, 3.0],
                                [0.5, 0.0]])
    with pytest.raises(ValueError):
        emd(first_signature, second_signature, distance_matrix)


def test_symmetric_distance_matrix_flow():
    first_signature = np.array([0.0, 1.0])
    second_signature = np.array([5.0, 3.0])
    distance_matrix = np.array([[0.0, 0.5, 3.0],
                                [0.5, 0.0]])
    with pytest.raises(ValueError):
        emd_with_flow(first_signature, second_signature, distance_matrix)
