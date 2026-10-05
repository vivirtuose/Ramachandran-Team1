"""
Partie VI du projet : Mesures de qualité et de stabilité de clustering
-------------------------------------------------------------------------------------------------
| OBJECTIF : Déterminer la qualité d'un clustering à partir d'une analyse des résultats obtenus |
-------------------------------------------------------------------------------------------------

Deux critères de qualité seront implémentées : 

    - Coefficient de Silhouette pour évaluer la qualité d'une partition ;
    - L'indice de Dunn pour évaluer les algorithmes de clustering.
"""
from pathlib import Path 

class ClusteringMeasures(ClusterPoint) :

    # Constructeur(self, attributs...)
    def __init__(self, cluster_point : list | str | Path) :

        self.cluster_point = cluster_point # On vérifie dans le setter qu'on a bien une liste en entrée

    @property
    def cluster_point(self) :
        return self._cluster_point

    @cluster_point.setter
    def cluster_point(self, value) :
        """
        Vérifie que l'attribut est bien une liste à la fin !
        """
        if isinstance(value, (str, Path)) :
            self.cluster_point = self._load(value)

    # Méthodes ...

    # Une méthode statique est une méthode qui ne tient pas compte de l'instance (donc pas besoin de self).
    @staticmethod
    def load(path : str | Path) -> list :
        """
        Lecture d'un fichier pour stocker le contenu dans une liste.
        """
        with open(path, encoding = "utf-8") as fh :
            fh.read().splitlines()


    