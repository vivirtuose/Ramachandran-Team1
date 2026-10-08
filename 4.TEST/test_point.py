import unittest
from Point import Point
from clustering_KMeans import ClusterPoint


class Test_Point(unittest.TestCase):

  def test_init_default(self):
    """
    Vérification de l'initialisation par défaut (0.0, 0.0)
    """
    p = Point()
    self.assertAlmostEqual(p.get_abs(), 0.0)
    self.assertAlmostEqual(p.get_ord(), 0.0)

  def test_init_values(self):
    """
    Vérification de l'initialisation avec des coordonnées
    """
    p = Point(3.5, -2,1)
    self.assertAlmostEqual(p.get_abs(), 3.5)
    self.assertAlmostEqual(p.get_ord(), -2.1)

  def test_init_invalid_types(self):
    """
    Vérification qu'il y à bien une erreure de levé si les coordonnées ne sont pas numériques
    """
    with self.assertRaises(TypeError):
      Point("3", 2)
    with self.assertRaises(TypeError):
      Point(1, None)

  def test_str(self):
    """ 
    Vérification du format de l'affichage __str__
    """
    p = Point(1.23456, -7.89012)
    expected_str = "Point of coordinates (1.2346, -7.8901)"
    self.assertEqual(str(p), expected_str)

  def test_add(self):
    """
    Vérification de l'ajout d'un autre point
    """
    p1 = Point(1.5, 2.5)
    p2 = Point(3.0, -1.0)
    p1.add(p2)
    self.assertAlmostEqual(p1.get_abs(), 4.5)
    self.assertAlmostEqual(p1.get_ord(), 1.5)

  def test_add_invalid_argument(self):
    """
    Vérification qu'on lève un message TypeError si on tente d'ajouter un objet qui ne fait pas partie de Point
    """
    p = Point(1, 1)
    with self.assertRaises(TypeError):
      p.add(5)
    with self.assertRaises(TypeError):
      p.add("Point")


  def test_rescale_positive_factor(self):
    """
    Vérification avec un facteur positif
    """
    p = Point(1, -2)
    p.rescale(3)
    self.assertEqual((p.get_abs(), p.get_ord()), (3, -6))

  def test_rescale_zero_factor(self):
    """
    Vérification avec le facteur 0
    """
    p = Point(4.0, 5.0)
    p.rescale(0)
    self.assertAlmostEqual(p.get_abs(), 0.0)
    self.assertAlmostEqual(p.get_ord(), 0.0)

  def test_rescale_invalid_factor(self):
    """
    Vérifie qu'un facteur non numérique lève une TypeError.
    """
    p = Point(1, 1)
    with self.assertRaises(TypeError):
      p.rescale("factor")

  def test_distance_origin(self):
    """
    Vérifie la distance par rapport à l'origine
    """
    self.assertEqual(Point(3, 4).distance_from_origin(), 5)
    self.assertEqual(Point(0, 0).distance_from_origin(), 0)

  def test_euclidean(self):
    """
    Vérifie la distance euclidienne entre deux points
    """
    self.assertEqual(Point(1, 1).euclidean_distance(Point(2, 1)), 1)
    self.assertEqual(Point(0, 0).euclidean_distance(Point(3, 4)), 5)
    self.assertEqual(Point(1, 1).euclidean_distance(Point(1, 1)), 0)

  def test_euclidean_distance_invalid_argument(self):
    """
    Vérifie qu'un argument invalide lève une TypeError
    """
    p = Point(1, 1)
    with self.assertRaises(TypeError):
      p.euclidean_distance((2, 2))

  def test_manhattan(self):
    """
    Vérifie la distance de manhattan entre deux points
    """
    self.assertEqual(Point(0, 0).manhattan_distance(Point(3, 4)), 7)
    self.assertEqual(Point(-1, -1).manhattan_distance(Point(1, 1)), 4)

  def test_manhattan_distance_invalid_argument(self):
    """
    Vérifie qu'un argument invalide lève une TypeError
    """
    p = Point(0, 0)
    with self.assertRaises(TypeError):
      p.manhattan_distance([1, 1])


if __name__ == "__main__":
  unittest.main()
