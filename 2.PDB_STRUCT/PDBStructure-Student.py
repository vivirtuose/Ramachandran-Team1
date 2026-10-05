from AminoAcid import AminoAcid
from Atom import Atom
from Point import Point

class StructurePDB: 
	
  def __init__(self, filename): 
    """
    Functions that reads a simple PDB file and the necessary information about residues to compute dihedral angles
    """
    self.path_to_file = filename
    self.residues = []
    previous_res_type = ""

    fd = open(self.path_to_file,'r')
    lines = fd.readlines().strip() #.strip() rajouté pour les \n
    fd.close()
    
    for line in lines:
      
      #Sécurité pour vérifier que la ligne n'est pas trop courte (taille standardisée à 78 char)
      if len(line) != 78:
        continue
      
      #On ne s'intéresse qu'aux lignes ATOM
      if line[0:4] != "ATOM":
        continue
      
      atom_type = line[12:17].strip()
      if atom_type not in ["N","CA","C","O"]:
        continue
      
      residue_type = line[17:20].strip() #type de résidu = amino acid
      
      if (residue_type != previous_res_type):
        aa = AminoAcid(residue_type, [])
        self.residues.append(aa)
        previous_res_type = residue_type
      
      coordX = float(line[32:39].strip())
      coordY = float(line[41:46].strip())
      coordZ = float(line[49:54].strip())
      atom = Atom(atom_type, coordX, coordY, coordZ)

      self.residues[-1].add(atom)


  def compute_dihedrals(self):
    """
    Functions that computes dihedral angles
    """
    phi = [] # list of floats
    psi = [] # list of floats
    self.phipsi = [] # list of Points (class Point...)
	
    phi.append(0.00)
    
    aa = self.residues[0]
   


  def write_dihedrals(self, filename):
    """
    Functions that writes a file with 2 columns phi and psi separated by a tabulation, with one line per residue. Values of phi and psi angles are given with a precision of 6 decimals.
    """
 
    
    
#	public static void main(String[] args) throws FileNotFoundException{
#		StructurePDB tey = new StructurePDB("D:/workspace/Enseignement/src/ramachandran/1TEY.pdb");
#		tey.readPDBFile();
#		tey.computeDihedrals();
#		
#		KMeans k4 = new KMeans(tey.phipsi,4);
#		System.out.println(k4);
#		k4.clusterize();
#		System.out.println(k4);
		
#		k4.printOutput();
#	}
iS = StructurePDB("1TEY.pdb")
print(iS.residues[0])
print(iS.residues[1])
print(iS.residues[2])
iS.compute_dihedrals()
iS.write_dihedrals("angles_1TEY.txt")