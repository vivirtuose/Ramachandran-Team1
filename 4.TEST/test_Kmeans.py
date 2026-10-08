"""
Tests unitaires et tests d'usage des classes Kmeans (fichier clustering.py).

"""
import random
import unittest

from Point import Point
from clustering_KMeans import Kmeans


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
    km.clusterize()                    # the method is called clusterize(), not run()
    return list(km.liste_k.values())   # liste_k is a dict {cluster number: points}


def run_dbscan(points, epsilon, minpoints):
    """Construit un Dbscan, le lance, et renvoie la liste des clusters (sans le bruit)."""
    db = Dbscan(points, epsilon, minpoints)
    db.run()
    return db.clusters


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
# KMEANS
# ---------------------------------------------------------------------------

class TestKmeansInvalid(unittest.TestCase):
    """Cas invalides : le programme doit refuser proprement les mauvais parametres."""

    def setUp(self):
        self.points = make_points(BLOB_A + BLOB_B)

#Nous allons utiliser assertRaises pour vérifier que l'exception est bien levée lorsque k est invalide. Cela permet de s'assurer que le code gère correctement les cas d'erreur et ne renvoie pas de résultats absurdes ou ne plante pas plus loin dans l'exécution. La fonction est innérente à la classe unittest.TestCase et est utilisée pour tester les exceptions attendues dans le code.

    def test_k_zero(self):
        """
        k = 0 voudrait dire "zero groupe", ce qui n'a aucun sens.
        Le contrat de la classe impose 1 <= k. On verifie qu'une erreur est levee
        au lieu de renvoyer un resultat absurde ou de planter plus loin.
        """
        with self.assertRaises((ValueError, TypeError)): 
            run_kmeans(self.points, 0)

    def test_k_negative(self):
        """
        un nombre de groupes negatif est impossible. Meme principe que
        k = 0, mais on verifie que le test sur le signe est bien fait (k < 1).
        """
        with self.assertRaises((ValueError, TypeError)):
            run_kmeans(self.points, -3)

    def test_k_not_integer_float(self):
        """
        k doit etre un entier (on ne peut pas faire 2.5 groupes).
        On verifie qu'un float est refuse.
        """
        with self.assertRaises((ValueError, TypeError)):
            run_kmeans(self.points, 2.5)

    def test_k_not_integer_string(self):
        """
        k vient parfois d'un fichier ou d'un input() et reste du texte
        ("2"). Le programme ne doit pas accepter une chaine a la place d'un entier.
        """
        with self.assertRaises((ValueError, TypeError)):
            run_kmeans(self.points, "2")

    def test_k_greater_than_number_of_points(self):
        """
        on ne peut pas faire plus de groupes qu'il n'y a de points
        (le contrat dit k <= nombre de points). 8 points et k = 9 doit etre refuse.
        """
        with self.assertRaises((ValueError, TypeError)):
            run_kmeans(self.points, 9)

    def test_empty_points_list(self):
        """
        le contrat demande une liste NON vide. Sans point il n'y a rien
        a regrouper. On verifie qu'une liste vide est refusee.
        """
        with self.assertRaises((ValueError, TypeError)):
            run_kmeans([], 1)


class TestKmeansPartition(unittest.TestCase):
    """Le resultat doit toujours etre une vraie partition des points."""

    def setUp(self):
        """ setUp est execute avant chaque test pour preparer les donnees, son role est de assurer que chaque test commence avec un état propre et cohérent, évitant ainsi les interférences entre les tests. On utilise blob_a et blob_b pour créer un ensemble de points de test, et on ajoute deux points isolés pour vérifier que l'algorithme gère correctement les cas où certains points sont éloignés des clusters principaux. 
        """
        self.coordinates = BLOB_A + BLOB_B + [(50, 50), (51, 50)]
        self.points = make_points(self.coordinates)

    def test_number_of_groups_is_k(self):
        """
        c'est la promesse de base de Kmeans, on demande k groupes
        et on doit en recevoir exactement k. On teste k = 1, 2, 3 et 4.
        """
        for k in [1, 2, 3, 4]:
            clusters = run_kmeans(self.points, k)
            self.assertEqual(len(clusters), k)

#assertEqual est une méthode de la classe unittest.TestCase qui compare deux valeurs et échoue le test si elles ne sont pas égales. Elle est utilisée ici pour vérifier que le nombre de groupes renvoyé par l'algorithme Kmeans correspond bien à la valeur attendue k, garantissant ainsi que l'algorithme respecte le contrat de création de k clusters.

    def test_sum_of_sizes_is_number_of_points(self):
        """
        si la somme des tailles des groupes est differente du nombre
        de points, alors on a perdu ou duplique des points. Cela detecte les bugs
        les plus frequents (point oublie lors de l'affectation).
        """
        clusters = run_kmeans(self.points, 3)
        self.assertEqual(count_points(clusters), len(self.points))

    def test_each_point_in_exactly_one_group(self):
        """
        un point ne doit etre ni perdu, ni present dans deux groupes.
        On compare la liste triee des coordonnees en sortie avec celle en entree :
        elles doivent etre identiques (meme points, chacun une seule fois).
        """
        clusters = run_kmeans(self.points, 3)
        expected = sorted(self.coordinates)
        self.assertEqual(all_coords(clusters), expected)

    def test_no_empty_group(self):
        """
        un groupe vide n'a pas de sens pour l'utilisateur (et casserait
        le calcul d'un centroide, division par zero). Avec des donnees bien
        reparties, aucun des k groupes ne doit etre vide.
        """
        clusters = run_kmeans(self.points, 3) 
        for group in clusters:
            self.assertGreater(len(group), 0)

#(self.points, 3) veut dire que l'on demande à l'algorithme de créer 3 groupes à partir de l'ensemble de points self.points. L'algorithme Kmeans va donc tenter de partitionner ces points en 3 clusters distincts, en fonction de leur proximité dans l'espace des coordonnées. Le test vérifie ensuite que chacun de ces clusters contient au moins un point, garantissant ainsi qu'aucun cluster n'est vide après l'exécution de l'algorithme avec assertGreater(len(group), 0) qui vérifie que la taille de chaque groupe est supérieure à zéro.

    def test_result_is_list_of_lists(self):
        """
        le sujet dit que le resultat est "une liste de k listes".
        Les autres classes (ClusteringMeasures, sortie fichier) comptent sur ce
        format, donc on verifie le type.
        """
        clusters = run_kmeans(self.points, 2)
        self.assertIsInstance(clusters, list)
        for group in clusters:
            self.assertIsInstance(group, list)



class TestKmeansKnownSolution(unittest.TestCase):
    """Cas ou on connait la bonne reponse a l'avance."""

    def test_k1_one_group_with_all_points(self):
        """
        cas limite k = 1. Il n'y a qu'un seul groupe, qui doit contenir
        tous les points (son centroide est alors la moyenne de tous les points).
        """
        points = make_points(BLOB_A + BLOB_B)
        clusters = run_kmeans(points, 1)
        self.assertEqual(len(clusters), 1)
        self.assertEqual(coords_of(clusters[0]), sorted(BLOB_A + BLOB_B))

    def test_k_equals_n_each_point_alone(self):
        """
        cas limite k = n. Chaque point doit se retrouver seul dans son
        groupe. On verifie qu'il y a n groupes de taille 1.
        """
        points = make_points(BLOB_A)
        clusters = run_kmeans(points, 4)
        self.assertEqual(len(clusters), 4)
        for group in clusters:
            self.assertEqual(len(group), 1)

    def test_single_point_k1(self):
        """
        plus petit jeu de donnees possible. Un seul point et k = 1
        doit donner un groupe contenant ce point, sans erreur.
        """
        points = make_points([(3, 4)])
        clusters = run_kmeans(points, 1)
        self.assertEqual(len(clusters), 1)
        self.assertEqual(coords_of(clusters[0]), [(3, 4)])

    def test_all_identical_points_no_crash(self):
        """
        si tous les points sont identiques, les distances valent 0 et
        les centroides sont confondus. C'est la que l'on risque une division par
        zero ou une boucle infinie. On demande seulement que le programme ne
        plante pas et ne perde aucun point.
        """
        points = make_points([(2, 2), (2, 2), (2, 2), (2, 2)])
        clusters = run_kmeans(points, 2)
        self.assertEqual(count_points(clusters), 4)

    def test_four_corners_of_a_square_k4(self):
        """
        cas classique a solution connue avec k = n = 4 : les quatre
        coins d'un carre doivent etre chacun dans un groupe different.
        """
        points = make_points([(0, 0), (0, 10), (10, 0), (10, 10)])
        clusters = run_kmeans(points, 4)
        self.assertEqual(canonical(clusters),
                         [[(0, 0)], [(0, 10)], [(10, 0)], [(10, 10)]])


if __name__ == "__main__":
    unittest.main()
