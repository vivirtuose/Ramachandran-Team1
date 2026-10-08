"""
Script principal : il relie les scripts du projet entre eux, sans rien ajouter.

Entree : un fichier PDB.
Chaine : PDBStructure -> Kmeans -> ClusteringMeasures.
Les fichiers de sortie sont ecrits par les classes elles-memes :
    <prefixe>_angles.txt    ecrit par StructurePDB.write_dihedrals
    <prefixe>_clusters.tsv  ecrit par Kmeans.create_tsv (phi, psi, cluster)
La silhouette et l'indice de Dunn sont affiches a l'ecran.

Utilisation :
    python main.py ENTREE.pdb [K] [PREFIXE_SORTIE]
Exemple :
    python main.py 1tey_model1.pdb 3
"""
import os
import sys

# The code of the project lives in three folders
ROOT = os.path.dirname(os.path.abspath(__file__))
for folder in ["1.ATOM_AMINO", "2.PDB_STRUCT", "3.STATS"]:
    sys.path.append(os.path.join(ROOT, folder))

from PDBStructure import StructurePDB
from clustering import Kmeans
from clusteringMeasures import ClusteringMeasures


if len(sys.argv) < 2:
    print("Utilisation : python main.py ENTREE.pdb [K] [PREFIXE_SORTIE]")
    sys.exit(1)

pdb_path = sys.argv[1]
k = int(sys.argv[2]) if len(sys.argv) > 2 else 3
prefix = sys.argv[3] if len(sys.argv) > 3 else os.path.splitext(pdb_path)[0]

# 1. PDB file -> phi / psi angles
structure = StructurePDB(pdb_path)
structure.compute_dihedrals()
structure.write_dihedrals(prefix + "_angles.txt")

# 2. Angles -> clustering
modele = Kmeans(structure._phipsi, k)
modele.run()
modele.create_tsv(prefix + "_clusters.tsv")

# 3. Clustering -> quality measures
mesures = ClusteringMeasures(modele.convert_in_clusterPoint())
print("Coefficient de silhouette :", mesures.coeff_silhouette())
print("Indice de Dunn :", mesures.indice_dunn())
