"""
Tests unitaires et tests d'usage de la classe ClusteringMethods
(fichier clustering.py).
"""
import inspect
import unittest

from Point import Point
from clustering import ClusteringMethods, Kmeans, Dbscan


# ---------------------------------------------------------------------------
# Fonctions utilitaires (simples, communes a tous les tests)
# ---------------------------------------------------------------------------

def make_points(coordinates):
    """Transforme une liste de tuples (x, y) en liste de Point."""
    points = []
    for (x, y) in coordinates:
        points.append(Point(x, y))
    return points


def count_points(clusters):
    """Renvoie le nombre total de points dans tous les groupes."""
    total = 0
    for group in clusters:
        total = total + len(group)
    return total


# Deux blobs tres eloignes l'un de l'autre (utilises dans plusieurs tests)
BLOB_A = [(0, 0), (0, 1), (1, 0), (1, 1)]
BLOB_B = [(100, 100), (100, 101), (101, 100), (101, 101)]


# ---------------------------------------------------------------------------
# CLASSE ABSTRAITE
# ---------------------------------------------------------------------------

class TestClusteringMethodsAbstract(unittest.TestCase):
    """ClusteringMethods est un modele : on ne doit pas pouvoir l'utiliser seule."""

    def test_class_is_abstract(self):
        """
        le sujet demande une classe ABSTRAITE. On verifie que Python la
        reconnait comme abstraite (elle contient au moins une methode abstraite).
        """
        self.assertTrue(inspect.isabstract(ClusteringMethods))

    def test_cannot_instantiate_directly(self):
        """
        une classe abstraite n'est qu'un modele, elle ne sait pas
        clusteriser. Creer directement un objet ClusteringMethods doit donc
        lever une erreur (TypeError).
        """
        with self.assertRaises(TypeError):
            ClusteringMethods()

    def test_incomplete_subclass_cannot_be_instantiated(self):
        """
        une classe fille qui n'ecrit pas les methodes abstraites reste
        abstraite. On cree une fille vide : elle ne doit pas pouvoir etre
        instanciee. Cela prouve que la classe mere oblige bien ses filles a
        ecrire leur propre algorithme.
        """
        class EmptyChild(ClusteringMethods):
            pass

        with self.assertRaises(TypeError):
            EmptyChild()


# ---------------------------------------------------------------------------
# HERITAGE
# ---------------------------------------------------------------------------

class TestClusteringMethodsInheritance(unittest.TestCase):
    """Kmeans et Dbscan doivent bien etre des filles de ClusteringMethods."""

    def setUp(self):
        """
        Prepare une liste de points et un objet de chaque sorte avant chaque test.
        """
        self.points = make_points(BLOB_A + BLOB_B)
        self.km = Kmeans(self.points, 2)
        self.db = Dbscan(self.points, 2, 3)

    def test_kmeans_is_subclass(self):
        """
        le sujet dit que Kmeans herite de ClusteringMethods. On le verifie
        sur la classe elle-meme.
        """
        self.assertTrue(issubclass(Kmeans, ClusteringMethods))

    def test_dbscan_is_subclass(self):
        """
        meme verification pour Dbscan.
        """
        self.assertTrue(issubclass(Dbscan, ClusteringMethods))

    def test_kmeans_instance_is_clustering_method(self):
        """
        un objet Kmeans doit aussi etre reconnu comme un
        ClusteringMethods (c'est ce qui permet de les traiter pareil plus tard).
        """
        self.assertIsInstance(self.km, ClusteringMethods)

    def test_dbscan_instance_is_clustering_method(self):
        """
        meme verification pour un objet Dbscan.
        """
        self.assertIsInstance(self.db, ClusteringMethods)

    def test_kmeans_is_not_abstract(self):
        """
        Kmeans doit avoir ecrit toutes les methodes abstraites : elle doit
        etre une classe concrete, utilisable. Sinon on ne pourrait pas creer
        d'objet (le setUp aurait deja plante).
        """
        self.assertFalse(inspect.isabstract(Kmeans))

    def test_dbscan_is_not_abstract(self):
        """
        meme verification pour Dbscan.
        """
        self.assertFalse(inspect.isabstract(Dbscan))


# ---------------------------------------------------------------------------
# INTERFACE COMMUNE
# ---------------------------------------------------------------------------

class TestClusteringMethodsCommonInterface(unittest.TestCase):
    """Les deux methodes de clustering s'utilisent exactement de la meme facon."""

    def setUp(self):
        """
        Prepare une liste de points et les deux objets. On les met dans une
        liste pour pouvoir faire la meme verification sur les deux avec une boucle.
        """
        self.points = make_points(BLOB_A + BLOB_B)
        self.methods = [Kmeans(self.points, 2), Dbscan(self.points, 2, 3)]

    def test_both_have_run_method(self):
        """
        l'interet de la classe mere est que toutes les filles aient la
        meme methode run(). On verifie que Kmeans et Dbscan en ont une.
        """
        for method in self.methods:
            self.assertTrue(hasattr(method, "run"))
            self.assertTrue(callable(method.run))

    def test_both_store_the_points(self):
        """
        le sujet dit que la liste des Point fait partie des attributs des
        deux classes. On verifie que la liste donnee au constructeur est bien
        gardee, avec le meme nombre de points.
        """
        for method in self.methods:
            self.assertEqual(len(method.points), len(self.points))

    def test_both_give_clusters_as_list_of_lists(self):
        """
        apres run(), les deux methodes doivent donner leur resultat dans
        .clusters, sous la forme d'une liste de listes. Les autres classes
        (ClusterPoint, ClusteringMeasures, sortie fichier) comptent sur ce
        format commun.
        """
        for method in self.methods:
            method.run()
            self.assertIsInstance(method.clusters, list)
            for group in method.clusters:
                self.assertIsInstance(group, list)

    def test_both_never_return_more_points_than_given(self):
        """
        quelle que soit la methode, on ne doit jamais recevoir plus de
        points qu'on en a donne (pas de point invente ni duplique). Pour Dbscan,
        le bruit peut faire qu'on en recoit moins, mais jamais plus.
        """
        for method in self.methods:
            method.run()
            self.assertLessEqual(count_points(method.clusters), len(self.points))

    def test_both_find_two_groups_on_two_far_blobs(self):
        """
        test d'usage : on utilise Kmeans et Dbscan de la meme maniere sur les
        memes donnees (deux blobs tres eloignes). Les deux doivent trouver 2
        groupes, ce qui montre que l'interface commune fonctionne.
        """
        for method in self.methods:
            method.run()
            self.assertEqual(len(method.clusters), 2)


if __name__ == "__main__":
    unittest.main()
