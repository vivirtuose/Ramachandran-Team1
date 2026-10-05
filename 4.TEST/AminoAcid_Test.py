import unittest
from AminoAcid import *
from Atom import *


class Test_AminoAcid(unittest.TestCase):

    def test_constructeur_construct_instance(self):

        AA = AminoAcid("SER", [("N", 1, 0, 0), ("CA",-1.93, 7.47, 6.55), ("0", 1,5, 5, 3.2)])
        AB = AminoAcid("LYS", [("N", 1, 0, 0), ("T",-1.93, 7.47, 6.55), ("0", 1,5, 5, 3.2)])

        self.assertIsInstance(AA, AminoAcid) #True
        self.assertNotIsInstance(AA, AminoAcid) #False
        self.assertNotIsInstance(AA, AminoAcid) #True

    def test_add_atom_When_Okay(self):

        AA = AminoAcid("SER", [("N", 1, 0, 0), ("CA",-1.93, 7.47, 6.55), ("0", 1,5, 5, 3.2)])
        AA_length = len(AA)
        A = Atom ("O", -5.6, 0, 3)
        self.assertIsInstance(AA, AminoAcid)
        self.assertIsInstance(A, Atom)
        AA.add(A)
        self.assertEquals(len(AA), AA_length + 1)
        self.assertEquals(AA.get_list_atoms[-1], A)


    def test_add_atom_When_Not_Okay(self):

        AA = AminoAcid("SER", [("N", 1, 0, 0), ("CA",-1.93, 7.47, 6.55), ("0", 1,5, 5, 3.2)])
        AA_length = len(AA)
        A = Atom ("K", -5.6, 0, 3)
        self.assertIsInstance(AA, AminoAcid)
        self.assertIsInstance(A, Atom) #False
        AA.add(A)
        self.assertNotEquals(len(AA), AA_length + 1)
        self.assertNotEquals(AA.get_list_atoms[-1], A)
         
    