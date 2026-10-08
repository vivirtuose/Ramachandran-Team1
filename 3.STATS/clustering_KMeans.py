import random
import math
from Point import Point

class ClusterPoint(Point):

    def __init__(self, x, y, nb_cluster):
        super().__init__(x, y)
        self._nb_cluster = nb_cluster

    @property
    def nb_cluster(self):
        return self._nb_cluster

    @nb_cluster.setter
    def nb_cluster(self, value):
        self._nb_cluster = value


class ClusteringMethods:

    # Pour obtenir l'abcisse d'un point : liste_point[n° du point].get_abs()
    # Pour obtenir l'ordonnée d'un point : liste_point[n° du point].get_ord()
    # Les calculs de distance sont dans la classe Point :
    # Point.euclidean_distance(self, another_point) et Point.manhattan_distance(self, another_point)

    def __init__(self, liste_point):
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

    def add_to_liste_k(self, key, value):
        # .setdefault crée la clé est ajoute une valeur, ici, une liste vide.
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
                file.write("{:.6f}\t{:.6f}\t{}\n".format(p.get_abs(), p.get_ord(), p.nb_cluster))


class Kmeans(ClusteringMethods):

    def __init__(self, liste_point, k):
        super().__init__(liste_point)
        self._k = k

    @property
    def k(self):
        return self._k

    @k.setter
    def k(self, value):
        self._k = value

    def choose_initial_points(self):  # Les ajoute au dico
        indices = random.sample(range(len(self.liste_point)), self.k)
        for i, index in enumerate(indices):
            self.add_to_liste_k(i, self.liste_point[index])
            

    def clusterize(self):
        self.choose_initial_points()
        # initialise : 1 groupe = 1 centroide
        centroides = [self.liste_k[i][0] for i in range(self.k)]

        # On ne sait pas combien de tours on a à faire, donc on while True et on break la boucle quand c'est bon.
        while True: 
            # 1. Calcul du centroïde le plus proche
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
                # Si le groupe est vide (not groupe), pas de calcul de moyenne possible
                # Cas rare où le centroide se déplacerait loin des autres points
                if not groupe:
                    nouveaux.append(centroides[i])
                    continue
                c = Point(0, 0) # C'est un "somme = 0" un peu fancy et plus adapté à notre problème
                for p in groupe:
                    c.add(p)                        # add modifie c
                c.rescale(1 / len(groupe))
                nouveaux.append(c)

            # 3. convergence : les centroïdes n'ont plus bougé
            if all(n.euclidean_distance(c) == 0 for n, c in zip(nouveaux, centroides)):
                break
            centroides = nouveaux

    