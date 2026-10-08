import random
import math
from abc import ABC, abstractmethod
from Point import Point

from pathlib import Path 

class ClusterPoint(Point):
    def __init__(self, x, y, nb_cluster):
        super().__init__(x, y)
        self._nb_cluster = self._check_nb_cluster(nb_cluster)

    def _check_nb_cluster(self, nb_cluster):
        if not isinstance(nb_cluster, int):
            raise TypeError("nb_cluster n'est pas un entier.")
        return nb_cluster
    
    @property
    def nb_cluster(self):
        return self._nb_cluster

    @nb_cluster.setter
    def nb_cluster(self, value):
        self._nb_cluster = self._check_nb_cluster(value)


class ClusteringMethods(ABC):
    # Pour obtenir l'abcisse d'un point : liste_point[n° du point].get_abs()
    # Pour obtenir l'ordonnée d'un point : liste_point[n° du point].get_ord()
    # Les calculs de distance sont dans la classe Point :
    # Point.euclidean_distance(self, another_point) et Point.manhattan_distance(self, another_point)

    def __init__(self, liste_point):
        if not liste_point:
            raise ValueError("Liste vide en entrée.")
        self._liste_point = liste_point
        self._liste_k = {}  # Dictionnaire : clé = numéro du cluster, value = liste des points dans le cluster

    @property
    def liste_point(self):
        return self._liste_point

    # Pas de setter pour liste_point, on veut que ça ne bouge pas.

    @property
    def liste_k(self):
        return self._liste_k

    @liste_k.setter
    def liste_k(self, results):
        self._liste_k = results

    @abstractmethod
    def run(self):
        """Chaque méthode de clustering doit l'implémenter."""
        pass

    def add_to_liste_k(self, key, value):
        # .setdefault crée la clé si elle n'existe pas (avec une liste vide) et renvoie sa liste.
        # Les values sont ajoutées à la liste automatiquement.
        # /!\ à ajouter des Points dans le append /!\
        self._liste_k.setdefault(key, []).append(value)

    def convert_in_clusterPoint(self):
        liste = []
        for key in self.liste_k:
            for point in self.liste_k[key]:
                liste.append(ClusterPoint(point.get_abs(), point.get_ord(), key))
        return liste

    def create_tsv(self, filename):
        with open(filename, "w", encoding="utf-8") as file:
            file.write("phi\tpsi\tcluster\n")  # header du .tsv
            for p in self.convert_in_clusterPoint():
                file.write(
                    "{:.6f}\t{:.6f}\t{}\n".format(
                        p.get_abs(), p.get_ord(), p.nb_cluster
                    )
                )


class Kmeans(ClusteringMethods):
    def __init__(self, liste_point, k, max_iter=300, tol=1e-9):
        super().__init__(liste_point)
        self._k = self._check_k(k)
        self._max_iter = max_iter
        self._tol = tol

    def _check_k(self, k):
        if not isinstance(k, int):
            raise TypeError("k n'est pas un entier.")
        if not 1 <= k <= len(self.liste_point):
            raise ValueError("k est inférieur à 1 ou supérieur au nombre de points.")
        return k

    @property
    def k(self):
        return self._k

    @k.setter
    def k(self, value):
        self._k = self._check_k(value)

    def choose_initial_points(self):  # Les ajoute au dico
        # On repart d'un dictionnaire vide : sinon un 2e appel à run() réutiliserait
        # les anciens clusters pour choisir les centroïdes initiaux.
        self._liste_k = {}
        indices = random.sample(range(len(self.liste_point)), self.k)
        for i, index in enumerate(indices):
            self.add_to_liste_k(i, self.liste_point[index])

    def run(self):
        self.choose_initial_points()
        # initialise : 1 groupe = 1 centroide
        centroides = [self.liste_k[i][0] for i in range(self.k)]

        # max_iter évite une boucle infinie si la convergence n'est jamais atteinte.
        for _ in range(self._max_iter):
            # 1. Affectation de chaque point au centroïde le plus proche
            self.liste_k = {i: [] for i in range(self.k)}
            for p in self.liste_point:
                # C'est ici qu'on change le type de distance, si besoin.
                # La méthode de calcul de distance doit être dans la classe Point.
                distances = [p.euclidean_distance(c) for c in centroides]
                self.add_to_liste_k(distances.index(min(distances)), p)

            # 2. Nouveaux centroïdes = moyenne de chaque groupe
            nouveaux = []
            for i in range(self.k):
                groupe = self.liste_k[i]
                # Groupe vide : pas de moyenne possible, on garde l'ancien centroïde.
                if not groupe:
                    nouveaux.append(centroides[i])
                    continue
                c = Point(0, 0)  # "somme = 0" adaptée à des Points
                for p in groupe:
                    c.add(p)
                c.rescale(1 / len(groupe))
                nouveaux.append(c)

            # 3. Convergence : les centroïdes ne bougent plus (tolérance sur les flottants)
            converge = all(
                n.euclidean_distance(c) <= self._tol
                for n, c in zip(nouveaux, centroides)
            )
            centroides = nouveaux
            if converge:
                break

class dbscan(ClusteringMethods):
    def __init__(self, liste_point,eps,nb_point):
        super().__init__(liste_point)
        self._eps = eps
        self._nb_point = nb_point
        self._liste_k = []
        self._point_traite = set()

        if self._eps <= 0 or self._nb_point <= 0:
            raise ValueError ("la distance minimale/eps/nb_point ne doit pas Ãªtre nÃ©gative ou Ã©gale Ã  0")
        if type(self._nb_point) != int:
            raise TypeError ("seulement int")
        if len(self._liste_point) <= 0 or self._liste_point == None:
            raise ValueError ("liste_point est vide ou None") 
        

    @property
    def liste_k(self):
        return self._liste_k
    @liste_k.setter
    def liste_k(self, r):
        self._liste_k = r

    @property
    def liste_point(self):
        return self._liste_point

    @property
    def eps(self):
        return self._eps

    @property
    def nb_point(self):
        return self._nb_point

    @property
    def point_traite(self):
        return self._point_traite


    def is_core(self,p1):
        x1,y1 = self.liste_point[p1]
        nb_neighbor = 0
        liste_neighbor = []

        for point in range(len(self.liste_point)):
            if point == p1:
                continue

            x2,y2 = self.liste_point[point]

            if math.sqrt((x1-x2)**2+(y1-y2)**2) <= self.eps:
                nb_neighbor += 1
                liste_neighbor.append(point)

        return (True,liste_neighbor) if nb_neighbor >= self.nb_point else (False,liste_neighbor)
    

    def is_traite(self,p1):
        return p1 in self.point_traite
        
    
    def run(self):
        liste_index_point = list(range(len(self.liste_point)))
        random.shuffle(liste_index_point)

        point_at_exp = set()

        for point in liste_index_point:
            if self.is_traite(point):
                continue
            is_core_point,liste_neighbor = self.is_core(point)

            if not is_core_point : 
                continue
        
            self.liste_k.append([point,*liste_neighbor])
            self.point_traite.update([point,*liste_neighbor])
            point_at_exp.update(liste_neighbor)

            while point_at_exp:
                point_at_exp_next = set()
                for point in point_at_exp:

                    is_core_point, liste_neighbor = self.is_core(point)
                    if not is_core_point:
                        continue

                    for neighbor in liste_neighbor:
                        if not self.is_traite(neighbor):
                            point_at_exp_next.add(neighbor)
                            self.point_traite.add(neighbor)

                self.liste_k[-1].extend(list(point_at_exp_next))
                point_at_exp = point_at_exp_next

    def clustering(self):
        liste_index_point = list(range(len(self.liste_point)))
        random.shuffle(liste_index_point)

        point_at_exp = set()

        for point in liste_index_point:
            if self.is_traite(point):
                continue
            is_core_point, liste_neighbor = self.is_core(point)

            if not is_core_point:
                continue

            self.liste_k.append([point, *liste_neighbor])
            self.point_traite.update([point, *liste_neighbor])
            point_at_exp.update(liste_neighbor)

            while point_at_exp:
                point_at_exp_next = set()
                for point in point_at_exp:
                    is_core_point, liste_neighbor = self.is_core(point)
                    if not is_core_point:
                        continue

                    for neighbor in liste_neighbor:
                        if not self.is_traite(neighbor):
                            point_at_exp_next.add(neighbor)
                            self.point_traite.add(neighbor)

                self.liste_k[-1].extend(list(point_at_exp_next))
                point_at_exp = point_at_exp_next


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

        return points
    
    @staticmethod
    def dist(p, q) -> float:
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
        for p in self.cluster_point_list:
            if p.nb_cluster not in groups:   
                groups[p.nb_cluster] = []  

            groups[p.nb_cluster].append(p)

        return groups

    def a(self, p: list) -> float :
        """
        Calcule la distance moyenne entre p et les autres points de son cluster (cohésion).

        Paramètre : 
            p : ClusterPoint -> correspond au point d'intérêt

        Sortie : 
            Un float correspondant à la distance.

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
        Calcule la distance moyenne entre p et tous les points d'un cluster.

        Paramètres : 
            p : ClusterPoint -> le point d'intérêt
            cluster : list -> la liste des ClusterPoint du cluster

        Sortie : 
            Un float correspondant à la distance.
        """
        total = 0
        for q in cluster:
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

    def coeff_silhouette(self):
        """
        Implémentation de la formule du sujet pour le coefficient de Silhouette.

        Sortie : 
            Une valeur entre -1 (mauvaise classification) et 1 (bonne classification).
        """
        groups = self.order_cluster()
        if len(groups) < 2:
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
    def diameter(self, cluster):
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

    def separation(self, cluster_1, cluster_2):
        """
        Retourne la plus petite distance en comparant chaque point présent parmi les deux clusters.
        """
        d_min = 0

        for p in cluster_1 :
            for q in cluster_2 :
                d = self.dist(p, q)

                if d_min == 0 or d < d_min:
                    d_min = d

        return d_min 

    def indice_dunn(self):
    
        groups = self.order_cluster()
        keys = list(groups)

        if len(keys) < 2:
            raise ValueError("L'indice de Dunn nécessite d'avoir au moins 2 clusters") # Gestion d'erreurs

        # On prend le plus grand diamètre comme dénominateur
        max_diameter = 0

        for k in keys:
            d = self.diameter(groups[k])
            
            if d > max_diameter:
                max_diameter = d

        # On prend la plus petite séparation entre deux clusters comme numérateur
        min_separation = 0
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):     
                s = self.separation(groups[keys[i]], groups[keys[j]])

                if min_separation == 0 or s < min_separation:
                    min_separation = s

        if max_diameter == 0:
            raise ValueError("Tous les clusters ont un diamètre nul") # Nouvelle gestion d'erreur pour les tests.

        return min_separation / max_diameter