import Atom

class AminoAcid : 

  def __init__(self, res_number, res_type):
    self._res_number = res_number
    self._res_type = res_type
    self._atoms = []

    if len(self._res_type) != 3 : 
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

  
  def angle_diedre(self) : 
    """
    
    """
    angle = []
    for i, atom in enumerate(self.atoms) : 
      if i + 3 < len(self.atoms) : 
        angle.append(atom.dihedral(self.atoms[i + 1], self.atoms[i + 2], self.atoms[i + 3]))
    
    return angle      



if __name__ == "__main__" : 
  atom1 = Atom.Atom("N",18.0,9.5,192.5)
  atom2 = Atom.Atom("C",18.0,9.5,0)
  atom3 = Atom.Atom("O",0,0,1)
  atom4 = Atom.Atom("CA", 0, 0, 1)
  atom5 = Atom.Atom("D", 0, 0, 1)
  a1 = AminoAcid(1, "MET")
  a1.add(atom1)
  a1.add(atom2)
  a1.add(atom3)
  a1.add(atom4)
  print(a1)
  print(a1.C)
  print(a1.CA)
  print(a1.N)
  print(a1.O)
  # a1.add(atom5)
  print(a1.angle_diedre())

  # a1 = Atom.Atom("N", 1, 0, 0)
  # a2 = Atom.Atom("CA",-1.93, 7.47, 6.55)
  # a3 = Atom.Atom("O", 1.5, 5, 3.2)
  # a4 = Atom.Atom("C", 3, 0, 2)

  # AA = AminoAcid(1, "SER")
         
  
  # AA.add(a1)
  # AA.add(a2)
  # AA.add(a3)
  # AA.add(a4)

  # print(AA.angle_diedre())