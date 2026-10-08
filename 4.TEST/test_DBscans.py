"""
Tests unitaires et tests d'usage des classes Dbscan (fichier clustering.py).

"""
import random
import unittest

from Point import Point
from clustering_DBscan import dbscan as Dbscan



# ---------------------------------------------------------------------------
# Fonctions utilitaires (simples, communes a tous les tests)
# ---------------------------------------------------------------------------

def make_points(coordinates):
    """Transforme une liste de tuples (x, y) en liste de Point."""
    points = []
    for (x, y) in coordinates:
        points.append(Point(x, y))
    return points


def run_kmeans(points, k):
    """Construit un Kmeans, le lance, et renvoie la liste des groupes."""
    km = Kmeans(points, k)
    km.run()
    return km.clusters


def run_dbscan(points, epsilon, minpoints):
    """Construit un Dbscan, le lance, et renvoie la liste des clusters (sans le bruit)."""
    # dbscan wants plain [x, y] lists, not Point objects
    lists = []
    for p in points:
        lists.append([p.x, p.y])
    db = Dbscan(lists, epsilon, minpoints)
    db.clustering()                    # the method is called clustering(), not run()
    # liste_k contains indices: we turn them back into the original Point objects
    result = []
    for group in db.liste_k:
        points_of_group = []
        for i in group:
            points_of_group.append(points[i])
        result.append(points_of_group)
    return result


def coords_of(group):
    """Renvoie la liste triee des (x, y) d'un groupe de Point."""
    result = []
    for p in group:
        result.append((p.x, p.y))
    result.sort()
    return result


def all_coords(clusters):
    """Renvoie la liste triee des (x, y) de tous les points de tous les groupes."""
    result = []
    for group in clusters:
        for p in group:
            result.append((p.x, p.y))
    result.sort()
    return result


def count_points(clusters):
    """Renvoie le nombre total de points dans tous les groupes."""
    total = 0
    for group in clusters:
        total = total + len(group)
    return total


def canonical(clusters):
    """
    Renvoie les clusters sous une forme comparable : une liste triee de groupes
    tries. Ainsi l'ordre des groupes et leur numerotation n'ont pas d'importance.
    """
    result = []
    for group in clusters:
        result.append(coords_of(group))
    result.sort()
    return result


# Deux blobs tres eloignes l'un de l'autre (utilises dans plusieurs tests)
BLOB_A = [(0, 0), (0, 1), (1, 0), (1, 1)]
BLOB_B = [(100, 100), (100, 101), (101, 100), (101, 101)]

# Deux blobs tres eloignes l'un de l'autre, mais un peu irreguliers. Avec des blobs parfaitement reguliers (carres symetriques), l'initialisation aleatoire de Kmeans peut parfois tomber sur une mauvaise reponse, meme si le code est correct. Des blobs irreguliers evitent cette fausse alerte.
KM_BLOB_A = [(0, 0), (1, 0.2), (0.3, 1.1), (1.4, 1.3), (0.7, 0.5)]
KM_BLOB_B = [(100, 100), (101.2, 100.1), (100.4, 101.3), (101.5, 101.1), (100.8, 100.6)]


# ---------------------------------------------------------------------------
# DBSCAN
# ---------------------------------------------------------------------------

class TestDbscanInvalid(unittest.TestCase):
    """Cas invalides : epsilon, minpoints et liste de points."""

    def setUp(self):
        self.points = make_points(BLOB_A + BLOB_B)

    def test_epsilon_zero(self):
        """
        epsilon est un rayon de voisinage. Un rayon de 0 ne
        represente rien : il doit etre strictement positif.
        """
        with self.assertRaises((ValueError, TypeError)):
            run_dbscan(self.points, 0, 3)

    def test_epsilon_negative(self):
        """
        une distance negative n'existe pas, le rayon doit donc etre
        refuse s'il est negatif.
        """
        with self.assertRaises((ValueError, TypeError)):
            run_dbscan(self.points, -1.5, 3)

    def test_epsilon_string(self):
        """
        epsilon doit etre un nombre. Une chaine comme "abc" ferait
        planter la comparaison avec les distances ; on veut une erreur claire.
        """
        with self.assertRaises((ValueError, TypeError)):
            run_dbscan(self.points, "abc", 3)

    def test_epsilon_none(self):
        """
        None (valeur oubliee).
        """
        with self.assertRaises((ValueError, TypeError)):
            run_dbscan(self.points, None, 3)

    def test_minpoints_zero(self):
        """
        un point noyau doit avoir au moins 1 voisin ; minpoints = 0
        rendrait tous les points "noyau". On le refuse.
        """
        with self.assertRaises((ValueError, TypeError)):
            run_dbscan(self.points, 2, 0)

    def test_minpoints_negative(self):
        """
        un nombre minimum de points negatif n'a pas de sens.
        """
        with self.assertRaises((ValueError, TypeError)):
            run_dbscan(self.points, 2, -2)

    def test_minpoints_not_integer(self):
        """
        un nombre de points est forcement entier (3.5 points n'existe
        pas). On verifie que le float est refuse.
        """
        with self.assertRaises((ValueError, TypeError)):
            run_dbscan(self.points, 2, 3.5)

    def test_empty_points_list(self):
        """
        sans point, il n'y a rien a clusteriser. Cas oublie tres
        souvent.
        """
        with self.assertRaises((ValueError, TypeError)):
            run_dbscan([], 2, 3)



class TestDbscanPartition(unittest.TestCase):
    """Chaque point est soit dans un cluster, soit du bruit, jamais les deux."""

    def setUp(self):
        # deux blobs + deux points isoles (bruit)
        self.coordinates = BLOB_A + BLOB_B + [(50, 50), (-50, -50)]
        self.points = make_points(self.coordinates)

    def test_no_point_duplicated(self):
        """
        un point ne peut pas appartenir a deux clusters. Si une
        coordonnee apparait deux fois dans la sortie, l'algorithme a ajoute le
        meme point plusieurs fois.
        """
        clusters = run_dbscan(self.points, 2, 3)
        result = all_coords(clusters)
        for i in range(len(result) - 1):
            self.assertNotEqual(result[i], result[i + 1])

    def test_clusters_plus_noise_equals_total(self):
        """
        on ne doit rien perdre. Le bruit = points d'entree absents des
        clusters, donc clusters + bruit = total par construction ; ce test verifie
        surtout que les clusters ne contiennent QUE des points d'entree, et pas
        plus de points qu'on en a donne.
        """
        clusters = run_dbscan(self.points, 2, 3)
        in_clusters = count_points(clusters)
        noise = len(self.points) - in_clusters
        self.assertGreaterEqual(noise, 0)
        self.assertEqual(in_clusters + noise, len(self.points))

    def test_clusters_contain_only_input_points(self):
        """
        l'algorithme ne doit pas inventer de nouveaux points. Chaque
        point d'un cluster doit exister dans les donnees d'entree.
        """
        clusters = run_dbscan(self.points, 2, 3)
        for c in all_coords(clusters):
            self.assertIn(c, self.coordinates)

    def test_no_empty_cluster(self):
        """
        un cluster vide n'a pas de sens. Dbscan ne cree un cluster
        qu'a partir d'un point noyau, donc il contient toujours des points.
        """
        clusters = run_dbscan(self.points, 2, 3)
        for group in clusters:
            self.assertGreater(len(group), 0)


class TestDbscanKnownSolution(unittest.TestCase):
    """Cas ou on connait la bonne reponse a l'avance."""

    def test_two_dense_blobs_no_noise(self):
        """
        Deux blobs denses et tres eloignes
        doivent donner exactement 2 clusters et aucun bruit.
        """
        points = make_points(BLOB_A + BLOB_B)
        clusters = run_dbscan(points, 2, 3)
        self.assertEqual(len(clusters), 2)
        expected = canonical([make_points(BLOB_A), make_points(BLOB_B)])
        self.assertEqual(canonical(clusters), expected)

    def test_single_point_is_noise(self):
        """
        un point seul n'a aucun voisin, donc il ne peut pas etre noyau
        avec minpoints = 2. Il doit etre du bruit : 0 cluster.
        """
        clusters = run_dbscan(make_points([(0, 0)]), 1, 2)
        self.assertEqual(count_points(clusters), 0)

    def test_tiny_epsilon_everything_is_noise(self):
        """
        si epsilon est plus petit que tous les ecarts entre points,
        personne n'a de voisin, donc tout est bruit et il n'y a aucun cluster.
        """
        points = make_points([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)])
        clusters = run_dbscan(points, 0.1, 2)
        self.assertEqual(len(clusters), 0)

    def test_huge_epsilon_one_single_cluster(self):
        """
        a l'inverse, si epsilon est enorme, tous les points sont
        voisins de tous : on attend un seul cluster contenant tous les points.
        """
        coordinates = BLOB_A + BLOB_B
        clusters = run_dbscan(make_points(coordinates), 1000, 2)
        self.assertEqual(len(clusters), 1)
        self.assertEqual(coords_of(clusters[0]), sorted(coordinates))

