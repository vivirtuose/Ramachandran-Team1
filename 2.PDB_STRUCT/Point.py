from math import sqrt

class Point:
    """
    La classe Point définit des objets qui sont des points dans un plan.
        x = (float) l'abscisse du point dans le plan
        y = (float) l'ordonnée du point dans le plan
    """

    def __init__(self, x = 0.00, y = 0.00):
        self._abs = x 
        self._ord = y   

    def __str__(self):
        return f"Point of coordinates ({self.x:.4f}, {self.y:.4f})"

    @property
    def x(self):
        return self._abs
    @property    
    def y(self):
        return self._ord

    @x.setter
    def x(self, value):
        self._abs = value
    @y.setter
    def y(self, value):
        self._ord = value


    def add(self, another_point):
        """
        Functions that adds to the current Point to another point passed as an argument
        """
        self.x += another_point.x
        self.y += another_point.y
        return


    def rescale(self, factor):
        """
        Functions that rescales the current Point by a scalar passed as an argument
        """
        self.x *= factor
        self.y *= factor
        return 


    def distance_from_origin(self):	
        """
        Functions that computes the distance of the current Point to the origin of the plan O
        """
        return sqrt(self.x**2 + self.y**2)


    def euclidean_distance(self, another_point):
        """
        Functions that computes the euclidean distance of the current Point with another point passed as an argument
        """
        return sqrt((self.x - another_point.x) ** 2 + (self.y - another_point.y) ** 2)


    def manhattan_distance(self, another_point):
        """
        Functions that computes the manhattan distance of the current Point with another point passed as an argument
        """
        return abs(self.x - another_point.x) + abs(self.y - another_point.y)

    
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
    assert pD.distance_from_origin() == 5, 'Error in Point.distance_from_origin'
    assert pB.euclidean_distance(pC) == 1, 'Error in Point.distance'
    assert pB.manhattan_distance(pC) == 1, 'Error in Point.distance'