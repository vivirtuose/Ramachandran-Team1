import unittest
from AminoAcid import *
from Atom import *


class Test_AminoAcid(unittest.TestCase):

    def test_constructeur_construct_instance(self):

        AA = AminoAcid(1, "SER", [("N", 1, 0, 0), ("CA",-1.93, 7.47, 6.55), ("0", 1.5, 5, 3.2)])
        AB = AminoAcid(2, "LYS", [("N", 1, 0, 0), ("T",-1.93, 7.47, 6.55), ("0", 1.5, 5, 3.2)])

        self.assertIsInstance(AA, AminoAcid) #True
        self.assertIsInstance(AA, AminoAcid) #False
        self.assertNotIsInstance(AA, AminoAcid) #True

    def test_add_atom_When_Okay(self):

        AA = AminoAcid(1, "SER", [("N", 1, 0, 0), ("CA",-1.93, 7.47, 6.55), ("0", 1.5, 5, 3.2)])
        AA_length = len(AA)
        A = Atom ("O", -5.6, 0, 3)
        self.assertIsInstance(AA, AminoAcid)
        self.assertIsInstance(A, Atom)
        AA.add(A)
        self.assertEquals(len(AA), AA_length + 1)
        self.assertEquals(AA.get_list_atoms[-1], A)


    def test_add_atom_When_Not_Okay(self):

        AA = AminoAcid(1, "SER", [("N", 1, 0, 0), ("CA",-1.93, 7.47, 6.55), ("0", 1.5, 5, 3.2)])
        AA_length = len(AA)
        A = Atom ("K", -5.6, 0, 3)
        self.assertIsInstance(AA, AminoAcid)
        self.assertIsInstance(A, Atom) #False
        AA.add(A)
        self.assertNotEquals(len(AA), AA_length + 1)
        self.assertNotEquals(AA.get_list_atoms[-1], A)

    
    def test_get_N(self):

        AA = AminoAcid(1, "SER", [("N", 1, 0, 0), ("CA",-1.93, 7.47, 6.55), ("0", 1.5, 5, 3.2)])
        self.assertIsInstance(AA, AminoAcid)
        self.assertEquals(("N", 1, 0, 0), AA.get_N())

    def test_get_CA(self):

        AA = AminoAcid(1, "SER", [("N", 1, 0, 0), ("CA",-1.93, 7.47, 6.55), ("0", 1.5, 5, 3.2)])
        self.assertIsInstance(AA, AminoAcid)
        self.assertEquals(("CA",-1.93, 7.47, 6.55), AA.get_CA())

    def test_get_C(self):

        AA = AminoAcid(1, "SER", [("N", 1, 0, 0), ("CA",-1.93, 7.47, 6.55), ("0", 1.5, 5, 3.2), ("C", 3, 0, 2)])
        self.assertIsInstance(AA, AminoAcid)
        self.assertEquals(("C", 3, 0, 2), AA.get_N())

    def test_get_O(self):

        AA = AminoAcid(1, "SER", [("N", 1, 0, 0), ("CA",-1.93, 7.47, 6.55), ("0", 1,5, 5, 3.2)])
        self.assertIsInstance(AA, AminoAcid)
        self.assertEquals(("0", 1.5, 5, 3.2), AA.get_O())



         
    