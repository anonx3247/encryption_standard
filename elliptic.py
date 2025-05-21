import galois
import random

class Point:
    def __init__(self, x, y, z, curve, checks=True):
        self.curve = curve
        self.field = self.curve.field
        self.x = self.field(x)
        self.y = self.field(y)
        self.z = self.field(z)
        
        if checks:
            self._reduce()
            assert self.on_curve(), "Point non sur la courbe"

    def on_curve(self, curve=None):
        if curve is None:
            curve = self.curve
        return self.x**3 + curve.a*self.x + curve.b == self.y**2

    def _origin(self):
        return Point(self.field(0), self.field(1), self.field(0), self.curve, checks=False)
        
    
    def __neg__(self):
        return self.curve.point(self.x, -self.y)

    def _reduce(self):
        if self.z == self.field(0):
            self.x, self.y, self.z = self.field(0), self.field(1), self.field(0)
        if self.z == self.field(1):
            self.x, self.y, self.z = self.x, self.y, self.field(1)
        z_inv = self.z**(-1)
        self.x, self.y, self.z = self.x*z_inv, self.y*z_inv, self.field(1)
    
    def __eq__(self, other):
        return self.coordinates() == other.coordinates()
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def coordinates(self):
        return (self.x, self.y, self.z)
    
    def double(self):
        if self.y == self.field(0):
            return self.curve.infinity
        else:
            pente = (3*self.x**2 + self.curve.a) / (2*self.y)
            x_r = pente**2 - 2*self.x
            y_r = -self.y + pente*(self.x - x_r)
            return self.curve.point(x_r, y_r)
        
    def copy(self):
        return self.curve.point(self.x, self.y)

    def __add__(self, other):
        if other == self.curve.infinity:
            return self
        if self == self.curve.infinity:
            return other
        if self == -other:
            return self.curve.infinity
        
        if self.x == other.x:
            if self.y == other.y:
                return self.double()
            else:
                return self.curve.infinity
        else:
            pente = (other.y - self.y) / (other.x - self.x)
            x_r = pente**2 - self.x - other.x
            y_r = -self.y + pente*(x_r - self.x)
            return self.curve.point(x_r, y_r)
        
    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"
    
    def __mul__(self, scalar):
        if scalar == 0:
            return self.curve.infinity
        if scalar < 0:
            return -self * -scalar
        else:
            """
            Aux règles de calcul dans la courbe elliptique, on ajoute un algorithme qui simplifiera les multiplications. 
            Le principe est de décomposer un entier k en une somme et différence de puissances de 2 en minimisant les opérations d'additions 
            (les inverses sont moins coûteux). Dans un premier temps, on se contentera de décomposer k en binaire. 
            """
            P = self.copy()
            k = bin(scalar)[2:]
            for i in range(1, len(k)):
                P = P.double()
                if k[i] == "1":
                    P = P + self
            return P
        
    def order(self, max_iter=None):
        if self == self.curve.infinity:
            return 0
        else:
            k = 1
            while self * k != self.curve.infinity or max_iter is not None and k > max_iter:
                k += 1
                if max_iter is not None and k > max_iter:
                    return None
            return k

class Curve:
    def __init__(self, a, b, p):
        self.field = galois.GF(p)
        self.a = self.field(a)
        self.b = self.field(b)
        self.infinity = Point(self.field(0), self.field(1), self.field(0), self, checks=False)
    
    def discriminant(self):
        return -16*(4*self.a**3 + 27*self.b**2)
    
    def is_elliptic(self):
        return self.discriminant() != 0
    
    def point(self, x=1, y=1, checks=False):
        return Point(x, y, 1, self, checks=checks)
    
    def rand_point(self):
        x = random.randint(1, self.field.order())
        z = x**3 + self.a * x + self.b
    

p = 2**128 + 51
a = 2
b = 36

curve = Curve(a, b, p)
gen = curve.point(checks=True)