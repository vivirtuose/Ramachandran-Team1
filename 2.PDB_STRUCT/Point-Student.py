# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 17:07:20 2020

@author: ebecker
"""
from math import sqrt

class Point:
  def __init__(self, x = 0.00, y = 0.00):
    self.abs = x 
    self.ord = x 


  def __str__(self):
    s = "Point of coordinates ({:.4f}, {:.4f})".format(self.get_abs(), self.get_abs())
    return(s)
	
  def get_abs(self):

	
  def get_ord(self):


  def add(self, another_point):
    """
    Functions that adds to the current Point to another point passed as an argument
    """


  def rescale(self, factor):
    """
    Functions that rescales the current Point by a scalar passed as an argument
    """


  def distance_from_origin(self):	
    """
    Functions that computes the distance of the current Point to the origin of the plan O
    """


  def euclidean_distance(self, another_point):
    """
    Functions that computes the euclidean distance of the current Point with another point passed as an argument
    """

  def manhattan_distance(self, another_point):
    """
    Functions that computes the manhattan distance of the current Point with another point passed as an argument
    """



if __name__ == "__main__":	
  pA = Point(0,0)
  pB = Point(1,1)
  pC = Point(2,1)
  pD = Point(3,4)

  print(pA)
  print(pB)
  print(pC)
  print(pD)

  pA.add(pB)
  assert pA.get_abs() == 1, 'Error in Point.add'
  pA.rescale(5)
  assert pA.get_abs() == 5, 'Error in Point.rescale'
  assert pD.distance_from_origin() == 5, 'Error in Point.distance_from_origin'
  assert pB.distance(pC) == 1, 'Error in Point.distance'
