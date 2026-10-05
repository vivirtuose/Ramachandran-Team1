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
    
    @property #name
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
    
    @property #coordinate
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


    @property  #x coordinate
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

        
    @property #y coordinate
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

    
    @property #z coordinate
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
      """
      Function that return the str representation of an atom
      """
      return f"{self.name} ({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

    
    def norm(self):
      """
      Function that computes the norm of the vector from O to the current instance
      """
      return sqrt((self.x)**2 + (self.y)**2 + (self.z)**2)

    
    def distance(self, another_atom):
        """
        Function that computes the distance between the current instance and another atom
        """
        return sqrt((self.x - another_atom.x)**2 + (self.y-another_atom.y)**2 + (self.z - another_atom.z))


    def substract(self, another_atom):
        """
        Function that computes the substraction between the current atom and the other atom passed as a parameter, and returns it as a new Atom with an empty name.
        """
        return Atom("", self.x - another_atom.x, self.y - another_atom.y, self.z - another_atom.z)

    
    def dot_product(self, another_atom):
        """
        Function that computes the dot product between the current atom and the other atom passed as a parameter, and returns it as a float
        """
        return float(self.x*another_atom.x + self.y*another_atom.y + self.z*another_atom.z)


    def cross_product(self, another_atom):
        """
        Function that computes the cross product between the current atom and the other atom passed as a parameter, and returns it as a new Atom with an empty name.
        """
        x = (self.y*another_atom.z) - (self.z*another_atom.y)
        y = (self.z*another_atom.x) - (self.x*another_atom.z)
        z = (self.x*another_atom.y) - (self.y*another_atom.x)
        return Atom("",x,y,z)

      
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
    
  print(atom1.dot_product(atom2))
  print(atom2)
  print(atom3)
