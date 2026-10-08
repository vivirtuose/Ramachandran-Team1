"""
Tests unitaires et tests d'usage de la classe ClusteringMeasures
(fichier clusteringMeasures.py)
"""
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from clustering_KMeans import ClusterPoint

# TEMPORARY WORKAROUND: clusteringMeasures.py starts with "import ClusterPoint", but
# there is no file ClusterPoint.py (the class is in clustering_KMeans.py). Until the
# import is fixed in clusteringMeasures.py, we register the class under that name so
# the file can be imported. Remove these two lines once the import is fixed.
sys.modules["ClusterPoint"] = ClusterPoint

from clusteringMeasures import ClusteringMeasures


# ---------------------------------------------------------------------------
# Fonctions utilitaires (simples, communes a tous les tests)
# ---------------------------------------------------------------------------

def make_cluster_points(data):
    """Transforme une liste de tuples (x, y, cluster) en liste de ClusterPoint."""
    points = []
    for (x, y, cluster) in data:
        points.append(ClusterPoint(x, y, cluster))
    return points


def compute_silhouette(measures):
    """Renvoie le coefficient de silhouette d'un objet ClusteringMeasures."""
    return measures.silhouette_coefficient()


def compute_dunn(measures):
    """Renvoie l'indice de Dunn d'un objet ClusteringMeasures."""
    return measures.dunn_index()


# Deux clusters compacts et bien separes, sur une ligne :
#   cluster 1 : (0,0) (2,0)      cluster 2 : (10,0) (12,0)
GOOD_CLUSTERING = [(0, 0, 1), (2, 0, 1), (10, 0, 2), (12, 0, 2)]

# Les memes 4 points, mais mal classes (chaque cluster melange un point de
# chaque cote) :
#   cluster 1 : (0,0) (12,0)     cluster 2 : (2,0) (10,0)
BAD_CLUSTERING = [(0, 0, 1), (2, 0, 2), (10, 0, 2), (12, 0, 1)]


# ---------------------------------------------------------------------------
# CONSTRUCTEUR
# ---------------------------------------------------------------------------

class TestClusteringMeasuresConstructor(unittest.TestCase):
    """Le constructeur accepte une liste de ClusterPoint ou un fichier."""

    def setUp(self):
        """
        Cree un dossier temporaire pour les fichiers de test. Il est supprime
        apres chaque test pour ne rien laisser sur le disque.
        """
        self.folder = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.folder)

    def write_file(self, text):
        """Ecrit un fichier dans le dossier temporaire et renvoie son chemin."""
        path = os.path.join(self.folder, "points.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return path

    def test_constructor_from_list(self):
        """
        c'est l'usage principal : on donne directement la liste des
        ClusterPoint (par exemple le resultat d'un Kmeans). On verifie que
        l'objet est cree et garde tous les points.
        """
        points = make_cluster_points(GOOD_CLUSTERING)
        measures = ClusteringMeasures(points)
        self.assertIsInstance(measures, ClusteringMeasures)
        self.assertEqual(len(measures.cluster_point_list), 4)

    def test_sample_file_of_the_project(self):
        """
        test d'usage : le sujet fournit le fichier angle_1TEY_small_clust.txt
        pour travailler. Il commence par une ligne d'en-tete (phi psi cluster),
        comme celui ecrit par create_tsv. On verifie que ce vrai fichier est lu.
        """
        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(here, "..", "3.STATS", "angle_1TEY_small_clust.txt")
        measures = ClusteringMeasures(path)
        self.assertGreater(len(measures.cluster_point_list), 0)

    def test_not_a_list_none(self):
        """
        None (valeur oubliee) n'est ni une liste ni un chemin : une erreur
        claire est attendue.
        """
        with self.assertRaises((ValueError, TypeError)):
            ClusteringMeasures(None)

    def test_not_a_list_number(self):
        """
        un nombre n'est ni une liste ni un chemin de fichier : il doit etre
        refuse.
        """
        with self.assertRaises((ValueError, TypeError)):
            ClusteringMeasures(5)

    def test_file_does_not_exist(self):
        """
        un chemin qui ne mene a aucun fichier doit donner une erreur
        (FileNotFoundError), pas un objet vide.
        """
        path = os.path.join(self.folder, "n_existe_pas.txt")
        with self.assertRaises(OSError):
            ClusteringMeasures(path)


# ---------------------------------------------------------------------------
# DISTANCE
# ---------------------------------------------------------------------------

class TestClusteringMeasuresDistance(unittest.TestCase):
    """La methode _dist calcule la distance euclidienne entre deux points."""

    def test_dist_3_4_5(self):
        """
        le triangle 3-4-5 est le cas classique : la distance entre (0,0)
        et (3,4) doit valoir exactement 5.
        """
        p = ClusterPoint(0, 0, 1)
        q = ClusterPoint(3, 4, 1)
        self.assertEqual(ClusteringMeasures._dist(p, q), 5)

    def test_dist_same_point_is_zero(self):
        """
        la distance d'un point a lui-meme est nulle.
        """
        p = ClusterPoint(2, 7, 1)
        self.assertEqual(ClusteringMeasures._dist(p, p), 0)

    def test_dist_is_symmetric(self):
        """
        la distance de p a q doit etre la meme que celle de q a p.
        """
        p = ClusterPoint(1, 2, 1)
        q = ClusterPoint(-4, 6, 2)
        self.assertEqual(ClusteringMeasures._dist(p, q),
                         ClusteringMeasures._dist(q, p))


# ---------------------------------------------------------------------------
# COEFFICIENT DE SILHOUETTE
# ---------------------------------------------------------------------------

class TestSilhouette(unittest.TestCase):
    """Coefficient de silhouette : de -1 (pire) a 1 (meilleur)."""

    def test_good_clustering_exact_value(self):
        """
        cas calcule a la main. Pour chaque point, a = distance moyenne aux
        points de son groupe, b = distance moyenne au groupe voisin,
        s = (b - a) / max(a, b).
            (0,0)  : a=2, b=11 -> 9/11        (2,0)  : a=2, b=9  -> 7/9
            (10,0) : a=2, b=11 -> 9/11        (12,0) : a=2, b=9  -> 7/9
        La moyenne vaut (9/11 + 7/9) / 2 = 0.79798 (a peu pres).
        """
        measures = ClusteringMeasures(make_cluster_points(GOOD_CLUSTERING))
        expected = (9 / 11 + 7 / 9) / 2
        self.assertAlmostEqual(compute_silhouette(measures), expected, places=6)

    def test_bad_clustering_exact_value(self):
        """
        meme jeu de 4 points mais mal classes. Calcul a la main :
            (0,0) : a=12, b=6 -> -0.5     (12,0) : a=12, b=6 -> -0.5
            (2,0) : a=8,  b=6 -> -0.25    (10,0) : a=8,  b=6 -> -0.25
        La moyenne vaut -0.375 : negative, car les points sont plus proches du
        groupe voisin que du leur.
        """
        measures = ClusteringMeasures(make_cluster_points(BAD_CLUSTERING))
        self.assertAlmostEqual(compute_silhouette(measures), -0.375, places=6)

    def test_bad_clustering_is_negative(self):
        """
        regle du sujet : un resultat negatif veut dire "mal classe". On
        verifie simplement le signe sur le mauvais clustering.
        """
        measures = ClusteringMeasures(make_cluster_points(BAD_CLUSTERING))
        self.assertLess(compute_silhouette(measures), 0)


    def test_value_between_minus_one_and_one(self):
        """
        quelle que soit la donnee, le coefficient est borne : entre -1 et 1.
        On teste le bon et le mauvais clustering.
        """
        for data in [GOOD_CLUSTERING, BAD_CLUSTERING]:
            measures = ClusteringMeasures(make_cluster_points(data))
            value = compute_silhouette(measures)
            self.assertGreaterEqual(value, -1)
            self.assertLessEqual(value, 1)



# ---------------------------------------------------------------------------
# INDICE DE DUNN
# ---------------------------------------------------------------------------

class TestDunn(unittest.TestCase):
    """
    Indice de Dunn = plus petite distance entre deux clusters (entre leurs
    deux points les plus proches) / plus grand diametre de cluster (distance
    entre ses deux points les plus eloignes). Plus il est grand, mieux c'est.
    """

    def test_good_clustering_exact_value(self):
        """
        cas calcule a la main : diametres = 2 et 2 ; plus petite distance entre
        les clusters = 10 - 2 = 8. Donc DI = 8 / 2 = 4.
        """
        measures = ClusteringMeasures(make_cluster_points(GOOD_CLUSTERING))
        self.assertAlmostEqual(compute_dunn(measures), 4.0, places=6)

    def test_bad_clustering_exact_value(self):
        """
        clustering melange : diametres = 12 et 8 ; plus petite distance entre
        clusters = 2 (entre (0,0) et (2,0)). Donc DI = 2 / 12 = 0.1667 environ.
        """
        measures = ClusteringMeasures(make_cluster_points(BAD_CLUSTERING))
        self.assertAlmostEqual(compute_dunn(measures), 2 / 12, places=6)

    def test_three_clusters_exact_value(self):
        """
        trois clusters : (0,0)(1,0) / (10,0)(11,0) / (0,20)(0,21).
        Tous les diametres valent 1. Les distances entre clusters sont 9, 20 et
        environ 22.4 : la plus petite est 9. Donc DI = 9 / 1 = 9.
        """
        data = [(0, 0, 1), (1, 0, 1), (10, 0, 2), (11, 0, 2),
                (0, 20, 3), (0, 21, 3)]
        measures = ClusteringMeasures(make_cluster_points(data))
        self.assertAlmostEqual(compute_dunn(measures), 9.0, places=6)

    def test_value_is_positive(self):
        """
        l'indice est un rapport de distances : il ne peut pas etre negatif.
        """
        measures = ClusteringMeasures(make_cluster_points(BAD_CLUSTERING))
        self.assertGreater(compute_dunn(measures), 0)

if __name__ == "__main__":
    unittest.main()
