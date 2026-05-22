# Exercise 1

class Cat:
    def __init__(self, cat_name, cat_age):
        self.name = cat_name
        self.age = cat_age

# Étape 1 : Créer trois objets chat
cat1 = Cat("Félix", 5)
cat2 = Cat("Mistigri", 12)
cat3 = Cat("Gribouille", 8)

# Étape 2 : Créer une fonction pour trouver le chat le plus âgé
def find_oldest_cat(c1, c2, c3):
    # On compare les âges pour trouver le plus grand
    if c1.age >= c2.age and c1.age >= c3.age:
        return c1
    elif c2.age >= c1.age and c2.age >= c3.age:
        return c2
    else:
        return c3

# Étape 3 : Appeler la fonction et imprimer les informations
oldest_cat = find_oldest_cat(cat1, cat2, cat3)

print(f"Le chat le plus âgé est {oldest_cat.name}, et a {oldest_cat.age} ans.")

# Exercise 2

# Étape 1 : Créer la classe Dog
class Dog:
    def __init__(self, name, height):
        self.name = name
        self.height = height

    def bark(self):
        print(f"{self.name} fait Ouaf !")

    def jump(self):
        print(f"{self.name} saute {self.height * 2} cm de haut !")


# Étape 2 : Créer des objets chien
davids_dog = Dog("Rex", 50)
sarahs_dog = Dog("Bella", 35)

# Étape 3 : Afficher les infos et appeler les méthodes
print(f"Nom : {davids_dog.name}, Taille : {davids_dog.height} cm")
davids_dog.bark()
davids_dog.jump()

print(f"Nom : {sarahs_dog.name}, Taille : {sarahs_dog.height} cm")
sarahs_dog.bark()
sarahs_dog.jump()

# Étape 4 : Comparer la taille des chiens
if davids_dog.height > sarahs_dog.height:
    print(f"Le chien de David ({davids_dog.name}) est le plus grand.")
elif sarahs_dog.height > davids_dog.height:
    print(f"Le chien de Sarah ({sarahs_dog.name}) est le plus grand.")
else:
    print("Les deux chiens ont la même taille !")

    # Exercise 3
    # Étape 1 : Créer la classe Song
class Song:
    def __init__(self, lyrics):
        # lyrics est une liste de lignes de la chanson
        self.lyrics = lyrics

    def sing_me_a_song(self):
        # Afficher chaque ligne sur une nouvelle ligne
        for line in self.lyrics:
            print(line)


# Instanciation et appel de la méthode
stairway = Song([
    "There's a lady who's sure",
    "all that glitters is gold",
    "and she's buying a stairway to heaven"
])

stairway.sing_me_a_song()

# Exercise 4

class Zoo:
    def __init__(self, zoo_name):
        self.zoo_name = zoo_name
        self.animals = []  # Liste vide pour stocker les animaux

    # -----------------------------------------------
    # Étape : Ajouter un animal (sans doublon)
    # Bonus : *args permet d'ajouter plusieurs animaux
    # -----------------------------------------------
    def add_animal(self, *args):
        for new_animal in args:
            if new_animal not in self.animals:
                self.animals.append(new_animal)
                print(f"✅ {new_animal} a été ajouté au zoo {self.zoo_name}.")
            else:
                print(f"⚠️  {new_animal} est déjà dans le zoo !")

    # -----------------------------------------------
    # Étape : Afficher tous les animaux
    # -----------------------------------------------
    def get_animals(self):
        if self.animals:
            print(f"\n🦒 Animaux dans le zoo '{self.zoo_name}' :")
            for animal in self.animals:
                print(f"  - {animal}")
        else:
            print(f"\n🚫 Le zoo '{self.zoo_name}' est vide !")

    # -----------------------------------------------
    # Étape : Vendre (supprimer) un animal
    # -----------------------------------------------
    def sell_animal(self, animal_sold):
        if animal_sold in self.animals:
            self.animals.remove(animal_sold)
            print(f"\n💰 {animal_sold} a été vendu et retiré du zoo.")
        else:
            print(f"\n❌ {animal_sold} n'est pas dans le zoo !")

    # -----------------------------------------------
    # Étape : Trier et regrouper par première lettre
    # -----------------------------------------------
    def sort_animals(self):
        # Trier la liste alphabétiquement
        sorted_animals = sorted(self.animals)

        # Regrouper par première lettre dans un dictionnaire
        grouped = {}
        for animal in sorted_animals:
            first_letter = animal[0].upper()  # Première lettre en majuscule
            if first_letter not in grouped:
                grouped[first_letter] = []    # Créer une nouvelle clé
            grouped[first_letter].append(animal)

        return grouped

    # -----------------------------------------------
    # Étape : Afficher les groupes
    # -----------------------------------------------
    def get_groups(self):
        groups = self.sort_animals()
        print(f"\n📋 Animaux groupés par lettre dans '{self.zoo_name}' :")
        for letter, animals in groups.items():
            print(f"  {letter}: {animals}")


# -----------------------------------------------
# Étape 2 : Créer une instance du Zoo
# -----------------------------------------------
brooklyn_safari = Zoo("Brooklyn Safari")

# -----------------------------------------------
# Étape 3 : Tester toutes les méthodes
# -----------------------------------------------

# Ajout d'animaux un par un
brooklyn_safari.add_animal("Giraffe")
brooklyn_safari.add_animal("Bear")
brooklyn_safari.add_animal("Baboon")

# Test du doublon
brooklyn_safari.add_animal("Giraffe")

# Afficher les animaux
brooklyn_safari.get_animals()

# Vendre un animal
brooklyn_safari.sell_animal("Bear")

# Afficher après vente
brooklyn_safari.get_animals()

# Bonus : Ajouter plusieurs animaux en une seule ligne
brooklyn_safari.add_animal("Lion", "Zebra", "Cat", "Cougar")

# Afficher les groupes triés
brooklyn_safari.get_groups()