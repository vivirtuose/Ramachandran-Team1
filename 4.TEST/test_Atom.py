import unittest
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

    # Tests de la methode
    
    # Tests de la methode distance

    # Tests de la methode substract

    # Tests de la methode dot_product

    # Tests de la methode cross_product

    # Tests de la methode angle

    # tests de la methode dihedral
unittest.main()