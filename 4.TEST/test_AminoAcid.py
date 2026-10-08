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

        self.assertIsInstance(AA, AminoAcid) #True
        self.assertIsInstance(AB, AminoAcid) #False
        self.assertNotIsInstance(AB, AminoAcid) #True

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
        self.assertIsInstance(A, Atom) #False
        AA.add(A)
        self.assertNotEqual(len(AA.atoms), AA_length + 1)
        self.assertNotEqual(AA.atoms[-1], A)

    
    def test_get_N(self):

        AA = AminoAcid(1, "SER", [Atom("N", 1, 0, 0), Atom("CA",-1.93, 7.47, 6.55), Atom("O", 1.5, 5, 3.2)])
        self.assertIsInstance(AA, AminoAcid)
        self.assertEqual(("N" (1, 0, 0)), AA.N)

    def test_get_CA(self):

        AA = AminoAcid(1, "SER", [Atom("N", 1, 0, 0), Atom("CA",-1.93, 7.47, 6.55), Atom("O", 1.5, 5, 3.2)])
        self.assertIsInstance(AA, AminoAcid)
        self.assertEqual(("CA" (-1.93, 7.47, 6.55)), AA.CA)

    def test_get_C(self):

        AA = AminoAcid(1, "SER", [Atom("N", 1, 0, 0), Atom("CA",-1.93, 7.47, 6.55), Atom("O", 1.5, 5, 3.2), ("C", 3, 0, 2)])
        self.assertIsInstance(AA, AminoAcid)
        self.assertEqual(("C" (3, 0, 2)), AA.C)

    def test_get_O(self):

        AA = AminoAcid(1, "SER", [Atom("N", 1, 0, 0), Atom("CA",-1.93, 7.47, 6.55), Atom("O", 1.5, 5, 3.2)])
        self.assertIsInstance(AA, AminoAcid)
        self.assertEqual(("O" (1.5, 5, 3.2)), AA.O)