######### IMPORT ##############
import unittest
from Point import *


######### LILOU ############
class test_Point(unittest.TestCase):
    """
    il faut tester : 
    - constructeur
    - str
    - fonction add
    - fonction rescal
    - fonction distance_from_origin
    - fonction euclidean_distance
    - fonction manhattan_distance
    """
    def test_point_constructeur_defaut(self):
        """
        test d'initiation du constructeur au coordonnée (0, 0).        
        """
        p = Point(0, 0)
        self.assertEqual((p.get_abs(), p.get_ord()), (1,2))
    
    
    def test_point_constructeur(self):
        """
        test du constructeur aux coordonnées données dans l'énoncé.        
        """
        p = Point(1,2)
        self.assertEqual((p.get_abs(), p.get_ord()), (1,2))

    def test_point_str(self):
        """
        test du str :
        - il faut 4 chiffres après la virgule
        """
        self.assertEqual(str(Point(1, 2)), "Point of coordinates (1.0000, 2.0000)")

    def test_point_add(self, another_point):
        """ 
        
        """
        pass

    def test_point_rescal(self, factor):
        pass

    def test_point_distance_from_origin(self):
        pass

    def test_point_euclidean_distance(self, another_point):
        pass

    def test_point_manhattan_distance(self, another_point):
        pass

    
        pass

    



######### VIVIAN ########### 
# clustering --> Kmean et DBscans 


# Kmeans : la liste des Point, k, et la liste de k listes de résultat.
"""
Kmeans :

Contrat de la classe :
Entrée : une liste non vide de Point 2D, et 1 ≤ k ≤ nombre de points.
Sortie : une partition. Chaque point est dans exactement un groupe, et il y a exactement k groupes.
Dépendance : elle utilise Point.euclidean_distance pour l'affectation. Elle dépend donc de la correction de Point.
Non déterministe : l'initialisation est aléatoire, donc deux exécutions peuvent donner deux partitions différentes.

Attributs de Kmean : 
paramètre du constructeur
 - k, nombre de groupes a créer 

paramètre du constructeur 
 - points, liste de Point à regrouper

résultat du clustering :
clusters, liste de k clusters et une sous-liste i qui contient les Point du groupe i 

"""
 
class test_Kmean

"""
Type de test :  
1. vérifier si cas invalides de k  :
- k = 0 
- k < 0 
-  non entier 

2. vérifier la parition  
Le résultat contient exactement k sous-listes.
Chaque point est dans exactement un groupe (pas de doublon, pas de perte).
La somme des tailles des groupes est égale au nombre de points.
Aucun groupe n'est vide.

3. Cas à solution connue 

Deux blobs très éloignés avec k=2 : on retrouve exactement les deux blobs.
Trois blobs, quatre coins d'un carré, etc.
k=1 : un seul groupe avec tous les points, et son centroïde est la moyenne.
k = n : chaque point est seul dans son groupe.
Tous les points identiques avec k>1 : le programme ne doit pas planter (pas de division par zéro).
Un seul point avec k=1.


"""

# Dbscan : la liste des Point, epsilon, min_points, et la liste de résultat.
"""
Type de test :

1. Vérifier les cas invalides des paramètres
- epsilon = 0
- epsilon < 0
- epsilon non numérique (chaîne, None)
- min_points = 0
- min_points < 0
- min_points non entier
- liste de points vide ou None

2. Vérifier la partition
- Chaque point est soit dans exactement un cluster, soit dans le bruit
  (pas de doublon, pas de perte).
- Somme des tailles des clusters + taille du bruit = nombre de points.
- Aucun cluster n'est vide.
- Le résultat n'est pas figé par l'ordre d'entrée : mélanger la liste donne
  les mêmes clusters (à la numérotation près).
- Les points d'entrée ne sont pas modifiés par l'algorithme.

3. Cas à solution connue
- Deux blobs denses très éloignés : 2 clusters, aucun bruit.
- Deux blobs + quelques points isolés très loin : 2 clusters, les points isolés
  sont du bruit.
- Un seul point : du bruit (si min_points > 1), un cluster si min_points = 1.
- Tous les points isolés (epsilon très petit) : tout est bruit, 0 cluster.
- epsilon très grand : un seul cluster avec tous les points.

4. Classification noyau / frontière / bruit
- Un point avec exactement min_points voisins est noyau ; avec min_points - 1
  il ne l'est pas.
- Un point à distance exactement epsilon d'un autre (voisin ou non ?).


"""












































































































































































