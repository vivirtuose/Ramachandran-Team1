# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 18:14:32 2020

@author: ebecker
"""
from math import sqrt 
from math import acos

class Atom:
    def __init__(self, name, px = 0.00, py = 0.00, pz = 0.00):
      self._name = name
      self._x = px
      self._y = py  
      self._z = pz
    
    @property
    def name(self):
      """
      Function that returns the name of the atom as a string
      """
      return self._name
    
    @name.setter
    def name(self, pname):
        """
        Function that modifies the name
        """
        self._name = pname
    
    @property
    def coords(self):
        """
        Function that returns a list containing the coordinates (x,y,z)
        """
        return [self._x,self._y,self._z]   
     
    @coords.setter
    def coords(self, values):
        """
        Function that modifies the attributes x, y, z
        """
        self._x,self._y,self._z = values


    @property  
    def x(self):
        """
        Function that returns the x coordinate
        """
        return self._x
    
    @x.setter
    def x(self,px):
        """
        Function that modifies the x coordinate
        """
        self._x=px
        
    @property
    def y(self):
        """
        Function that returns the y coordinate
        """
        return self._y
    
    @y.setter
    def y(self,py):
       """
        Function that modifies the y coordinate
        """
       self._y=py
    
    @property
    def z(self):
        """
        Function that returns the z coordinate
        """
        return(self._z)
    
    @z.setter
    def z(self,pz):
        """
        Function that modifies the z coordinate
        """
        self._z=pz


    def copy(self, another_atom):
        """
        Function that copies the values of the current instance in a new atom passed as a parameter
        """
        another_atom.name=self.name
        another_atom.coords = self.coords
        return another_atom    
  
    def __str__(self):
      return f"{self.name} ({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"
    
    
    def norm(self):
      """
      Function that computes the norm of the vector from O to the current instance
      """
      current_coord=self.coords
      norm = sqrt((current_coord[0])**2+(current_coord[1])**2+(current_coord[2])**2)
      return norm
    
    
    def distance(self, another_atom):
        """
        Function that computes the distance between the current instance and another atom
        """
        current_coord=self.coords
        other_coord=another_atom.coords
        norm = sqrt((current_coord[0]-other_coord[0])**2+(current_coord[1]-other_coord[1])**2+(current_coord[2]-other_coord[2])**2)
        return norm

    def substract(self, another_atom):
        """
        Function that computes the substraction between the current atom and the other atom passed as a parameter, and returns it as a new Atom with an empty name.
        """

    
    def dot_product(self, another_atom):
        """
        Function that computes the dot product between the current atom and the other atom passed as a parameter, and returns it as a float
        """
        A1_coords = self.coords
        A2_coords = another_atom.coords
        res=float(A1_coords[0]*A2_coords[0]+A1_coords[1]*A2_coords[1]+A1_coords[2]*A2_coords[2])
        return res

    def cross_product(self, another_atom):
        """
        Function that computes the cross product between the current atom and the other atom passed as a parameter, and returns it as a new Atom with an empty name.
        """
      
      
    def angle(self, another_atom):
        return(self.dot_product(another_atom)/(self.norm()*another_atom.norm()))
    

    def dihedral(a1, a2, a3, a4):
        """
        Function that computes dihedral angle (torsion angle) between 4 atoms named a1 to a4
        """

if __name__ == "__main__":	
  print("Testing Class Atom")
  atom1 = Atom("H",18.0,9.5,192.5)
  atom2 = Atom("C",18.0,9.5,0)
  atom3 = Atom("O",0,0,1)
    
  print(atom1)
  print(atom2)
  print(atom3)
