"""
Partie VI du projet : Mesures de qualité et de stabilité de clustering
-------------------------------------------------------------------------------------------------
| OBJECTIF : Déterminer la qualité d'un clustering à partir d'une analyse des résultats obtenus |
-------------------------------------------------------------------------------------------------

Deux critères de qualité seront implémentées : 

    - Coefficient de Silhouette pour évaluer la qualité d'une répartition ;
    - L'indice de Dunn pour évaluer les algorithmes de clustering.
"""
import ClusterPoint
from pathlib import Path 

class ClusteringMeasures() :

    # -- Constructeur(self, attributs...) --
    def __init__(self, cluster_point_list : list | str | Path) :

        self.cluster_point_list = cluster_point_list # On vérifie dans le setter qu'on a bien une liste en entrée

    # -- Getter et setter --
    @property
    def cluster_point_list(self) :
        return self._cluster_point_list

    @cluster_point_list.setter
    def cluster_point_list(self, value) :
        """
        Vérifie que l'attribut est bien une liste à la fin !
        """
        if isinstance(value, (str, Path)) :
            self.cluster_point_list = self._load(value)

        else :
            raise ValueError(f"self.cluster_point_list doit être une liste !")
        
        self.cluster_point_list = list(value)

    # -- Méthodes ... --

    # Une méthode statique est une méthode qui ne tient pas compte de l'instance (donc pas besoin de self).
    @staticmethod
    def _load(path : str | Path) -> list :
        """
        Lecture d'un fichier pour stocker le contenu dans une liste.
        """
        points = []
        with open(path, encoding = "utf-8") as fh :
            for line in  fh.read().splitlines() : 
                x, y, cluster = line.split("\t")
                points.append(ClusterPoint(float(x), float(y), int(cluster)))

        return points
    
    @staticmethod
    def _dist(p, q) -> float :
        """
        Implémentation de la distance euclidienne qu'on utilisera par défaut.
        On pourra la modifier ici pour par exemple faire une distance de Manhattan.
        On pourrait aussi utiliser le module math pour avoir quelque chose de plus simple mais
        l'avantage ici est qu'on a directement le détail de la formule.
        """
        return ((p.x - q.x) ** 2 + (p.y - q.y) ** 2) ** 0.5


    