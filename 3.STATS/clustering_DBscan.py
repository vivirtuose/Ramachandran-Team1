import random
import math

class dbscan:
    def __init__(self, liste_point,eps,nb_point):
        self._liste_point = liste_point
        self._eps = eps
        self._nb_point = nb_point
        self._liste_k = []
        self._point_traite = set()

        if eps <= 0 or nb_point <= 0:
            raise ValueError ("la distance minimale/eps/nb_point ne doit pas être négative ou égale à 0")

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
        
    
    def clustering(self):
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



if __name__ == "__main__":
    # modele1 = dbscan([[1,2],[2,2],[1,1],[1,0],[10,9],[9,9],[10,10],[5,5]],3,2)
    # print(len(modele1.liste_point))
    # print(modele1.is_core(7))
    # print(modele1.is_neighbor(1))
    # print(modele1.liste_k)
    # modele1.liste_k = [[1,5,87],[75,89,12]]
    # print(modele1.liste_k)
    # print(modele1.is_traite(6))
    # print(modele1.liste_k[-1])
    # modele1.liste_k[-1].extend([12,15])
    # print(modele1.liste_k[-1])

    modele2 = dbscan([[1,2],[2,2],[1,1],[1,0],[10,9],[9,9],[10,10],[5,5]],3,2)
    modele2.clustering()
    print(modele2.liste_k)


