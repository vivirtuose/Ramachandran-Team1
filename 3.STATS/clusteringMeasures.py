"""
Partie VI du projet : Mesures de qualité et de stabilité de clustering
-------------------------------------------------------------------------------------------------
| OBJECTIF : Déterminer la qualité d'un clustering à partir d'une analyse des résultats obtenus |
-------------------------------------------------------------------------------------------------

Deux critères de qualité seront implémentées : 

    - Coefficient de Silhouette pour évaluer la qualité d'une répartition ;
    - L'indice de Dunn pour évaluer les algorithmes de clustering.
"""
from clustering_KMeans import ClusterPoint
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
    def cluster_point_list(self, value):
        """
        Accepte une liste de ClusterPoint ou un chemin de fichier.
        """

        if isinstance(value, (str, Path)):
            value = self.load(value)

        if not isinstance(value, list):
            raise TypeError(f"Une liste de ClusterPoint ou un chemin vers un fichier .txt est attendu. (Type actuel : {type(value)})")
        
        if len(value) == 0:
            raise ValueError("Il n'y a pas de points à analyser...")
        
        self._cluster_point_list = value

    # -- Méthodes ... --

    # Une méthode statique est une méthode qui ne tient pas compte de l'instance (donc pas besoin de self).
    @staticmethod
    def load(path : str | Path) -> list :
        """
        Lecture d'un fichier pour stocker le contenu dans une liste.
        """
        points = []
        with open(path, encoding="utf-8") as fh:
            for line in fh.read().splitlines():
                if line.strip() == "" or line.startswith("phi"):   # S'il y a une ligne vide ou en-tête
                    continue

                phi, psi, cluster = line.split("\t")
                points.append(ClusterPoint(float(phi), float(psi), int(cluster)))
    
    @staticmethod
    def dist(p, q) -> float:
        """
        Réutilisation de la méthode dans la classe Point.
        """
        return p.euclidean_distance(q)
    
    def order_cluster(self) -> dict :
        """
        Ordonne les points selon le cluster auquel ils sont associés.

        Fonctionnement du code : Pour chaque point, on regarde son numéro de cluster. 
        Si ce cluster n'a pas encore de liste dans le dictionnaire, on lui en crée une vide. 
        Ensuite, on ajoute le point dans cette liste.
        """
        groups = {}
        for p in self.cluster_point_list:
            if p.nb_cluster not in groups:   
                groups[p.nb_cluster] = []  

            groups[p.nb_cluster].append(p)

        return groups

    def a(self, p: list) -> float :
        """
        Distance moyenne entre p et les autres points de son cluster (cohésion).
        """
        groups = self.order_cluster()
        cluster = groups[p.nb_cluster]

        if len(cluster) == 1:
            return 0.0

        total = 0
        for q in cluster:
            if q is not p:
                total += self.dist(p, q)

        return total / (len(cluster) - 1)

    def mean_distance(self, p, cluster) :
        """
        Distance moyenne entre p et tous les points d'un cluster.
        """
        total = 0
        for q in cluster:
            total += self.dist(p, q)

        return total / len(cluster)

    def b(self, p) :
        """
        b(i) : plus petite distance moyenne entre p et un autre cluster.
        """
        groups = self.order_cluster()
        best = None

        for k in groups :
            if k != p.nb_cluster :                               
                mean = self.mean_distance(p, groups[k])

                if best is None or mean < best :
                    best = mean

        return best
    