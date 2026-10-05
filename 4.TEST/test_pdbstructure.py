import unittest
from PDBStructure import StructurePDB


class TestPDBStructure(unittest.TestCase):

    # Tester creation de la structure :
    def test_creation(self):
        structure = StructurePDB("1tey_model1.pdb")
        self.assertTrue(structure != None)


    # Tester le premier residu :
    def test_premier_residu(self):
        structure = StructurePDB("1tey_model1.pdb")
        self.assertEqual(structure.residues[0].res_type, "MET")


    # Tester le deuxieme residu :
    def test_deuxieme_residu(self):
        structure = StructurePDB("1tey_model1.pdb")
        self.assertEqual(structure.residues[1].res_type, "ALA")


    # Tester le troisieme residu :
    def test_troisieme_residu(self):
        structure = StructurePDB("1tey_model1.pdb")
        self.assertEqual(structure.residues[2].res_type, "LYS")


    # Tester les angles phi et psi :
    def test_angles(self):

        structure = StructurePDB("1tey_model1.pdb")
        structure.compute_dihedrals()
        self.assertEqual(round(structure.phipsi[0].abs, 3), -1.297)

        self.assertEqual(round(structure.phipsi[0].ord, 3), 2.371)


unittest.main()