import Atom

class AminoAcid : 

  def __init__(self, res_number, res_type, list_atoms = []):
    self._res_number = res_number
    self._res_type = res_type
    self._atoms = list_atoms 

    if len(self._res_type) != 3 : 
      raise ValueError


  @property
  def res_number(self) : 
    return self._res_numbera

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
    if atom.name in ["N", "O", "C", "CA"] : 
      self.atoms.append(atom)
    else : 
      raise ValueError


  @property 
  def N(self):
    """
    Function that returns an Atom corresponding to the N of the current residue
    """
    return(next(atom for atom in self.atoms if atom.name == "N"))


  @property
  def CA(self):
    """
    Function that returns an Atom corresponding to the CA of the current residue
    """     
    return(next(atom for atom in self.atoms if atom.name == "CA"))


  @property
  def C(self):
    """
    Function that returns an Atom corresponding to the C of the current residue
    """  
    return(next(atom for atom in self.atoms if atom.name == "C"))	
  

  @property
  def O(self):
    """
    Function that returns an Atom corresponding to the O of the current residue
    """
    return(next(atom for atom in self.atoms if atom.name == "O")) 

  
  def is_angle_diedre(self) : 
    """
    
    """
    for atom in self.atoms : 
      if atom + 3 <= len(self.atoms) : 
        atom.dihedral(atom + 1, atom + 2, atom + 3)  



if __name__ == "__main__" : 
  atom1 = Atom.Atom("N",18.0,9.5,192.5)
  atom2 = Atom.Atom("C",18.0,9.5,0)
  atom3 = Atom.Atom("O",0,0,1)
  atom4 = Atom.Atom("CA", 0, 0, 1)
  atom5 = Atom.Atom("D", 0, 0, 1)
  a1 = AminoAcid(1, "MET", [atom1, atom2, atom3, atom4])
  print(a1)
  print(a1.C)
  print(a1.CA)
  print(a1.N)
  print(a1.O)
  # a1.add(atom5)
  print(a1.is_angle_diedre)