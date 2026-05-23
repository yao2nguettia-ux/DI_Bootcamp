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
    
    # main.py
from circle import Circle

# -------------------------------------------------------
# Séparateur visuel pour les sections de test
# -------------------------------------------------------
def section(titre):
    print(f"\n{'=' * 50}")
    print(f"  {titre}")
    print('=' * 50)


# -------------------------------------------------------
# 1️ Création de cercles
# -------------------------------------------------------
section("1. Création de cercles")

c1 = Circle(5)                    # Via le rayon
c2 = Circle.from_diameter(20)     # Via le diamètre → rayon = 10
c3 = Circle(3)
c4 = Circle(7)
c5 = Circle(5)                    # Même rayon que c1

print(f"c1 créé avec rayon    = 5  → {c1}")
print(f"c2 créé avec diamètre = 20 → {c2}")
print(f"c3 créé avec rayon    = 3  → {c3}")
print(f"c4 créé avec rayon    = 7  → {c4}")
print(f"c5 créé avec rayon    = 5  → {c5}")


# -------------------------------------------------------
# 2️ Accès au rayon et au diamètre
# -------------------------------------------------------
section("2. Rayon et Diamètre")

print(f"c1 → rayon    : {c1.radius}")
print(f"c1 → diamètre : {c1.diameter}")

# Modification via le setter du diamètre
c1.diameter = 14
print(f"\nc1 après c1.diameter = 14 :")
print(f"  → rayon    : {c1.radius}")
print(f"  → diamètre : {c1.diameter}")

# On remet le rayon à 5 pour la suite
c1 = Circle(5)


# -------------------------------------------------------
# 3️ Aire et Circonférence
# -------------------------------------------------------
section("3. Calculs géométriques")

print(f"c1 (r=5)  → aire          : {c1.area():.4f}")
print(f"c1 (r=5)  → circonférence : {c1.circumference():.4f}")
print(f"c2 (r=10) → aire          : {c2.area():.4f}")
print(f"c2 (r=10) → circonférence : {c2.circumference():.4f}")


# -------------------------------------------------------
# 4️ Affichage (__str__ et __repr__)
# -------------------------------------------------------
section("4. Affichage")

print(f"str(c1)  → {str(c1)}")
print(f"repr(c1) → {repr(c1)}")


# -------------------------------------------------------
# 5️ Addition de cercles
# -------------------------------------------------------
section("5. Addition de cercles")

c6 = c1 + c3   # rayon = 5 + 3 = 8
print(f"c1 (r=5) + c3 (r=3) = {c6}")

c7 = c2 + c4   # rayon = 10 + 7 = 17
print(f"c2 (r=10) + c4 (r=7) = {c7}")


# -------------------------------------------------------
# 6 Comparaisons
# -------------------------------------------------------
section("6. Comparaisons")

print(f"c1 (r=5) == c5 (r=5) → {c1 == c5}")   # True
print(f"c1 (r=5) == c3 (r=3) → {c1 == c3}")   # False
print(f"c2 (r=10) > c1 (r=5) → {c2 > c1}")    # True
print(f"c3 (r=3) > c4 (r=7)  → {c3 > c4}")    # False
print(f"c3 (r=3) < c4 (r=7)  → {c3 < c4}")    # True
print(f"c1 (r=5) >= c5 (r=5) → {c1 >= c5}")   # True
print(f"c4 (r=7) <= c2 (r=10)→ {c4 <= c2}")   # True


# -------------------------------------------------------
# 7 Tri d'une liste de cercles
# -------------------------------------------------------
section("7. Tri d'une liste de cercles")

cercles = [c2, c4, c3, c1, c5, c6, c7]

print("Avant le tri :")
for c in cercles:
    print(f"  {repr(c)}")

cercles_tries = sorted(cercles)

print("\nAprès le tri (ordre croissant) :")
for c in cercles_tries:
    print(f"  {repr(c)}")

print("\nAprès le tri (ordre décroissant) :")
for c in sorted(cercles, reverse=True):
    print(f"  {repr(c)}")


# -------------------------------------------------------
# gestion des erreurs
# -------------------------------------------------------
section("8. Gestion des erreurs")

try:
    c_invalid = Circle(-5)
except ValueError as e:
    print(f"Erreur capturée : {e}")

try:
    c_invalid = Circle.from_diameter(-10)
except ValueError as e:
    print(f"Erreur capturée : {e}")

try:
    result = c1 + 42   # Type incompatible
except TypeError as e:
    print(f"Erreur capturée : {e}")