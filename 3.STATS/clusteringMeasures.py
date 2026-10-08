from pathlib import Path 
from clustering import ClusterPoint
from copy import copy

class ClusteringMeasures() :
    """
    Mesures de qualité d'un clustering via l'implémentation du coefficient de Silhouette et l'indice de Dunn.

    Attribut :
    cluster_point_list : list -> liste des ClusterPoint.
    """
    # -- Constructeur(self, attributs...) --
    def __init__(self, cluster_point_list : list | str | Path) :

        self.cluster_point_list = cluster_point_list # On vérifie dans le setter qu'on a bien une liste en entrée

    # -- Getter et setter --
    @property
    def cluster_point_list(self) :
        return copy(self._cluster_point_list) # On évite de travailler sur la liste originale pour respecter l'encapsulation

    @cluster_point_list.setter
    def cluster_point_list(self, value) :
        """
        Accepte une liste de ClusterPoint ou un chemin de fichier.
        """

        if isinstance(value, (str, Path)) :
            value = self.load(value)

        if not isinstance(value, list) :
            raise TypeError(f"Une liste de ClusterPoint ou un chemin vers un fichier .txt est attendu. (Type actuel : {type(value)})")
        
        if len(value) == 0 :
            raise ValueError("Il n'y a pas de points à analyser...")
        
        self._cluster_point_list = copy(value)

    # -- Méthodes ... --

    # Une méthode statique est une méthode qui ne tient pas compte de l'instance (donc pas besoin de self).
    @staticmethod
    def load(path : str | Path) -> list :
        """
        Lecture d'un fichier pour stocker le contenu dans une liste.
        """
        points = []
        with open(path, encoding="utf-8") as fh :
            for line in fh.read().splitlines() :
                if line.strip() == "" or line.startswith("phi") :   # S'il y a une ligne vide ou en-tête
                    continue

                phi, psi, cluster = line.split("\t")
                points.append(ClusterPoint(float(phi), float(psi), int(cluster)))

        return points
    
    @staticmethod
    def dist(p, q) -> float :
        """
        Correspond à d(p, q) du sujet -> distance euclidienne, réutilisée depuis la classe Point.

        Paramètres :
            p, q qui sont des objets Points à comparer

        Sortie :
            Un float correspondant à la distance entre les deux points
        """
        return p.euclidean_distance(q)

    # -- Méthodes relatives aux Coefficient de Silhouette --
    def order_cluster(self) -> dict :
        """
        Ordonne les points selon le cluster auquel ils sont associés.

        Fonctionnement du code : Pour chaque point, on regarde son numéro de cluster. 
        Si ce cluster n'a pas encore de liste dans le dictionnaire, on lui en crée une vide. 
        Ensuite, on ajoute le point dans cette liste.

        Sortie :
            Un dictionnaire avec le numéro de cluster en clé et la liste des ClusterPoint associée en valeur.
        """
        groups = {}
        for p in self.cluster_point_list :
            if p.nb_cluster not in groups :   
                groups[p.nb_cluster] = []  

            groups[p.nb_cluster].append(p)

        return groups

    def a(self, p) -> float :
        """
        Calcule la distance moyenne entre p et les autres points de son cluster (cohésion).

        Paramètre : 
            p : ClusterPoint -> correspond au point d'intérêt

        Sortie : 
            Un float correspondant à la distance.

        """
        groups = self.order_cluster()
        cluster = groups[p.nb_cluster]

        if len(cluster) == 1 :
            return 0.0

        total = 0
        for q in cluster :
            if q is not p :
                total += self.dist(p, q)

        return total / (len(cluster) - 1)

    def mean_distance(self, p, cluster) :
        """
        Calcule la distance moyenne entre p et tous les points d'un cluster.

        Paramètres : 
            p : ClusterPoint -> le point d'intérêt
            cluster : list -> la liste des ClusterPoint du cluster

        Sortie : 
            Un float correspondant à la distance.
        """
        total = 0
        for q in cluster :
            total += self.dist(p, q)

        return total / len(cluster)

    def b(self, p) :
        """
        Calcule la plus petite distance moyenne entre p et un autre cluster.

        Paramètre : 
            p : ClusterPoint -> le point d'intérêt.

        Sortie : 
            Un float ou None s'il n'existe pas d'autres clusters.
        """
        groups = self.order_cluster()
        best = None

        for k in groups :
            if k != p.nb_cluster :                               
                mean = self.mean_distance(p, groups[k])

                if best is None or mean < best :
                    best = mean

        return best

    def silhouette_point(self, p) :
        """
        c_sil(i) = (b(i) - a(i)) / max(a(i), b(i)).

        Paramètre : 
            p : ClusterPoint -> le point d'intérêt.

        Sortie : 
            Une valeur entre -1 (mal classé) et 1 (bien classé).
        """
        if len(self.order_cluster()[p.nb_cluster]) == 1 :
            return 0.0

        a = self.a(p)
        b = self.b(p)

        if max(a, b) == 0 :
            return 0.0

        return (b - a) / max(a, b)

    def coeff_silhouette(self) :
        """
        Implémentation de la formule du sujet pour le coefficient de Silhouette.

        Sortie : 
            Une valeur entre -1 (mauvaise classification) et 1 (bonne classification).
        """
        groups = self.order_cluster()
        if len(groups) < 2 :
            raise ValueError("Le coefficient de Silhouette nécessite au moins 2 clusters")

        total = 0
        for k in groups :
            cluster = groups[k]
            cluster_sum = 0

            for p in cluster :
                cluster_sum += self.silhouette_point(p)
                
            total += cluster_sum / len(cluster)

        return total / len(groups) 

    # -- Méthodes relatives à l'Indice de Dunn --
    def diameter(self, cluster) :
        """
        Retourne la distance max entre deux points du cluster.
        """
        d_max = 0

        for i in range(len(cluster)) :
            for j in range(i + 1, len(cluster)) :
                d = self.dist(cluster[i], cluster[j])

                if d > d_max :
                    d_max = d

        return d_max

    def separation(self, cluster_1, cluster_2) :
        """
        Retourne la plus petite distance en comparant chaque point présent parmi les deux clusters.
        """
        d_min = None # permet d'éviter d'avoir deux points qui se superposent dans deux clusters différents

        for p in cluster_1 :
            for q in cluster_2 :
                d = self.dist(p, q)

                if d_min is None or d < d_min :
                    d_min = d

        return d_min 

    def indice_dunn(self):
    
        groups = self.order_cluster()
        keys = list(groups)

        if len(keys) < 2 :
            raise ValueError("L'indice de Dunn nécessite d'avoir au moins 2 clusters") # Gestion d'erreurs

        # On prend le plus grand diamètre comme dénominateur
        max_diameter = 0

        for k in keys :
            d = self.diameter(groups[k])
            
            if d > max_diameter :
                max_diameter = d

        # On prend la plus petite séparation entre deux clusters comme numérateur
        min_separation = None
        for i in range(len(keys)) :
            for j in range(i + 1, len(keys)) :     
                s = self.separation(groups[keys[i]], groups[keys[j]])

                if min_separation is None or s < min_separation :
                    min_separation = s

        if max_diameter == 0 :
            raise ValueError("Tous les clusters ont un diamètre nul") # Nouvelle gestion d'erreur pour les tests.

        return min_separation / max_diameter