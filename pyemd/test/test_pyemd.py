#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import numpy as np
from pyemd import emd


class TestEmd(unittest.TestCase):

    def test_case_1(self):
        first_signature = np.array([0.0, 1.0])
        second_signature = np.array([5.0, 3.0])
        distance_matrix = np.array([[0.0, 0.5],
                                   [0.5, 0.0]])
        assert 3.5 == emd(first_signature, second_signature, distance_matrix)

    def test_case_2(self):
        first_signature = np.array([1.0, 1.0])
        second_signature = np.array([1.0, 1.0])
        distance_matrix = np.array([[0.0, 1.0],
                                   [1.0, 0.0]])
        assert 0.0 == emd(first_signature, second_signature, distance_matrix)

    def test_case_3(self):
        first_signature = np.array([6.0, 1.0])
        second_signature = np.array([1.0, 7.0])
        distance_matrix = np.array([[0.0, 0.0],
                                   [0.0, 0.0]])
        assert 0.0 == emd(first_signature, second_signature, distance_matrix)

    def test_error_different_signature_lengths(self):
        first_signature = np.array([6.0, 1.0, 9.0])
        second_signature = np.array([1.0, 7.0])
        distance_matrix = np.array([[0.0, 1.0],
                                    [1.0, 0.0]])
        with self.assertRaises(ValueError):
            emd(first_signature, second_signature, distance_matrix)

    def test_error_wrong_distance_matrix_shape(self):
        first_signature = np.array([6.0, 1.0])
        second_signature = np.array([1.0, 7.0])
        distance_matrix = np.array([[0.0, 1.0, 0.4],
                                    [1.0, 0.0]])
        with self.assertRaises(ValueError):
            emd(first_signature, second_signature, distance_matrix)

    def test_error_wrong_signature_ndim(self):
        first_signature = np.array([[6.0, 1.0]])
        second_signature = np.array([1.0, 7.0])
        distance_matrix = np.array([[0.0, 1.0],
                                    [1.0, 0.0]])
        with self.assertRaises(ValueError):
            emd(first_signature, second_signature, distance_matrix)

    def test_error_wrong_distance_matrix_ndim(self):
        first_signature = np.array([6.0, 1.0])
        second_signature = np.array([1.0, 7.0])
        distance_matrix = np.array([[[0.0, 1.0],
                                    [1.0, 0.0]]])
        with self.assertRaises(ValueError):
            emd(first_signature, second_signature, distance_matrix)
