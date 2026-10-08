from math import sqrt


class Point:
    """
    La classe Point définit des objets qui sont des points dans un plan.
        x = (float) l'abscisse du point dans le plan
        y = (float) l'ordonnée du point dans le plan
    """

    def __init__(self, x = 0.00, y = 0.00):
        if isinstance(x, (int, float)) and isinstance(y , (int, float)):
            self._abs = x 
            self._ord = y
        else:
            raise TypeError()

    def __str__(self):
        return f"Point of coordinates ({self.x:.4f}, {self.y:.4f})"

    # accesseur
    @property
    def x(self):
        return self._abs
    @property    
    def y(self):
        return self._ord

    # mutateur
    @x.setter
    def x(self, value):
        self._abs = value
    @y.setter
    def y(self, value):
        self._ord = value

    def add(self, another_point):
        """
        Fonction qui recalcul les coordonnées du point actuel en 
        l'additionnant avec un autre point passé en argument     
        """
        if isinstance(another_point, Point):
            self.x += another_point.x
            self.y += another_point.y
            return
        else:
            raise TypeError()


    def rescale(self, factor):
        """
        Fonction qui recalcul les coordonnées du point actuel en le 
        multipliant par un scalaire passé en argument
        """
        if isinstance(factor, (int, float)):
            self.x *= factor
            self.y *= factor
            return
        else:
            raise TypeError()


    def distance_from_origin(self):	
        """
        Fonction qui calcul la distance à l'origine du point actuel
        """
        return sqrt(self.x**2 + self.y**2)


    def euclidean_distance(self, another_point):
        """
        Fonction qui calcul la distance euclidienne entre le point actuel et
        un point passé en argument.
        """
        if isinstance(another_point, Point):
            return sqrt((self.x - another_point.x) ** 2 +
                        (self.y - another_point.y) ** 2)
        else:
            raise TypeError()


    def manhattan_distance(self, another_point):
        """
        Fonction qui calcul la distance manhattan entre le point actuel et
        un point passé en argument.
        """
        if isinstance(another_point, Point):
            return abs(self.x - another_point.x) + abs(self.y - another_point.y)
        else:
            raise TypeError()

    
if __name__ == "__main__":	
    pA = Point(0,0)
    pB = Point(1,1)
    pC = Point(2,1)
    pD = Point(3,4)

    print(pA)
    print(pB)
    print(pC)
    print(pD)

    pA.add(pB)
    assert pA.x == 1, 'Error in Point.add'
    pA.rescale(5)
    assert pA.x == 5, 'Error in Point.rescale'
    assert pD.distance_from_origin() == 5, 'Error in Point.distance_\
        from_origin'
    assert pB.euclidean_distance(pC) == 1, 'Error in Point.distance'
    assert pB.manhattan_distance(pC) == 1, 'Error in Point.distance'