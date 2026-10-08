"""
Script principal du projet Ramachandran : lance toute la chaine avec une entree et
des sorties.

Entree :
    un fichier PDB (par exemple 1tey_model1.pdb ou 1TEY.pdb)

Sorties (dans le dossier --sortie, "resultats" par defaut) :
    <nom>_angles.txt    phi et psi de chaque residu (en radians), separes par une tabulation
    <nom>_clusters.tsv  phi, psi et numero de cluster (-1 = point de bruit avec DBSCAN)
    <nom>_qualite.txt   coefficient de silhouette et indice de Dunn du clustering

Etapes : lecture du PDB -> angles phi/psi -> clustering (K-means ou DBSCAN) -> qualite.

Exemples :
    python main.py 1tey_model1.pdb
    python main.py 1tey_model1.pdb --algo dbscan --eps 0.3 --min-points 4
    python main.py 1TEY.pdb --modele 3 --k 4
"""
import argparse
import os
import sys
import tempfile

# The code of the project lives in three folders: we add them to the Python path
ROOT = os.path.dirname(os.path.abspath(__file__))
for folder in ["1.ATOM_AMINO", "2.PDB_STRUCT", "3.STATS"]:
    sys.path.append(os.path.join(ROOT, folder))

from PDBStructure import StructurePDB
from clustering import Kmeans, dbscan, ClusterPoint
from clusteringMeasures import ClusteringMeasures


def extract_model(pdb_path, model_number, folder):
    """
    Un fichier PDB de RMN (comme 1TEY.pdb) contient plusieurs modeles. On en extrait un seul
    dans un fichier temporaire, car StructurePDB lit un fichier comme une seule structure.
    Si le fichier n'a pas de ligne MODEL, il est utilise tel quel.
    """
    with open(pdb_path) as f:
        lines = f.read().splitlines()

    model_lines = [line for line in lines if line.startswith("MODEL")]
    if len(model_lines) == 0:
        return pdb_path

    if model_number < 1 or model_number > len(model_lines):
        print("Erreur : le fichier contient", len(model_lines), "modeles, pas le modele",
              model_number)
        sys.exit(1)

    kept = []
    current = 0
    for line in lines:
        if line.startswith("MODEL"):
            current = current + 1
        elif line.startswith("ENDMDL"):
            if current == model_number:
                break
        elif current == model_number:
            kept.append(line)

    temp_path = os.path.join(folder, "modele.pdb")
    with open(temp_path, "w") as f:
        f.write("\n".join(kept) + "\n")
    return temp_path


def cluster_with_kmeans(points, k):
    """Renvoie la liste des numeros de cluster, dans le meme ordre que les points."""
    model = Kmeans(points, k)
    model.run()

    cluster_of = {}
    for number, group in model.liste_k.items():
        for p in group:
            cluster_of[id(p)] = number

    labels = []
    for p in points:
        labels.append(cluster_of[id(p)])
    return labels


def cluster_with_dbscan(points, eps, min_points):
    """Renvoie la liste des numeros de cluster (-1 pour le bruit), dans l'ordre des points."""
    # dbscan works with [x, y] lists and gives back the numbers of the points
    lists = []
    for p in points:
        lists.append([p.x, p.y])

    model = dbscan(lists, eps, min_points)
    model.run()

    labels = [-1] * len(points)
    for number, group in enumerate(model.liste_k):
        for index in group:
            labels[index] = number
    return labels


def write_clusters(path, points, labels):
    """Ecrit un fichier a 3 colonnes : phi, psi, cluster (separees par des tabulations)."""
    with open(path, "w", encoding="utf-8") as f:
        f.write("phi\tpsi\tcluster\n")
        for p, label in zip(points, labels):
            f.write("{:.6f}\t{:.6f}\t{}\n".format(p.x, p.y, label))


def compute_quality(points, labels):
    """Renvoie un texte avec la silhouette et l'indice de Dunn (le bruit est ignore)."""
    cluster_points = []
    for p, label in zip(points, labels):
        if label != -1:
            cluster_points.append(ClusterPoint(p.x, p.y, label))

    numbers = set()
    for p in cluster_points:
        numbers.add(p.nb_cluster)

    text = "Nombre de clusters : {}\n".format(len(numbers))
    text += "Points classes : {} sur {}\n".format(len(cluster_points), len(points))

    if len(numbers) < 2:
        text += "Mesures de qualite impossibles : il faut au moins 2 clusters.\n"
        return text

    measures = ClusteringMeasures(cluster_points)
    text += "Coefficient de silhouette : {:.4f}  (entre -1 et 1)\n".format(
        measures.coeff_silhouette())
    try:
        text += "Indice de Dunn : {:.4f}  (plus il est grand, mieux c'est)\n".format(
            measures.indice_dunn())
    except ValueError as error:
        text += "Indice de Dunn impossible : {}\n".format(error)
    return text


def main():
    parser = argparse.ArgumentParser(
        description="Fichier PDB -> angles phi/psi -> clustering -> qualite")
    parser.add_argument("pdb", help="fichier PDB en entree")
    parser.add_argument("--modele", type=int, default=1,
                        help="numero du modele a lire si le PDB en contient plusieurs (defaut : 1)")
    parser.add_argument("--algo", choices=["kmeans", "dbscan"], default="kmeans",
                        help="algorithme de clustering (defaut : kmeans)")
    parser.add_argument("--k", type=int, default=3,
                        help="kmeans : nombre de groupes (defaut : 3)")
    parser.add_argument("--eps", type=float, default=0.3,
                        help="dbscan : distance de voisinage (defaut : 0.3)")
    parser.add_argument("--min-points", type=int, default=4,
                        help="dbscan : nombre minimum de voisins (defaut : 4)")
    parser.add_argument("--sortie", default="resultats",
                        help="dossier des fichiers de sortie (defaut : resultats)")
    args = parser.parse_args()

    if not os.path.isfile(args.pdb):
        print("Erreur : fichier introuvable :", args.pdb)
        sys.exit(1)

    os.makedirs(args.sortie, exist_ok=True)
    name = os.path.splitext(os.path.basename(args.pdb))[0]

    # 1. Read the PDB file and compute the phi / psi angles
    with tempfile.TemporaryDirectory() as temp_folder:
        pdb_to_read = extract_model(args.pdb, args.modele, temp_folder)
        structure = StructurePDB(pdb_to_read)
        structure.compute_dihedrals()
    points = structure._phipsi
    print("Residus lus :", len(structure._residues), "| couples (phi, psi) :", len(points))

    angles_path = os.path.join(args.sortie, name + "_angles.txt")
    structure.write_dihedrals(angles_path)

    # 2. Clustering (the classes refuse invalid parameters with a ValueError or TypeError)
    try:
        if args.algo == "kmeans":
            labels = cluster_with_kmeans(points, args.k)
        else:
            labels = cluster_with_dbscan(points, args.eps, args.min_points)
    except (ValueError, TypeError) as error:
        print("Erreur : parametres de clustering invalides :", error)
        sys.exit(1)

    clusters_path = os.path.join(args.sortie, name + "_clusters.tsv")
    write_clusters(clusters_path, points, labels)

    # 3. Quality of the clustering
    quality = compute_quality(points, labels)
    quality_path = os.path.join(args.sortie, name + "_qualite.txt")
    with open(quality_path, "w", encoding="utf-8") as f:
        f.write(quality)

    print(quality)
    print("Fichiers ecrits dans", args.sortie, ":")
    print(" -", os.path.basename(angles_path))
    print(" -", os.path.basename(clusters_path))
    print(" -", os.path.basename(quality_path))


if __name__ == "__main__":
    main()
