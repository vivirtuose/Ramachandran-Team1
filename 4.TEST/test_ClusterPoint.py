"""
Tests unitaires et tests d'usage de la classe ClusterPoint (fichier clustering.py).

ClusterPoint est un Point qui garde en plus le numero du cluster auquel il
appartient : ClusterPoint(x, y, nb_cluster). Elle sert a stocker le resultat d'un
clustering (Kmeans, dbscan) et d'entree a ClusteringMeasures.
"""
import unittest

from Point import Point
from clustering import ClusterPoint


# ---------------------------------------------------------------------------
# CONSTRUCTEUR
# ---------------------------------------------------------------------------

class TestClusterPointConstructor(unittest.TestCase):
    """Le constructeur prend une abscisse, une ordonnee et un numero de cluster."""

    def test_constructor_creates_instance(self):
        """
        on verifie qu'un ClusterPoint se construit bien avec 3 valeurs.
        """
        p = ClusterPoint(1, 2, 3)
        self.assertIsInstance(p, ClusterPoint)

    def test_constructor_cluster_zero(self):
        """
        Kmeans numerote ses clusters a partir de 0. Le numero 0 est "faux" en
        Python : on verifie qu'il est bien garde et qu'il n'est pas remplace par
        None ou par une valeur par defaut.
        """
        p = ClusterPoint(1, 1, 0)
        self.assertEqual(p.nb_cluster, 0)

    def test_constructor_missing_cluster_number(self):
        """
        le numero de cluster est obligatoire : sans lui, ce ne serait plus un
        ClusterPoint. Le constructeur doit refuser les deux seules coordonnees.
        """
        with self.assertRaises(TypeError):
            ClusterPoint(1, 2)


# ---------------------------------------------------------------------------
# HERITAGE
# ---------------------------------------------------------------------------

class TestClusterPointInheritance(unittest.TestCase):
    """ClusterPoint doit se comporter comme un Point."""

    def test_is_subclass_of_point(self):
        """
        le sujet dit que ClusterPoint herite de Point. On le verifie sur la
        classe.
        """
        self.assertTrue(issubclass(ClusterPoint, Point))

    def test_instance_is_a_point(self):
        """
        un ClusterPoint doit etre accepte partout ou on attend un Point (par
        exemple dans euclidean_distance, qui verifie le type de son argument).
        """
        p = ClusterPoint(1, 2, 3)
        self.assertIsInstance(p, Point)

    def test_str_returns_text(self):
        """
        str() est herite de Point : on verifie simplement qu'il renvoie bien un
        texte et ne plante pas.
        """
        p = ClusterPoint(1.23456, 2, 3)
        self.assertIsInstance(str(p), str)

    def test_distance_from_origin(self):
        """
        la distance a l'origine est heritee de Point : le point (3, 4) est a une
        distance de 5.
        """
        p = ClusterPoint(3, 4, 1)
        self.assertEqual(p.distance_from_origin(), 5)

    def test_euclidean_distance_between_cluster_points(self):
        """
        distance euclidienne entre deux ClusterPoint : (0,0) et (3,4) sont a
        une distance de 5.
        """
        p = ClusterPoint(0, 0, 1)
        q = ClusterPoint(3, 4, 2)
        self.assertEqual(p.euclidean_distance(q), 5)

    def test_manhattan_distance(self):
        """
        distance de Manhattan heritee de Point : entre (0,0) et (3,4), elle
        vaut 3 + 4 = 7.
        """
        p = ClusterPoint(0, 0, 1)
        q = ClusterPoint(3, 4, 1)
        self.assertEqual(p.manhattan_distance(q), 7)

    def test_distance_ignores_cluster_number(self):
        """
        le numero de cluster ne doit jamais changer une distance : deux points
        aux memes coordonnees sont a la meme distance, qu'ils soient dans le meme
        cluster ou dans deux clusters differents.
        """
        origin = ClusterPoint(0, 0, 1)
        same_cluster = ClusterPoint(3, 4, 1)
        other_cluster = ClusterPoint(3, 4, 2)
        self.assertEqual(origin.euclidean_distance(same_cluster),
                         origin.euclidean_distance(other_cluster))

    def test_add_changes_coordinates_only(self):
        """
        add est herite de Point : il additionne les coordonnees. Le numero de
        cluster ne doit pas bouger.
        """
        p = ClusterPoint(1, 2, 5)
        p.add(Point(10, 20))
        self.assertEqual((p.x, p.y), (11, 22))
        self.assertEqual(p.nb_cluster, 5)

    def test_add_another_cluster_point_keeps_own_cluster(self):
        """
        quand on ajoute un ClusterPoint a un autre, le point modifie garde son
        propre numero de cluster (on n'additionne pas les numeros).
        """
        p = ClusterPoint(1, 1, 2)
        q = ClusterPoint(3, 3, 7)
        p.add(q)
        self.assertEqual((p.x, p.y), (4, 4))
        self.assertEqual(p.nb_cluster, 2)
        self.assertEqual(q.nb_cluster, 7)




# ---------------------------------------------------------------------------
# NUMERO DE CLUSTER (getter / setter)
# ---------------------------------------------------------------------------

class TestClusterPointClusterNumber(unittest.TestCase):
    """Le numero de cluster se lit et se modifie avec la propriete nb_cluster."""

    def test_setter_changes_cluster_number(self):
        """
        on peut changer le cluster d'un point (par exemple apres une nouvelle
        iteration de Kmeans). Le nouveau numero doit etre retrouve.
        """
        p = ClusterPoint(1, 2, 1)
        p.nb_cluster = 4
        self.assertEqual(p.nb_cluster, 4)

    def test_setter_does_not_change_coordinates(self):
        """
        changer le cluster ne doit pas toucher aux coordonnees.
        """
        p = ClusterPoint(1.5, -2.5, 1)
        p.nb_cluster = 9
        self.assertEqual((p.x, p.y), (1.5, -2.5))

    def test_setter_invalid_value(self):
        """
        le setter doit refuser une valeur qui n'est pas un entier, comme le
        constructeur. Sinon on pourrait contourner la verification en changeant
        le numero apres la creation.
        """
        p = ClusterPoint(1, 2, 1)
        with self.assertRaises((ValueError, TypeError)):
            p.nb_cluster = "abc"

    def test_cluster_numbers_are_independent(self):
        """
        deux points ne partagent pas leur numero de cluster : modifier l'un ne
        doit pas modifier l'autre.
        """
        p = ClusterPoint(0, 0, 1)
        q = ClusterPoint(0, 0, 1)
        p.nb_cluster = 2
        self.assertEqual(q.nb_cluster, 1)



if __name__ == "__main__":
    unittest.main()
