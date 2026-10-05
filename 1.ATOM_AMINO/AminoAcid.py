import Atom


class AminoAcid(Atom) : 

  def __init__(self, name, px, py, pz, res_number, res_type, list_atoms):
    super.__init__(name, px, py, pz)
    self._res_number = res_number
    self._res_type = res_type
    self._atoms = list_atoms

    if len(self._res_type) != 3 : 
      raise ValueError

    if len(self._atoms) == 0 : 
      raise ValueError


  @property
  def res_number(self) : 
    return self._res_number

  @res_number.setter 
  def res_number(self, res_number) : 
    self._res_number = res_number


  @property
  def res_type(self) : 
    return self._res_type

  @res_type.setter
  def res_type(self, res_type) : 
    self._res_type = res_type


  @property 
  def atoms(self) : 
    return self._atoms


  def __str__(self):
    s = "Amino acid number {} of type {} with a list of {} atoms".format(self.res_number, self.res_type, len(self.atoms))
    return(s)    

    
  def add(self, atom):
    """
    Function that adds a new atom in the list of atoms for the current residue
    """
    
  def get_N(self):
    """
    Function that returns an Atom corresponding to the N of the current residue
    """

  def get_CA(self):
    """
    Function that returns an Atom corresponding to the CA of the current residue
    """      

  def get_C(self):
    """
    Function that returns an Atom corresponding to the C of the current residue
    """  	

  def get_O(self):
    """
    Function that returns an Atom corresponding to the O of the current residue
    """

if __name__ == "__main__" : 
  a1 = AminoAcid(1, "MET", ["N", "C", "C", "O", "C"])
  print(a1)