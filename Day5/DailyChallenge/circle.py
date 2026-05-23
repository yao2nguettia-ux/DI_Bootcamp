# circle.py
import math


class Circle:
    """
    Classe représentant un cercle.
    Peut être créé via le rayon ou le diamètre (décorateur @classmethod).
    
    Attributs :
        radius (float) : le rayon du cercle
    """

    def __init__(self, radius):
        """
        Initialise un cercle avec un rayon.
        
        Paramètres :
            radius (float) : le rayon du cercle
        """
        if radius < 0:
            raise ValueError(" Le rayon ne peut pas être négatif.")
        self.radius = radius

    # -------------------------------------------------------
    #  Constructeur alternatif : créer un cercle via le diamètre
    # -------------------------------------------------------
    @classmethod
    def from_diameter(cls, diameter):
        """
        Crée un cercle à partir de son diamètre.
        
        Paramètres :
            diameter (float) : le diamètre du cercle
        
        Retourne :
            Circle : une nouvelle instance de Circle
        
        Exemple :
            c = Circle.from_diameter(10)  # rayon = 5
        """
        if diameter < 0:
            raise ValueError(" Le diamètre ne peut pas être négatif.")
        return cls(diameter / 2)

    # -------------------------------------------------------
    #  Propriétés : rayon et diamètre
    # -------------------------------------------------------
    @property
    def diameter(self):
        """
        Retourne le diamètre du cercle.
        
        Retourne :
            float : le diamètre (rayon × 2)
        """
        return self.radius * 2

    @diameter.setter
    def diameter(self, value):
        """
        Permet de modifier le diamètre (met à jour le rayon).
        
        Paramètres :
            value (float) : nouveau diamètre
        """
        if value < 0:
            raise ValueError(" Le diamètre ne peut pas être négatif.")
        self.radius = value / 2

    # -------------------------------------------------------
    #  Calculs géométriques
    # -------------------------------------------------------
    def area(self):
        """
        Calcule et retourne l'aire du cercle.
        
        Formule : π × r²
        
        Retourne :
            float : l'aire du cercle
        """
        return math.pi * self.radius ** 2

    def circumference(self):
        """
        Calcule et retourne la circonférence du cercle.
        
        Formule : 2 × π × r
        
        Retourne :
            float : la circonférence du cercle
        """
        return 2 * math.pi * self.radius

    # -------------------------------------------------------
    #  Méthodes dunder : affichage
    # -------------------------------------------------------
    def __str__(self):
        """
        Retourne une représentation lisible du cercle.
        Utilisé par print().
        """
        return (
            f"Circle("
            f"rayon={self.radius:.2f}, "
            f"diamètre={self.diameter:.2f}, "
            f"aire={self.area():.2f}, "
            f"circonférence={self.circumference():.2f})"
        )

    def __repr__(self):
        """
        Retourne une représentation technique du cercle.
        Utilisé dans les listes, le débogage, etc.
        """
        return f"Circle(radius={self.radius})"

    # -------------------------------------------------------
    #  Méthode dunder : addition de deux cercles
    # -------------------------------------------------------
    def __add__(self, other):
        """
        Additionne deux cercles : retourne un nouveau cercle
        dont le rayon est la somme des deux rayons.
        
        Paramètres :
            other (Circle) : le deuxième cercle
        
        Retourne :
            Circle : nouveau cercle avec le rayon combiné
        
        Exemple :
            c3 = c1 + c2
        """
        if not isinstance(other, Circle):
            raise TypeError(
                f"Impossible d'additionner Circle et {type(other).__name__}"
            )
        return Circle(self.radius + other.radius)

    # -------------------------------------------------------
    # Méthodes de comparaison
    # -------------------------------------------------------
    def __eq__(self, other):
        """
        Vérifie si deux cercles sont égaux (même rayon).
        
        Retourne :
            bool : True si les rayons sont égaux
        
        Exemple :
            c1 == c2
        """
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius == other.radius

    def __gt__(self, other):
        """
        Vérifie si ce cercle est plus grand qu'un autre.
        
        Retourne :
            bool : True si self.radius > other.radius
        
        Exemple :
            c1 > c2
        """
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius > other.radius

    def __lt__(self, other):
        """
        Vérifie si ce cercle est plus petit qu'un autre.
        Nécessaire pour le tri avec sorted() ou list.sort().
        
        Retourne :
            bool : True si self.radius < other.radius
        
        Exemple :
            c1 < c2
            sorted([c1, c2, c3]) 
        """
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius < other.radius

    def __ge__(self, other):
        """Vérifie si ce cercle est plus grand ou égal à un autre."""
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius >= other.radius

    def __le__(self, other):
        """Vérifie si ce cercle est plus petit ou égal à un autre."""
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius <= other.radius