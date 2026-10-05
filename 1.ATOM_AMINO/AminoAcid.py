

class AminoAcid : 

  def __init__(self, res_number, res_type, list_atoms = []):
    self._res_number = res_number
    self._res_type = res_type
    self._atoms = list_atoms 

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
    self.atoms.append(atom)


  @property 
  def N(self):
    """
    Function that returns an Atom corresponding to the N of the current residue
    """
    return(atom for atom in self.atoms if atom.name == "N")


  @property
  def CA(self):
    """
    Function that returns an Atom corresponding to the CA of the current residue
    """     
    return(atom for atom in self.atoms if atom.name == "CA") 


  @property
  def C(self):
    """
    Function that returns an Atom corresponding to the C of the current residue
    """  
    return(atom for atom in self.atoms if atom.name == "C") 	
  

  @property
  def O(self):
    """
    Function that returns an Atom corresponding to the O of the current residue
    """
    return(atom for atom in self.atoms if atom.name == "O") 



if __name__ == "__main__" : 
  a1 = AminoAcid(1, "MET", ["N", "C", "C", "O", "C"])
  print(a1)