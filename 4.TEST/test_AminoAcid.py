import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "1.ATOM_AMINO"))

from AminoAcid import *
from Atom import *


class Test_AminoAcid(unittest.TestCase):

    def test_constructeur_construct_instance(self):

        AA = AminoAcid(1, "SER", [Atom("N", 1, 0, 0), Atom("CA",-1.93, 7.47, 6.55), Atom("O", 1.5, 5, 3.2)])
        AB = AminoAcid(2, "LYS", [Atom("N", 1, 0, 0), Atom("T",-1.93, 7.47, 6.55), Atom("O", 1.5, 5, 3.2)])

        self.assertIsInstance(AA, AminoAcid)
        self.assertIsInstance(AB, AminoAcid)

    def test_add_atom_When_Okay(self):

        AA = AminoAcid(1, "SER", [Atom("N", 1, 0, 0), Atom("CA",-1.93, 7.47, 6.55), Atom("O", 1.5, 5, 3.2)])
        AA_length = len(AA.atoms)
        A = Atom ("O", -5.6, 0, 3)
        self.assertIsInstance(AA, AminoAcid)
        self.assertIsInstance(A, Atom)
        AA.add(A)
        self.assertEqual(len(AA.atoms), AA_length + 1)
        self.assertEqual(AA.atoms[-1], A)


    def test_add_atom_When_Not_Okay(self):

        AA = AminoAcid(1, "SER", [Atom("N", 1, 0, 0), Atom("CA",-1.93, 7.47, 6.55), Atom("O", 1.5, 5, 3.2)])
        AA_length = len(AA.atoms)
        A = Atom ("K", -5.6, 0, 3)
        self.assertIsInstance(AA, AminoAcid)
        self.assertIsInstance(A, Atom)
        # "K" is not an atom of the backbone (N, CA, C, O): add() must refuse it
        with self.assertRaises(ValueError):
            AA.add(A)
        self.assertEqual(len(AA.atoms), AA_length)
        self.assertIsNot(AA.atoms[-1], A)

    
    def test_get_N(self):

        AA = AminoAcid(1, "SER", [Atom("N", 1, 0, 0), Atom("CA",-1.93, 7.47, 6.55), Atom("O", 1.5, 5, 3.2)])
        self.assertIsInstance(AA, AminoAcid)
        self.assertEqual(AA.N.name, "N")
        self.assertEqual(AA.N.coords, [1, 0, 0])

    def test_get_CA(self):

        AA = AminoAcid(1, "SER", [Atom("N", 1, 0, 0), Atom("CA",-1.93, 7.47, 6.55), Atom("O", 1.5, 5, 3.2)])
        self.assertIsInstance(AA, AminoAcid)
        self.assertEqual(AA.CA.name, "CA")
        self.assertEqual(AA.CA.coords, [-1.93, 7.47, 6.55])

    def test_get_C(self):

        AA = AminoAcid(1, "SER", [Atom("N", 1, 0, 0), Atom("CA",-1.93, 7.47, 6.55), Atom("O", 1.5, 5, 3.2), Atom("C", 3, 0, 2)])
        self.assertIsInstance(AA, AminoAcid)
        self.assertEqual(AA.C.name, "C")
        self.assertEqual(AA.C.coords, [3, 0, 2])

    def test_get_O(self):

        AA = AminoAcid(1, "SER", [Atom("N", 1, 0, 0), Atom("CA",-1.93, 7.47, 6.55), Atom("O", 1.5, 5, 3.2)])
        self.assertIsInstance(AA, AminoAcid)
        self.assertEqual(AA.O.name, "O")
        self.assertEqual(AA.O.coords, [1.5, 5, 3.2])