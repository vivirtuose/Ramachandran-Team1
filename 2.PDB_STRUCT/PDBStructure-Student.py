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
    self.phipsi = [] #Liste d'objets Point (phi, psi)

    previous_res_type = None

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

      
      atom_name = line[12:16].strip()
      #On ne s'intéresse qu'aux atomes N, CA, C et O car squelette des aa, pour calcul des angles 
      if atom_name not in ["N","CA","C","O"]:
        continue
      
      residue_type = line[17:20].strip() #type de résidu = amino acid
      
      if (residue_type != previous_res_type):
        aa = AminoAcid(residue_type, [])
        self.residues.append(aa) #on ajoute un objet AminoAcid à la liste de résidus, avec le type de résidu et une liste vide qui contiendra les atomes et leurs coordonnées
        previous_res_type = residue_type

      #On stocke les coordonnées
      coordX = float(line[32:39].strip())
      coordY = float(line[41:46].strip())
      coordZ = float(line[49:54].strip())
      atom = Atom(atom_name, coordX, coordY, coordZ) #objet Atom créé, ajouté à l'objet AminoAcid correspondant

      self.residues[-1].add(atom) #on ajoute les objets Atom créés dans la liste de coordonnées des atomes dans le dernier objet AminoAcid (le résidu dont on est entrain de parcourir les atomes)


  def compute_dihedrals(self):
    """
    Functions that computes dihedral angles
    """
    phi = [] # list of floats
    psi = [] # list of floats
    self.phipsi = [] # list of Points (class Point...)

    for ires in range(len(self.residues)):
      current_aa = self.residues[ires]
      for iaa in range(len(current_aa)):
        list_atoms = current_aa[iaa].atom

    #On parcours les atomes de chaque aa
    for iat in range(len(list_atoms)-1):
      if list_atoms[iat].name == "N"and list_atoms[iat].name == "CA":
        pass
      #calcul angle phi




	
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