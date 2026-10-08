import unittest
import sys
import os

# Chercher les fichiers dans les autres dossiers
sys.path.append("2.PDB_STRUCT")
sys.path.append("1.ATOM_AMINO")

from PDBStructure import StructurePDB


class TestPDBStructure(unittest.TestCase):

    # Tester la creation de la structure
    def test_creation(self):
        structure = StructurePDB("1tey_model1.pdb")
        self.assertTrue(structure != None)


    # Tester le nom du fichier
    def test_nom_fichier(self):
        structure = StructurePDB("1tey_model1.pdb")
        self.assertEqual(structure._path_to_file, "1tey_model1.pdb")


    # Tester le nombre de residus
    def test_nombre_residus(self):
        structure = StructurePDB("1tey_model1.pdb")
        self.assertEqual(len(structure._residues), 156)


    # Tester le premier residu
    def test_premier_residu(self):
        structure = StructurePDB("1tey_model1.pdb")
        self.assertEqual(structure._residues[0].res_type, "MET")


    # Tester le deuxieme residu
    def test_deuxieme_residu(self):
        structure = StructurePDB("1tey_model1.pdb")
        self.assertEqual(structure._residues[1].res_type, "ALA")


    # Tester le troisieme residu
    def test_troisieme_residu(self):
        structure = StructurePDB("1tey_model1.pdb")
        self.assertEqual(structure._residues[2].res_type, "LYS")


    # Tester le dernier residu
    def test_dernier_residu(self):
        structure = StructurePDB("1tey_model1.pdb")
        self.assertEqual(structure._residues[-1].res_type, "ASN")


    # Tester le nombre d'atomes du premier residu
    def test_nombre_atomes(self):
        structure = StructurePDB("1tey_model1.pdb")
        self.assertEqual(len(structure._residues[0].atoms), 4)


    # Tester les noms des atomes du premier residu
    def test_noms_atomes(self):
        structure = StructurePDB("1tey_model1.pdb")

        noms = []

        for atom in structure._residues[0].atoms:
            noms.append(atom.name)

        self.assertEqual(noms, ["N", "CA", "C", "O"])


    # Tester que tous les residus ont 4 atomes
    def test_quatre_atomes_par_residu(self):
        structure = StructurePDB("1tey_model1.pdb")

        for residu in structure._residues:
            self.assertEqual(len(residu.atoms), 4)


    # Tester que seuls N, CA, C et O sont gardes
    def test_atomes_valides(self):
        structure = StructurePDB("1tey_model1.pdb")

        for residu in structure._residues:
            for atom in residu.atoms:
                self.assertTrue(atom.name in ["N", "CA", "C", "O"])


    # Tester les coordonnees du premier atome N
    def test_coordonnees_premier_atome(self):
        structure = StructurePDB("1tey_model1.pdb")

        atom = structure._residues[0].atoms[0]

        self.assertEqual(atom.name, "N")
        self.assertEqual(round(atom.x, 3), -23.630)
        self.assertEqual(round(atom.y, 3), 0.712)
        self.assertEqual(round(atom.z, 3), 8.124)


    # Tester la recherche d'un atome N
    def test_recherche_atome(self):
        structure = StructurePDB("1tey_model1.pdb")

        residu = structure._residues[0]

        atom = structure._get_atom_by_name(residu, "N")

        self.assertEqual(atom.name, "N")


    # Tester la recherche d'un atome qui n'existe pas
    def test_atome_inexistant(self):
        structure = StructurePDB("1tey_model1.pdb")

        residu = structure._residues[0]

        atom = structure._get_atom_by_name(residu, "X")

        self.assertEqual(atom, None)


    # Tester si les angles sont calcules
    def test_angles(self):
        structure = StructurePDB("1tey_model1.pdb")

        structure.compute_dihedrals()

        self.assertTrue(len(structure._phipsi) > 0)


    # Tester le nombre de couples phi psi
    def test_nombre_angles(self):
        structure = StructurePDB("1tey_model1.pdb")

        structure.compute_dihedrals()

        self.assertEqual(len(structure._phipsi), 154)


    # Tester le nombre de phi et de psi
    def test_nombre_phi_psi(self):
        structure = StructurePDB("1tey_model1.pdb")

        phi, psi = structure.compute_dihedrals()

        self.assertEqual(len(phi), 154)
        self.assertEqual(len(psi), 154)


    # Tester le premier angle phi
    def test_premier_phi(self):
        structure = StructurePDB("1tey_model1.pdb")

        structure.compute_dihedrals()

        self.assertEqual(
            round(structure._phipsi[0].x, 3),
            -1.297
        )


    # Tester le premier angle psi
    def test_premier_psi(self):
        structure = StructurePDB("1tey_model1.pdb")

        structure.compute_dihedrals()

        self.assertEqual(
            round(structure._phipsi[0].y, 3),
            2.371
        )


    # Tester le deuxieme couple phi psi
    def test_deuxieme_angle(self):
        structure = StructurePDB("1tey_model1.pdb")

        structure.compute_dihedrals()

        self.assertEqual(
            round(structure._phipsi[1].x, 3),
            -1.511
        )

        self.assertEqual(
            round(structure._phipsi[1].y, 3),
            -0.570
        )


    # Tester le troisieme couple phi psi
    def test_troisieme_angle(self):
        structure = StructurePDB("1tey_model1.pdb")

        structure.compute_dihedrals()

        self.assertEqual(
            round(structure._phipsi[2].x, 3),
            -2.372
        )

        self.assertEqual(
            round(structure._phipsi[2].y, 3),
            2.314
        )


    # Tester que les angles sont entre -pi et pi
    def test_limites_angles(self):
        structure = StructurePDB("1tey_model1.pdb")

        structure.compute_dihedrals()

        for point in structure._phipsi:

            self.assertTrue(point.x >= -3.15)
            self.assertTrue(point.x <= 3.15)

            self.assertTrue(point.y >= -3.15)
            self.assertTrue(point.y <= 3.15)


    # Tester que refaire le calcul ne rajoute pas des angles
    def test_recalcul_angles(self):
        structure = StructurePDB("1tey_model1.pdb")

        structure.compute_dihedrals()
        nombre1 = len(structure._phipsi)

        structure.compute_dihedrals()
        nombre2 = len(structure._phipsi)

        self.assertEqual(nombre1, nombre2)


    # Tester l'ecriture du fichier des angles
    def test_ecriture_fichier(self):
        structure = StructurePDB("1tey_model1.pdb")

        structure.compute_dihedrals()

        structure.write_dihedrals("angles_test.txt")

        self.assertTrue(os.path.exists("angles_test.txt"))

        os.remove("angles_test.txt")


    # Tester le nombre de lignes du fichier des angles
    def test_nombre_lignes_fichier(self):
        structure = StructurePDB("1tey_model1.pdb")

        structure.compute_dihedrals()

        structure.write_dihedrals("angles_test.txt")

        fichier = open("angles_test.txt", "r")
        lignes = fichier.readlines()
        fichier.close()

        self.assertEqual(len(lignes), 154)

        os.remove("angles_test.txt")


    # Tester la premiere ligne du fichier des angles
    def test_premiere_ligne_fichier(self):
        structure = StructurePDB("1tey_model1.pdb")

        structure.compute_dihedrals()

        structure.write_dihedrals("angles_test.txt")

        fichier = open("angles_test.txt", "r")
        ligne = fichier.readline().strip()
        fichier.close()

        self.assertEqual(
            ligne,
            "-1.296614\t2.370531"
        )

        os.remove("angles_test.txt")


    # Tester avec un fichier qui n'existe pas
    def test_fichier_inexistant(self):

        with self.assertRaises(FileNotFoundError):
            StructurePDB("fichier_inexistant.pdb")


    


if __name__ == "__main__":
    unittest.main()
