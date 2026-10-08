import sys
from math import atan2
from pathlib import Path

# Récupère le chemin absolu du dossier 1.ATOM_AMINO (situé à côté de 2.PDB_STRUCT)
atom_amino_dir = Path(__file__).resolve().parent.parent / "1.ATOM_AMINO"
sys.path.append(str(atom_amino_dir))

from AminoAcid import AminoAcid
from Atom import Atom
from Point import Point


class StructurePDB: 
	
  def __init__(self, filename): 
    """
    Functions that reads a simple PDB file and the necessary information about residues to compute dihedral angles
    """
    self._path_to_file = filename
    self._residues = []
    self._phipsi = [] #Liste d'objets Point (phi, psi)
    #On déclare ici tous les attributs de la classe dès sa création même si on ne s'en sert que dans compute_dihedrals

    self.phi = []
    self.psi = []

    previous_res_num = None

    fd = open(self._path_to_file,'r')
    lines = fd.readlines() #.strip() rajouté pour les \n
    fd.close()
    
    for line in lines:
      line = line.rstrip('\r\n')
      
      #Sécurité pour vérifier que la ligne n'est pas trop courte (taille standardisée à 78 char)
      if len(line) < 5:
        continue
      
      #On ne s'intéresse qu'aux lignes ATOM
      if line[0:4] != "ATOM":
        continue
      
      atom_name = line[12:16].strip()
      #On ne s'intéresse qu'aux atomes N, CA, C et O car squelette des aa, pour calcul des angles 
      if atom_name not in ["N","CA","C","O"]:
        continue
      
      residue_type = line[17:20].strip() #type de résidu = amino acid
      residue_num = int(line[22:26].strip()) #On récupère le numéro du résidu dans le fichier PDB

      #Détection d'un nouveau résidu 
      if residue_num != previous_res_num:
          aa = AminoAcid(residue_num, residue_type, [])
          self._residues.append(aa) #on ajoute un objet AminoAcid à la liste de résidus, avec le type de résidu et une liste vide qui contiendra les atomes et leurs coordonnées
          previous_res_num = residue_num

      #On récupère et stocke les coordonnées
      coordX = float(line[31:38].strip())
      coordY = float(line[38:46].strip())
      coordZ = float(line[46:54].strip())
      atom = Atom(atom_name, coordX, coordY, coordZ) #objet Atom créé, ajouté à l'objet AminoAcid correspondant

      self._residues[-1].add(atom) #on ajoute les objets Atom créés dans la liste de coordonnées des atomes dans le dernier objet AminoAcid (le résidu dont on est entrain de parcourir les atomes)


  def calculate_dihedrals(self, a1, a2, a3, a4):
    """
    Calcule l'angle dièdre (en radians) défini par 4 atomes (a1, a2, a3, a4).

    L'angle dièdre est l'angle de torsion entre le plan formé par les 3 premiers atomes A1 A2 A3 et le plan formé par les 3 derniers A2, A3, A4.

    S'appuie sur les fonctions définies dans la classe Atom.
    """
    # Calcule des vecteurs entre les atomes (qui les relient entre eux)
    b1 = a2.substract(a1) # Vecteur A1 -> A2
    b2 = a3.substract(a2) # Vecteur A2 -> A3
    b3 = a4.substract(a3) # Vecteur A3 -> A4

    # Calcul des deux plans (produit vectoriel avec cross_product)
    n1 = b1.cross_product(b2) # Vecteur perpendiculaire au premier plan (A1, A2, A3)
    n2 = b2.cross_product(b3) # Vecteur perpendiculaire au second plan (A2, A3, A4)

    # Calcul des composantes de l'angle pour atan2
    x = n1.dot_product(n2) #dot_product = produit scalaire
    #x mesure le cosinus de l'angle entre les deux plans.
    y = n1.cross_product(n2).dot_product(b2) / b2.norm() #norm = norme du vecteur
    #y mesure le sinus

    return atan2(y, x)
   #Atan2 calcule l'angle exact (en radians à partir de ses composantes x et y, en gérant automatiquement le bon quadrant et le signe de la rotation. 
   #Le signe négatif permet de respecter la convention de sens utilisée en biochimie structurale.

  def _get_atom_by_name(self, aa, name):
    """Permet de récupérer un atome spécifique dans un résidu"""
    for atom in aa.atoms:
      if atom.name == name:
        return atom
    return None

  def compute_dihedrals(self):
    """
    Calcule les angles dièdres phi et psi pour chaque résidu et stocke les couples dans self.phipsi sous forme de Point(phi, psi).
    """
    self._phipsi = [] # list of Points (class Point...)
    #On réinitialise compute_dihedrals
    psi = []
    phi = []

    for ires in range(len(self._residues)):
      current_aa = self._residues[ires]

      # Récupération des atomes du résidu courant
      c_n = self._get_atom_by_name(current_aa, "N")
      c_ca = self._get_atom_by_name(current_aa, "CA")
      c_c = self._get_atom_by_name(current_aa, "C")

      phi_val = None
      psi_val = None

      # Calcul de PHI : C(i-1) - N(i) - CA(i) - C(i)
      if ires > 0:
          prev_aa = self._residues[ires - 1]
          p_c = self._get_atom_by_name(prev_aa, "C")
          if p_c and c_n and c_ca and c_c:
              phi_val = self.calculate_dihedrals(p_c, c_n, c_ca, c_c)
              phi.append(phi_val)

      # Calcul de PSI : N(i) - CA(i) - C(i) - N(i+1)
      if ires < len(self._residues) - 1:
          next_aa = self._residues[ires + 1]
          n_n = self._get_atom_by_name(next_aa, "N")
          if c_n and c_ca and c_c and n_n:
              psi_val = self.calculate_dihedrals(c_n, c_ca, c_c, n_n)
              psi.append(psi_val)

      # Si les deux angles existent pour le résidu, on enregistre le point (phi, psi)
      if phi_val is not None and psi_val is not None:
          self._phipsi.append(Point(phi_val, psi_val))

    return phi, psi

  def write_dihedrals(self, filename):
    """
    Écrit les angles phi et psi (en radians) séparés par une tabulation dans un fichier.
    """
    with open(filename, 'w', encoding='utf-8') as out:
       out.writelines(f"{pt.x:.6f}\t{pt.y:.6f}\n" for pt in self._phipsi)
 
    
    
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
if __name__ == "__main__":
  iS = StructurePDB("1TEY.pdb")
  print(iS._residues[0])
  print(iS._residues[1])
  print(iS._residues[2])
  phi, psi = iS.compute_dihedrals()
  iS.write_dihedrals("angles_1TEY.txt")

  # Amino acid number 1 of type MET with a list of 4 atoms
  # Amino acid number 2 of type ALA with a list of 4 atoms
  # Amino acid number 3 of type LYS with a list of 4 atoms

  print("PHI")
  print(phi[:10])
  print("-------------------")
  print("PSI")
  print(psi[:10])