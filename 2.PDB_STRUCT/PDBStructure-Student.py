# -*- coding: utf-8 -*-
from math import atan2, sqrt

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

    previous_res_num = None

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
      residue_num = int(line[22:26].strip()) #On récupère le numéro du résidu dans le fichier PDB

      #Détection d'un nouveau résidu 
      if residue_num != previous_res_num:
          aa = AminoAcid(residue_num, residue_type, [])
          self.residues.append(aa) #on ajoute un objet AminoAcid à la liste de résidus, avec le type de résidu et une liste vide qui contiendra les atomes et leurs coordonnées
          previous_res_num = residue_num

      #On récupère et stocke les coordonnées
      coordX = float(line[32:39].strip())
      coordY = float(line[41:46].strip())
      coordZ = float(line[49:54].strip())
      atom = Atom(atom_name, coordX, coordY, coordZ) #objet Atom créé, ajouté à l'objet AminoAcid correspondant

      self.residues[-1].add(atom) #on ajoute les objets Atom créés dans la liste de coordonnées des atomes dans le dernier objet AminoAcid (le résidu dont on est entrain de parcourir les atomes)


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

    return -atan2(y, x)
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

    #BROUILLON !!

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