import unittest
import math
from Atom import *

class Test_Atom(unittest.TestCase):


    #  Tests le constructeur
    def test_constructeur_construct_instance(self):
        """
        Test que la class Atom construit bien un objet.
        """
        f = Atom("N", 1, 0, 0)
        self.assertIsInstance(f, Atom)

    # Tests de la methode str
    def test_str_0(self):
        """
        Test que la class Atom peut rendre un str.
        """
        f = Atom("N", 0, 0, 0)
        self.assertIsInstance(str(f), str)

    def test_str_0(self):
        """
        Test que la class Atom rend un str aux bon format avec des 0.
        """
        f = Atom("N", 0, 0, 0)
        self.assertEqual(str(f), "N (0.00, 0.00, 0.00)")

    def test_str_round_2f_pos(self):
        """
        Test que le str de la class Atom rend bien des chiffres positifs arrondis a 2 nombre apres la virgule. 
        """
        f = Atom("O", 3.6666, 2.5555, 1.44444)
        self.assertEqual(str(f), "O (3.67, 2.56, 1.44)")

    def test_str_round_2f_neg(self):
        """
        Test que le str de la class Atom rend bien des chiffres negatifs arrondis a 2 nombre apres la virgule. 
        """
        f = Atom("C", -3, -4, -2)
        self.assertEqual(str(f), "C (-3.00), -4.00, -2.00)")

    #  Tests de la methode norm.
    def test_norm_0(self):
        f = Atom("N", 0, 0, 0)
        self.assertEqual(f.norm(), 0)

    def test_norm_1(self):
        f = Atom("N", 1, 0, 0)
        self.assertEqual(f.norm(), 1)

    def test_norm_neg1(self):
        f = Atom("N", -1, 0, 0)
        self.assertEqual(f.norm(), 1)

    def test_norm_neg1(self):
        f = Atom("N", -1.115, 8.537, 7.075)
        self.assertEqual(f.norm(), 11.143572990742243)

    def test_norm_neg1(self):
        f = Atom("CA", -1.925, 7.470, 6.547)
        self.assertEqual(f.norm(), 10.117792941150752)

    def test_norm_pos(self):
        f = Atom("N", 1, 2, 3)
        self.assertEqual(f.norm(), round(math.sqrt(14), 15))
    
    # Tests de la methode distance

    # Tests de la methode substract

    # Tests de la methode dot_product

    # Tests de la methode cross_product
    # https://www.dcode.fr/produit-vectoriel
    def test_cross_product_return_type(self):
        """
        Tests si la methode cross_product de la class Atom rend bien une '...'.
        """
        f = Atom("N", 1, 0, 2)
        g = Atom("N", 2, 1, 0)
        pass

    def test_cross_product_return_type_inside(self):
        """
        Tests si la methode cross_product de la class Atom rend bien des float.
        """
        f = Atom("N", 1, 0, 2)
        g = Atom("N", 2, 1, 0)
        result = f.cross_product(g)
        list_bool = [type(number) == float for number in result]
        self.assertEqual(list_bool, [True, True, True])

    def test_cross_product_work(self):
        """
        Tests si la methode cross_product de la class Atom rend bien des float.
        """
        f = Atom("N", 1, 0, 2)
        g = Atom("N", 2, 1, 0)
        result = f.cross_product(g)
        self.assertEqual(result, (-2, 4, 1))
    

    # Tests de la methode angle

    # tests de la methode dihedral

if __name__ == "__main__":
    unittest.main()