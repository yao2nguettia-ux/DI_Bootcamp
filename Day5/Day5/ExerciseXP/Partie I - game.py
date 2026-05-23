# game.py
import random

class Game:
    """
    Classe représentant une partie de Pierre-Feuille-Ciseaux.
    Contient toute la logique du jeu.
    """

    ITEMS = ["pierre", "feuille", "ciseaux"]

    # -------------------------------------------------------
    # Règles du jeu :
    #   pierre  bat  ciseaux
    #   ciseaux bat  feuille
    #   feuille bat  pierre
    # -------------------------------------------------------
    WINNING_COMBINATIONS = {
        "pierre":  "ciseaux",
        "ciseaux": "feuille",
        "feuille": "pierre",
    }

    def get_user_item(self):
        """
        Demande à l'utilisateur de choisir un élément.
        Répète la demande jusqu'à ce qu'un choix valide soit saisi.
        
        Retourne :
            str : l'élément choisi par l'utilisateur
        """
        while True:
            print("\n Choisissez votre élément :")
            print("  [1] Pierre")
            print("  [2] Feuille")
            print("  [3] Ciseaux")

            choix = input("\n Votre choix (1/2/3) : ").strip()

            # Validation de la saisie
            if choix == "1":
                return "pierre"
            elif choix == "2":
                return "feuille"
            elif choix == "3":
                return "ciseaux"
            else:
                print("❌ Choix invalide. Veuillez entrer 1, 2 ou 3.")

    def get_computer_item(self):
        """
        Sélectionne aléatoirement un élément pour l'ordinateur.
        
        Retourne :
            str : l'élément choisi aléatoirement par l'ordinateur
        """
        return random.choice(self.ITEMS)

    def get_game_result(self, user_item, computer_item):
        """
        Détermine le résultat du match.
        
        Paramètres :
            user_item     (str) : élément choisi par l'utilisateur
            computer_item (str) : élément choisi par l'ordinateur
        
        Retourne :
            str : "victoire", "match nul" ou "défaite"
        """
        # Égalité
        if user_item == computer_item:
            return "match nul"

        # Victoire : l'élément de l'utilisateur bat celui de l'ordinateur
        if self.WINNING_COMBINATIONS[user_item] == computer_item:
            return "victoire"

        # Sinon, défaite
        return "défaite"

    def play(self):
        """
        Fonction principale appelée depuis l'extérieur de la classe.
        Orchestre une partie complète :
          1. Récupère le choix de l'utilisateur
          2. Génère le choix de l'ordinateur
          3. Détermine et affiche le résultat
        
        Retourne :
            str : "victoire", "match nul" ou "défaite"
        """
        # Étape 1 : récupérer les choix
        user_item     = self.get_user_item()
        computer_item = self.get_computer_item()

        # Étape 2 : déterminer le résultat
        result = self.get_game_result(user_item, computer_item)

        # Étape 3 : afficher le résultat
        print("\n" + "=" * 45)
        print(f"Vous avez choisi     : {user_item.capitalize()}")
        print(f"L'ordinateur a choisi: {computer_item.capitalize()}")
        print("-" * 45)

        if result == "victoire":
            print("Résultat : Vous avez GAGNÉ !")
        elif result == "match nul":
            print("Résultat : Match NUL !")
        else:
            print("Résultat : Vous avez PERDU !")

        print("=" * 45)

        return result
