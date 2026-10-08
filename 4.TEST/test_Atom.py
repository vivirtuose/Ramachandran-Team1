import unittest
import math
from Atom import Atom

def almost_equal(number_1, number_2, threshold=1E-2):
    """
    Calcul si 2 valeurs numeriques sont egale a threshold pret.
    Parameters
    ----------
        number_1 : le premier nombre a comparer
        number_2 : le second nombre a comparer
        threshold : en dessous de quelle distance ont considere les nombres egaux

    Returns
    -------
        bool : True si les 2 nombres sont considere comme egaux.
    """
    return abs((number_1) - (number_2)) < threshold

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
        self.assertIs(f.name, str)

    def test_atom_getter_name_work(self):
        """
        Test si le getter de name rend bien l'attribut donnee.
        """
        f = Atom("N", 1, 0, 0)
        self.assertEqual(f.name, "N")

    #################
    #   GET_COORDS  #
    #################
    def test_atom_get_coords_return_list(self):
        """
        Test si le getter de coords rend bien une liste.
        """
        f = Atom("N", 1, 0, 0)
        self.assertIs(f.coords, list)  

    def test_atom_get_coords_return_list(self):
        """
        Test si le getter de coords rend bien des nombres.
        """
        f = Atom("N", 1, 0, 0)
        self.assertTrue(all([ isinstance(n, (int, float)) for n in f.coords]))      

    def test_atom_get_coords_order(self):
        """
        Test si le getter de coords rend bien la liste de coordonnees dans l'ordre x, y, z.
        """
        f = Atom("N", 1, 2, 3)
        self.assertEqual(f.coords, [1, 2, 3]) 

    #############
    #   GET_X   #
    #############
    def test_atom_get_x_number(self):
        """
        Test si le getter de x rend un nombre.
        """
        f = Atom("N", 1, 0, 0)
        self.assertIsInstance(f.x, (int, float), f'\n{type(f.x)=}')

    def test_atom_get_x_works(self):
        """
        Test si le getter de x rend le bon nombre.
        """
        f = Atom("N", 1, 2, 3)
        self.assertEqual(f.x, 1)

    #############
    #   GET_Y   #
    #############
    def test_atom_get_y_number(self):
        """
        Test si le getter de y rend un nombre.
        """
        f = Atom("N", 1, 0, 0)
        self.assertIsInstance(f.y, (int, float), f'\n{type(f.y)=}')

    def test_atom_get_y_works(self):
        """
        Test si le getter de y rend le bon nombre.
        """
        f = Atom("N", 1, 2, 3)
        self.assertEqual(f.y, 2)


    #############
    #   GET_Z   #
    #############
    def test_atom_get_z_number(self):
        """
        Test si le getter de z rend un nombre.
        """
        f = Atom("N", 1, 0, 0)
        self.assertIsInstance(f.z, (int, float), f'\n{type(f.z)=}')

    def test_atom_get_z_works(self):
        """
        Test si le getter de z rend le bon nombre.
        """
        f = Atom("N", 1, 2, 3)
        self.assertEqual(f.z, 3)

    #############
    #   COPY    #
    #############
    def test_atom_copy_name(self):
        """
        Test si la methode copy copie bien le nom de l atome.
        """
        f = Atom("N", 1, 2, 3)
        g = Atom("CA", 2, 3, 4)
        f.copy(g)
        self.assertTrue(g.name == f.name)
    
    def test_atom_copy_coords(self):
        """
        Test si la methode copy copie bien les coordonees de l atome.
        """
        f = Atom("N", 1, 2, 3)
        g = Atom("CA", 2, 3, 4)
        f.copy(g)
        self.assertTrue(g.coords == f.coords)

    def test_atom_copy_works(self):
        """
        Test si la copie contient les memes valeurs d'attributs.
        """
        f = Atom("N", 1, 2, 3)
        g = Atom("CA", 2, 3, 4)
        f.copy(g)
        result = [g.name == f.name, g.coords == f.coords]
        self.assertTrue(all(result))

    def test_atom_copy_not_same_instance(self):
        """
        Vérifie que la copie est bien une instance separe.
        """
        f = Atom("N", 1, 2, 3)
        g = Atom("CA", 2, 3, 4)
        f.copy(g)
        g.name = "CA"
        g.coords = (1, 2, 2)
        result = [g.name != f.name, g.coords != f.coords]
        self.assertTrue(all(result))            

   ############
   # SET_NAME #
   ############
    def test_atom_set_works(self):
        """
        Test si le setter de name change bien le nom.
        """
        f = Atom("N", 1, 1, 1)
        f.name = "C"
        self.assertTrue(f.name == "C")

    def test_atom_set_name_incorrect(self):
        """
        test si le setter de name accepte les nom incorrect.
        """
        f = Atom("N", 1, 0, 0)
        with self.assertRaises(ValueError):
            f.name = "X"

    def test_atom_set_name_modify_rest(self):
        """
        Test si l'utilisation du setter change juste le name et pas le reste.
        """
        g = Atom("N", 1, 1, 1)
        g.name = "C"
        self.assertTrue(g.name == "C" and g.coords == [1, 1, 1])

    ##############
    # SET_COORDS #
    ##############
    def test_atom_set_coords_works(self):
        """
        Test si le setter de coords modifie bien les coords.
        """
        f = Atom("N", 1, 0, 0)
        f.coords = (1, 2, 3)
        self.assertEqual(f.coords, [1, 2, 3]) 

    def test_atom_set_coords_incorrect(self):
        """
        Test si le setter de coords accepte des valeurs qui ne sont pas des nombres.
        """      
        f = Atom("N", 1, 0, 0)
        with self.assertRaises(ValueError):
            f.coords = ('a', 'b', 'c')   

    def test_atom_set_coords_modify_rest(self):
        """
        Verifie que le setter de coords ne modifie pas les coords.
        """
        g = Atom("N", 1, 1, 1)
        g.coords = (1, 2, 3)
        self.assertTrue(g.name == "N" and g.coords == [1, 2, 3])

    ############
    #   STR    #
    ############
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

    #############
    #   NORM    #
    #############
    def test_norm_return_number(self):
        """
        Test si la methode norm rend un nombre.
        """
        f = Atom("N", 0, 0, 0)
        result = f.norm()
        self.assertIsInstance(result, (int, float), f'\n{type(result)=}')

    def test_norm_0(self):
        """
        Test que la methode donne bien 0 si les coords sont (0, 0, 0).
        """
        f = Atom("N", 0, 0, 0)
        self.assertEqual(f.norm(), 0)

    def test_norm_1(self):
        """
        Test que la bonne methode donne bien 1 si les coords sont positives (1, 0, 0).
        """
        f = Atom("N", 1, 0, 0)
        self.assertEqual(f.norm(), 1)

    def test_norm_neg1(self):
        """
        Test que la methode donne bien 1 si les coords sont negatives (-1, 0, 0).
        """
        f = Atom("N", -1, 0, 0)
        self.assertEqual(f.norm(), 1)

    def test_norm_works_1(self):
        """
        Test que la methode rend la valeur attendue.
        """
        f = Atom("N", -1.115, 8.537, 7.075)
        self.assertTrue(almost_equal(f.norm(), 11.143572990742243), f'{f.norm()=}\nreal={11.143572990742243}')

    def test_norm_works_2(self):
        """
        Test que la methode rend la valeur attendue.
        """
        f = Atom("CA", -1.925, 7.470, 6.547)
        self.assertTrue(almost_equal(f.norm(), 10.117792941150752))

    #################
    #   DISTANCE    #
    #################
    def test_distance_return_number(self):
        """
        Test si la distance renvoie bien un nombre.
        """
        f = Atom("N", -1.115, 8.537, 7.075)
        g = Atom("CA", -1.925, 7.470, 6.547)
        result = f.distance(g)
        self.assertIsInstance(result, (float, int), f'{type(result)}')

    def test_distance_work_1(self):
        """
        Test que les distances renvoie la bonne valeur.
        """
        f = Atom("N", -1, 0, 0)
        g = Atom("CA", 1, 0, 0)
        result = f.distance(g)
        self.assertTrue(almost_equal(result, 2), f"\n{result=}\nReal=2")

    def test_distance_work_2(self):
        """
        Test que les distances renvoie la bonne valeur.
        """
        f = Atom("N", -1.115, 8.537, 7.075)
        g = Atom("CA", -1.925, 7.470, 6.547)
        result = f.distance(g)
        self.assertTrue(almost_equal(result, 1.4399211783983188), f"\n{result=}\nReal=1.4399211783983188")

    def test_distance_order(self):
        """
        Test que la methode distance fonctionne dans les 2 sens.
        """
        f = Atom("N", -1, 0, 0)
        g = Atom("CA", 1, 0, 0)
        result_1 = f.distance(g)
        result_2 = g.distance(f)
        self.assertTrue(result_1 == result_2)       

    #################
    #   SUBSTRACT   #
    #################
    def test_substract_return_type(self):
        """
        Tests si la methode substract de la class Atom rend bien un Atom.
        """
        f = Atom("N", 1, 0, 2)
        g = Atom("N", 2, 1, 0)
        result = f.substract(g)
        self.assertIsInstance(result, Atom)

    def test_substract_returns_name(self):
        """
        Test si la methode cross_porduct renvoie un Atom sans nom.
        """
        f = Atom("N", 1, 0, 2)
        g = Atom("N", 2, 1, 0)
        result = f.substract(g)
        self.assertTrue(result.name == "" or result.name == None)

    def test_substract_work(self):
        f = Atom("N", -1.115, 8.537, 7.075)
        g = Atom("CA", -1.925, 7.470, 6.547)
        result = f.substract(g)
        result_bool = [ almost_equal(n, real) for n, real in zip(result.coords, [0.81, 1.07, 0.53])] 
        self.assertTrue(all(result_bool), f'\n{result.coords=}\nReal=[0.81, 1.07, 0.53]')

    ####################
    #   DOT_PRODUCT    #
    ####################
    # resultat de test obtenus grace a numpy.dot(a,b)
    def test_dot_product_retun_float(self):
        """
        Test si la methode dot_product rend bien le resultat attendus/fonctionne.
        """
        f = Atom("N", -1, 8, 7)
        g = Atom("CA", -1, 7, 6)
        result = f.dot_product(g)
        self.assertIsInstance(result, float)

    def test_dot_product_work_1(self):
        """
        Test si la methode dot_product rend bien le resultat attendus/fonctionne.
        """
        f = Atom("N", -1, 8, 7)
        g = Atom("CA", -1, 7, 6)
        result = f.dot_product(g)
        self.assertAlmostEqual(result, 99.00)

    def test_dot_product_work_2(self):
        """
        Test si la methode dot_product rend bien le resultat attendus/fonctionne.
        """
        f = Atom("N", -1.115, 8.537, 7.075)
        g = Atom("CA", -1.925, 7.470, 6.547)
        result = f.dot_product(g)
        self.assertTrue(almost_equal(result,  112.23779), f'\n{result=}\nreal={112.23779}')

    #######################
    #   CROSS _PRODUCT    #
    #######################
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
        self.assertEqual(result.name, "")

    def test_cross_product_return_type_inside(self):
        """
        Tests si la methode cross_product de la class Atom rend bien des nombre pour coordonnees.
        """
        f = Atom("N", 1, 0, 2)
        g = Atom("N", 2, 1, 0)
        result = f.cross_product(g)
        list_bool = [type(number) == float or type(number) == int for number in result.coords]
        self.assertTrue(all(list_bool), f'\n{result.coords}\nIs a number={list_bool}')

    def test_cross_product_work_1(self):
        """
        Tests si la methode cross_product de la class Atom rend bien le resultat attendue.
        """
        f = Atom("N", 1, 0, 2)
        g = Atom("N", 2, 1, 0)
        result = f.cross_product(g)
        self.assertEqual(result.coords, [-2, 4, 1])

    def test_cross_product_work_2(self):
        """
        Tests si la methode cross_product de la class Atom rend bien le resultat attendue.
        """
        f = Atom("N", -1.115, 8.537, 7.075)
        g = Atom("CA", -1.925, 7.470, 6.547)
        result = f.cross_product(g)
        # On passe par un arrondissement pour diminuer les chances de faux a cause d'une faible difference.
        list_bool = [almost_equal(n, real) for n, real in zip(result.coords, [3.041489, -6.31947 ,  8.104675])]
        self.assertTrue(all(list_bool), f'\n{result.coords=}\nReal={[3.041489, -6.31947 ,  8.104675]}')

    #############
    #   ANGLE   #
    #############
    def test_angle_return_float(self):
        """
        Test si la methode angle rend bien un float.
        """
        f = Atom("N", -1.115, 8.537, 7.075)
        g = Atom("CA", -1.925, 7.470, 6.547)
        result = f.angle(g)
        self.assertIsInstance(result, (float, int), f'\n{type(result)=}')

    def test_angle_order(self):
        """
        Verifie si l ordre des atomes changes l angle.
        """
        f = Atom("N", -1.115, 8.537, 7.075)
        g = Atom("CA", -1.925, 7.470, 6.547)
        result_1 = f.angle(g)
        result_2 = g.angle(f)
        self.assertTrue(result_1 == result_2)

    def test_angle_work(self):
        """
        Test si la methode angle rend bien la bonne reponse.
        """
        f = Atom("N", -1.115, 8.537, 7.075)
        g = Atom("CA", -1.925, 7.470, 6.547)  
        self.assertTrue(almost_equal(f.angle(g), 0.09520358627719255), f'\n{f.norm()=}\nreal={0.09520358627719255}')

    
    #################
    #   DIHEDRAL    #
    #################
    # source des resultats
    # https://stackoverflow.com/questions/20305272/dihedral-torsion-angle-from-four-points-in-cartesian-coordinates-in-python
    def test_dihedral_return_number(self):
        """
        Test si la methode rend bien un nombre.
        """
        f = Atom("N", 24.969, 13.428, 30.692)
        g = Atom("N", 24.044, 12.661, 29.808)
        h = Atom("N", 22.785, 13.482, 29.543)
        i = Atom("N", 21.951, 13.670, 30.431)
        result = f.dihedral(g, h, i)
        self.assertIsInstance(result, (float, int), f"\n{type(result)=}")

    def test_dihedral_work_1(self):
        """
        Test si la methode rend le bon nombre a 10**-4 pret.
        """
        f = Atom("N", 24.969, 13.428, 30.692)
        g = Atom("N", 24.044, 12.661, 29.808)
        h = Atom("N", 22.785, 13.482, 29.543)
        i = Atom("N", 21.951, 13.670, 30.431)
        result = f.dihedral(g, h, i)
        self.assertTrue(almost_equal(result, -1.2429388648155737), f'\n{result=}\nreal=-1.2429388648155737') #radial -71.21515

    def test_dihedral_work_2(self):
        """
        Test si la methode rend le bon nombre.
        """
        f = Atom("N", 24.044, 12.661, 29.808)
        g = Atom("N", 23.672, 11.328, 30.466)
        h = Atom("N", 22.881, 10.326, 29.620)
        i = Atom("N", 23.691,  9.935, 28.389)
        result = f.dihedral(g, h, i)
        self.assertTrue(almost_equal(result, 1.0615488238319344), f'\n{result=}\nreal= 1.0615488238319344') #radial 60.82226


if __name__ == "__main__":
    unittest.main()