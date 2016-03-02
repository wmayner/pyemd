#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from pyemd import emd
from unittest import TestCase, main

class TestEMD(TestCase):

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

class TestInputValidation(TestCase):
    
    def test_larger_signatures(self):
      first_signature = np.array([0.0, 1.0,2.0])
      second_signature = np.array([5.0, 3.0,3.0])
      distance_matrix = np.array([[0.0, 0.5],
                                [0.5, 0.0]])
      
      self.assertRaises(ValueError,\
                      emd,first_signature, second_signature, distance_matrix)

    def test_larger_signatures_1(self):
      first_signature = np.array([0.0, 1.0,2.0])
      second_signature = np.array([5.0, 3.0])
      distance_matrix = np.array([[0.0, 0.5],
                                [0.5, 0.0]])
      
      self.assertRaises(ValueError,\
                      emd,first_signature, second_signature, distance_matrix)

    def test_larger_signatures_2(self):
      first_signature = np.array([0.0, 1.0])
      second_signature = np.array([5.0, 3.0,3.0])
      distance_matrix = np.array([[0.0, 0.5],
                                [0.5, 0.0]])
      
      self.assertRaises(ValueError,\
                      emd,first_signature, second_signature, distance_matrix)
    
    def test_different_signature_dims(self):
      first_signature = np.array([0.0, 1.0])
      second_signature = np.array([5.0, 3.0,3.0])
      distance_matrix = np.array([[0.0, 0.5,0.0],
                                [0.5, 0.0,0.0],
                                [0.5, 0.0,0.0]])

      
      assert 3.5 == emd(first_signature, second_signature, distance_matrix)
    
    def test_symmetric_distance_matrix(self):
      first_signature = np.array([0.0, 1.0])
      second_signature = np.array([5.0, 3.0])
      distance_matrix = np.array([[0.0, 0.5,3.0],
                                [0.5, 0.0]])

    
      self.assertRaises(ValueError,\
                      emd,first_signature, second_signature, distance_matrix)

if __name__ == '__main__':
  main()
