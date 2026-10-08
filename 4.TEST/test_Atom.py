import unittest
import math
from Atom import *

class Test_Atom(unittest.TestCase):

    ##############
    #  __INNIT__ #
    ##############
    def test_atom_innit_create_instance(self):
        """
        Test que la class Atom construit bien un objet.
        """
        f = Atom("N", 1, 0, 0)
        self.assertIsInstance(f, Atom)

    def test_atom_innit_name_incorrect(self):
        """
        Test que le constructeur n'accepte pas de nom impossible.
        """
        with self.assertRaises(ValueError):
            f = Atom("X", 1, 0, 0)

    def test_atom_innit_coords_incorrect(self):
        """
        Test que le constructeur n'accepte pas des coords impossible.
        """
        with self.assertRaises(ValueError):
            f = Atom("N", "a", 0, 0)

    #####################
    #    GET_NAME       #
    #####################
    def test_atom_getter_name_work(self):
        """
        test si le getter de name rend une string.
        """
        f = Atom("N", 1, 0, 0)
        self.assertIs(f.get_name(), str)

    def test_atom_getter_name_work(self):
        """
        Test si le getter de name rend bien l'attribut donnee.
        """
        f = Atom("N", 1, 0, 0)
        self.assertEqual(f.get_name(), "N")

    #################
    #   GET_COORDS  #
    #################
    def test_atom_get_coords_return_list(self):
        """
        Test si le getter de coords rend bien une liste.
        """
        f = Atom("N", 1, 0, 0)
        self.assertIs(f.get_coords(), list)  

    def test_atom_get_coords_return_list(self):
        """
        Test si le getter de coords rend bien des nombres.
        """
        f = Atom("N", 1, 0, 0)
        self.assertTrue(all([ isinstance(n, (int, float)) for n in f.get_coords()]))      

    def test_atom_get_coords_order(self):
        """
        Test si le getter de coords rend bien la liste de coordonnees dans l'ordre x, y, z.
        """
        f = Atom("N", 1, 2, 3)
        self.assertEqual(f.get_coords(), [1, 2, 3]) 

    #############
    #   GET_X   #
    #############
    # tests des setters
    def test_atom_setter_change_name(self):
        """
        test si le setter de name change le nom.
        """
        f = Atom("N", 1, 0, 0)
        f.set_name("CA")
        self.assertEqual(f.get_name(), "CA")

    def test_atom_set_name_incorrect(self):
        """
        test si le setter de name accepte les nom incorrect.
        """
        f = Atom("N", 1, 0, 0)
        with self.assertRaises(ValueError):
            f.set_name("X")

    def test_atom_set_name_modify_rest(self):
        """
        Test si l'utilisation du setter change juste le name et pas le reste.
        """
        f = Atom("N", 1, 0, 0)
        g = Atom("C", 1, 0, 0)
        f.set_name("C")
        self.assertEqual(f, g)

    def test_atom_set_coords_works(self):
        """
        Test si le setter de coords modifie bien les coords.
        """
        f = Atom("N", 1, 0, 0)
        f.set_coords(1, 2, 3)
        self.assertEqual(f.get_coords(), [1, 2, 3]) 

    def test_atom_set_coords_incorrect(self):
        """
        Test si le setter de coords accepte des valeurs qui ne sont pas des nombres.
        """      
        f = Atom("N", 1, 0, 0)
        with self.assertRaises(ValueError):
            f.set_coords('a', 'b', 'c')   

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
        self.assertEqual(str(f), "C (-3.00, -4.00, -2.00)")

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
    def test_distance_work(self):
        f = Atom("N", -1.115, 8.537, 7.075)
        g = Atom("CA", -1.925, 7.470, 6.547)
        result = f.distance(g)
        self.assertEqual(result, 1.4399211783983188)

    # Tests de la methode substract
    def test_substract_work(self):
        f = Atom("N", -1.115, 8.537, 7.075)
        g = Atom("CA", -1.925, 7.470, 6.547)
        result = f.substract(g)
        self.assertEqual(result.get_coords(), ( 0.81, 1.07, 0.53))

    # Tests de la methode dot_product
    f = Atom("N", -1.115, 8.537, 7.075)
    g = Atom("CA", -1.925, 7.470, 6.547)
    112.23779

    # Tests de la methode cross_product
    # https://www.dcode.fr/produit-vectoriel
    def test_cross_product_return_type(self):
        """
        Tests si la methode cross_product de la class Atom rend bien un Atom.
        """
        f = Atom("N", 1, 0, 2)
        g = Atom("N", 2, 1, 0)
        result = f.cross_product(g)
        self.assertIsInstance(result, Atom)

    def test_cross_product_returns_name(self):
        """
        Test si la methode cross_porduct renvoie un Atom sans nom.
        """
        f = Atom("N", 1, 0, 2)
        g = Atom("N", 2, 1, 0)
        result = f.cross_product(g)
        self.assertEqual(result.get_name(), "")

    def test_cross_product_return_type_inside(self):
        """
        Tests si la methode cross_product de la class Atom rend bien des float.
        """
        f = Atom("N", 1, 0, 2)
        g = Atom("N", 2, 1, 0)
        result = f.cross_product(g)
        list_bool = [type(number) == float for number in result.get_coords()]
        self.assertTrue(all(list_bool))

    def test_cross_product_work(self):
        """
        Tests si la methode cross_product de la class Atom rend bien des float.
        """
        f = Atom("N", 1, 0, 2)
        g = Atom("N", 2, 1, 0)
        result = f.cross_product(g)
        self.assertEqual(result.get_coords(), (-2, 4, 1))
    

    # Tests de la methode angle
    def test_angle_return_float(self):
        """
        Test si la methode angle rend bien un float.
        """
        f = Atom("N", -1.115, 8.537, 7.075)
        g = Atom("CA", -1.925, 7.470, 6.547)
        self.assertIs(f.angle(g), float)
        0.09520358627719255

    def test_angle_work(self):
        """
        Test si la methode angle rend bien la bonne reponse.
        """
        f = Atom("N", -1.115, 8.537, 7.075)
        g = Atom("CA", -1.925, 7.470, 6.547)
        self.assertEqual(f.angle(g), 0.09520358627719255)

    

    # tests de la methode dihedral

if __name__ == "__main__":
    unittest.main()