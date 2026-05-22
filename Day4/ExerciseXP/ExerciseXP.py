# Exercise 1 : Les animaux de compagnie
class Pets():
    def __init__(self, animals):
        self.animals = animals

    def walk(self):
        for animal in self.animals:
            print(animal.walk())

class Cat():
    is_lazy = True

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def walk(self):
        return f'{self.name} is just walking around'

class Bengal(Cat):
    def sing(self, sounds):
        return f'{sounds}'

class Chartreux(Cat):
    def sing(self, sounds):
        return f'{sounds}'

# Étape 1 : Créer la classe Siamese qui hérite de Cat
class Siamese(Cat):
    def sing(self, sounds):
        return f'{sounds}'

# Étape 2 : Créer une liste d'instances de chats
bengal_cat    = Bengal("Simba", 3)
chartreux_cat = Chartreux("Luna", 5)
siamese_cat   = Siamese("Milo", 2)

all_cats = [bengal_cat, chartreux_cat, siamese_cat]

# Étape 3 : Créer une instance de Pets
sara_pets = Pets(all_cats)

# Étape 4 : Emmener les chats en promenade
sara_pets.walk()

# Exercice 2 : Les chiens
class Dog:
    # Étape 1 : Créer la classe Dog avec ses attributs et méthodes
    def __init__(self, name, age, weight):
        self.name   = name
        self.age    = age
        self.weight = weight

    def bark(self):
        return f'{self.name} barks'

    def run_speed(self):
        return self.weight / self.age * 10

    def fight(self, other_dog):
        # La puissance de combat = vitesse * poids
        my_power    = self.run_speed()    * self.weight
        other_power = other_dog.run_speed() * other_dog.weight

        if my_power > other_power:
            return f'{self.name} a gagné le combat contre {other_dog.name} !'
        elif other_power > my_power:
            return f'{other_dog.name} a gagné le combat contre {self.name} !'
        else:
            return f'Match nul entre {self.name} et {other_dog.name} !'

# Étape 2 : Créer trois instances de Dog
dog1 = Dog("Rex",   3, 30)
dog2 = Dog("Bella", 5, 20)
dog3 = Dog("Max",   2, 25)

# Étape 3 : Tester les méthodes
print(dog1.bark())
print(dog2.bark())
print(dog3.bark())

print(f"Vitesse de {dog1.name} : {dog1.run_speed():.2f}")
print(f"Vitesse de {dog2.name} : {dog2.run_speed():.2f}")
print(f"Vitesse de {dog3.name} : {dog3.run_speed():.2f}")

print(dog1.fight(dog2))
print(dog2.fight(dog3))
print(dog1.fight(dog3))

# Exercice 3 : Les chiens de compagnie

import random
from exercise_2 import Dog  # Étape 1 : Importer la classe Dog

# Étape 2 : Créer la classe PetDog qui hérite de Dog
class PetDog(Dog):
    def __init__(self, name, age, weight):
        super().__init__(name, age, weight)  # Appel du constructeur parent
        self.trained = False                  # Attribut supplémentaire

    def train(self):
        print(self.bark())    # Affiche le résultat de bark()
        self.trained = True   # Le chien est maintenant dressé

    def play(self, *args):
        # Rassemble tous les noms (self + les autres chiens passés en args)
        dog_names = ", ".join([dog.name for dog in args])
        print(f"{self.name}, {dog_names} jouent tous ensemble !")

    def do_a_trick(self):
        if self.trained:
            tricks = [
                "does a barrel roll",
                "stands on his back legs",
                "shakes your hand",
                "plays dead"
            ]
            print(f"{self.name} {random.choice(tricks)}")
        else:
            print(f"{self.name} n'est pas encore dressé !")

# Étape 3 : Tester les méthodes de PetDog
dog_a = PetDog("Fido",  2, 10)
dog_b = PetDog("Buddy", 4, 15)
dog_c = PetDog("Max",   3, 12)

# Test de train()
dog_a.train()

# Test de do_a_trick() avant et après entraînement
dog_b.do_a_trick()  # Pas encore dressé
dog_b.train()
dog_b.do_a_trick()  # Dressé → affiche un tour aléatoire

# Test de play()
dog_a.play(dog_b, dog_c)

# Exercice 4 : La famille

# Étape 1 : Créer la classe Person
class Person:
    def __init__(self, first_name, age):
        self.first_name = first_name
        self.age        = age
        self.last_name  = ""       # Initialisé vide, assigné par Family

    def is_18(self):
        return self.age >= 18      # Retourne True si majeur, sinon False


#  Étape 2 : Créer la classe Family
class Family:
    def __init__(self, last_name):
        self.last_name = last_name
        self.members   = []        # Liste vide pour stocker les membres

    def born(self, first_name, age):
        """Crée un nouveau membre et l'ajoute à la famille."""
        new_person           = Person(first_name, age)
        new_person.last_name = self.last_name   # Attribue le nom de famille
        self.members.append(new_person)
        print(f"Bienvenue dans la famille, {first_name} {self.last_name} !")

    def check_majority(self, first_name):
        """Vérifie si un membre est majeur."""
        for member in self.members:
            if member.first_name == first_name:
                if member.is_18():
                    print(
                        "You are over 18, your parents Jane and John "
                        "accept that you will go out with your friends"
                    )
                else:
                    print("Sorry, you are not allowed to go out with your friends.")
                return  # On arrête la recherche une fois trouvé

        print(f"{first_name} n'est pas membre de cette famille.")

    def family_presentation(self):
        """Affiche les informations de la famille."""
        print(f"\n👨‍👩‍👧‍👦 Famille {self.last_name} :")
        print("-" * 30)
        for member in self.members:
            print(f"  - {member.first_name} {member.last_name}, {member.age} ans")
        print("-" * 30)


#  Tests complets
my_family = Family("Dupont")

# Ajout de membres
my_family.born("Alice",  25)
my_family.born("Bob",    15)
my_family.born("Claire", 18)

# Vérification de majorité
print()
my_family.check_majority("Alice")    # Majeure 
my_family.check_majority("Bob")      # Mineur 
my_family.check_majority("Claire")   # Exactement 18 

# Présentation de la famille
my_family.family_presentation()

