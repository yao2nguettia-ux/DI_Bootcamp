class Farm:
    # -----------------------------------------------
    # Étape 2 : Initialisation de la ferme
    # -----------------------------------------------
    def __init__(self, farm_name):
        self.name = farm_name
        self.animals = {}  # Dictionnaire vide : {'cow': 5, 'sheep': 2}

    # -----------------------------------------------
    # Étape 3 : Ajouter un animal au dictionnaire
    # Étape 8 (Bonus) : Utiliser **kwargs pour
    #                   ajouter plusieurs animaux
    # -----------------------------------------------
    def add_animal(self, animal_type=None, count=1, **kwargs):
        # Cas normal : un seul animal passé en argument positionnel
        if animal_type is not None:
            if animal_type in self.animals:
                # L'animal existe déjà → on incrémente son compteur
                self.animals[animal_type] += count
            else:
                # Nouvel animal → on l'ajoute avec son compteur
                self.animals[animal_type] = count

        # Bonus : plusieurs animaux passés via **kwargs
        # Appel : macdonald.add_animal(cow=5, sheep=2, goat=12)
        for animal, number in kwargs.items():
            if animal in self.animals:
                self.animals[animal] += number
            else:
                self.animals[animal] = number

    # -----------------------------------------------
    # Étape 4 : Afficher les informations de la ferme
    # -----------------------------------------------
    def get_info(self):
        # En-tête avec le nom de la ferme
        info = f"{self.name}'s farm\n\n"

        # Afficher chaque animal et sa quantité
        for animal, count in self.animals.items():
            # :<10 aligne le nom sur 10 caractères à gauche
            info += f"{animal:<10} : {count}\n"

        # Pied de page
        info += "\n    E-I-E-I-0!"
        return info

    # -----------------------------------------------
    # Étape 6 (Bonus) : Retourner les types d'animaux
    #                   triés alphabétiquement
    # -----------------------------------------------
    def get_animal_types(self):
        # sorted() retourne une liste triée des clés du dictionnaire
        return sorted(self.animals.keys())

    # -----------------------------------------------
    # Étape 7 (Bonus) : Retourner une phrase résumée
    # -----------------------------------------------
    def get_short_info(self):
        animal_types = self.get_animal_types()

        # Ajouter un 's' si le nombre d'animaux est supérieur à 1
        animal_list = []
        for animal in animal_types:
            if self.animals[animal] > 1:
                animal_list.append(animal + "s")  # pluriel
            else:
                animal_list.append(animal)        # singulier

        # Construire la phrase selon le nombre d'animaux
        if len(animal_list) == 1:
            # Un seul type d'animal
            animals_str = animal_list[0]
        elif len(animal_list) == 2:
            # Deux types : "cows and goats"
            animals_str = f"{animal_list[0]} and {animal_list[1]}"
        else:
            # Trois types ou plus : "cows, goats and sheeps"
            animals_str = ", ".join(animal_list[:-1]) + f" and {animal_list[-1]}"

        return f"{self.name}'s farm has {animals_str}."


# -----------------------------------------------
# Étape 5 : Tester le code
# -----------------------------------------------
macdonald = Farm("McDonald")

# Ajout d'animaux un par un (méthode normale)
macdonald.add_animal('cow', 5)
macdonald.add_animal('sheep')       # count=1 par défaut
macdonald.add_animal('sheep')       # sheep passe de 1 à 2
macdonald.add_animal('goat', 12)

print("=" * 30)
print(macdonald.get_info())

print("=" * 30)
# Étape 6 : Types d'animaux triés
print("Types d'animaux :", macdonald.get_animal_types())

print("=" * 30)
# Étape 7 : Phrase résumée
print(macdonald.get_short_info())

print("=" * 30)
# Étape 8 : Ajouter plusieurs animaux via **kwargs
macdonald.add_animal(horse=3, chicken=10, duck=1)
print(macdonald.get_info())
print(macdonald.get_short_info())