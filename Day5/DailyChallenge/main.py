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