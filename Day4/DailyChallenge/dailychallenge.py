import math


class Pagination:
    """
    Classe simulant un système de pagination basique.
    
    Exemple visuel :
    Page 1      Page 2      Page 3
    [a, b, c]   [d, e, f]   [g, h, i]
    """

    # Étape 2 : Implémenter la méthode __init__
    def __init__(self, items=None, page_size=10):
        """
        Initialise la pagination.
        
        Args:
            items     : Liste d'éléments à paginer (None par défaut → liste vide)
            page_size : Nombre d'éléments par page (10 par défaut)
        """
        # Si aucune liste fournie, on initialise une liste vide
        self.items       = items if items is not None else []
        self.page_size   = page_size
        self.current_idx = 0   # Index interne (commence à 0)

        # Calcul du nombre total de pages avec math.ceil
        # Ex: 26 lettres / 4 par page = ceil(6.5) = 7 pages
        self.total_pages = math.ceil(len(self.items) / self.page_size)

    # Étape 3 : Retourner les éléments visibles sur la page actuelle
    def get_visible_items(self):
        """
        Retourne la liste des éléments de la page courante.
        
        Utilise le slicing basé sur current_idx et page_size.
        Ex: page 0 → items[0:4], page 1 → items[4:8], etc.
        """
        start = self.current_idx * self.page_size
        end   = start + self.page_size
        return self.items[start:end]

    # Étape 4 : Méthodes de navigation
    def go_to_page(self, page_num):
        """
        Accède à la page spécifiée (indexation utilisateur à partir de 1).
        
        Lève une ValueError si page_num est hors limites.
        
        Args:
            page_num : Numéro de page (commence à 1 pour l'utilisateur)
        """
        # Conversion en entier au cas où une string est passée
        page_num = int(page_num)

        # Vérification des limites (l'utilisateur utilise des pages à partir de 1)
        if page_num < 1 or page_num > self.total_pages:
            raise ValueError(
                f"Page {page_num} invalide. "
                f"Choisissez une page entre 1 et {self.total_pages}."
            )

        # Conversion : page utilisateur (base 1) → index interne (base 0)
        self.current_idx = page_num - 1
        return self   # Retourne self pour le chaînage de méthodes

    def first_page(self):
        """Accède à la première page (index 0)."""
        self.current_idx = 0
        return self   # Retourne self pour le chaînage de méthodes

    def last_page(self):
        """Accède à la dernière page."""
        self.current_idx = self.total_pages - 1
        return self   # Retourne self pour le chaînage de méthodes

    def next_page(self):
        """
        Passe à la page suivante.
        Ne fait rien si on est déjà sur la dernière page.
        """
        if self.current_idx < self.total_pages - 1:
            self.current_idx += 1
        return self   # Retourne self pour le chaînage de méthodes

    def previous_page(self):
        """
        Revient à la page précédente.
        Ne fait rien si on est déjà sur la première page.
        """
        if self.current_idx > 0:
            self.current_idx -= 1
        return self   #  Retourne self pour le chaînage de méthodes

    # Étape 5 (Bonus) : Méthode __str__ personnalisée
    def __str__(self):
        """
        Retourne une chaîne affichant les éléments de la page actuelle,
        chacun sur une nouvelle ligne.
        
        Ex: 'a\nb\nc\nd'
        """
        return "\n".join(str(item) for item in self.get_visible_items())


# ============================================================
# Étape 6 : Tests
# ============================================================

alphabetList = list("abcdefghijklmnopqrstuvwxyz")
p = Pagination(alphabetList, 4)

print("=" * 40)
print("Test __str__ (page 1) :")
print(str(p))
# a
# b
# c
# d

print("\n" + "=" * 40)
print("Test get_visible_items() - Page 1 :")
print(p.get_visible_items())
# ['a', 'b', 'c', 'd']

print("\n" + "=" * 40)
print("Test next_page() - Page 2 :")
p.next_page()
print(p.get_visible_items())
# ['e', 'f', 'g', 'h']

print("\n" + "=" * 40)
print("Test last_page() - Dernière page :")
p.last_page()
print(p.get_visible_items())
# ['y', 'z']

print("\n" + "=" * 40)
print("Test first_page() - Retour à la page 1 :")
p.first_page()
print(p.get_visible_items())
# ['a', 'b', 'c', 'd']

print("\n" + "=" * 40)
print("Test previous_page() sur la page 1 (aucun effet) :")
p.previous_page()
print(p.get_visible_items())
# ['a', 'b', 'c', 'd']

print("\n" + "=" * 40)
print("Test chaînage : next_page x3 → get_visible_items :")
p.first_page()
result = p.next_page().next_page().next_page().get_visible_items()
print(result)
# ['m', 'n', 'o', 'p']

print("\n" + "=" * 40)
print("Test go_to_page(10) - Doit lever ValueError :")
try:
    p.go_to_page(10)
except ValueError as e:
    print(f"ValueError capturée → {e}")
# ValueError: Page 10 invalide. Choisissez une page entre 1 et 7.

print("\n" + "=" * 40)
print("Test go_to_page(0) - Doit lever ValueError :")
try:
    p.go_to_page(0)
except ValueError as e:
    print(f"ValueError capturée → {e}")
# ValueError: Page 0 invalide. Choisissez une page entre 1 et 7.