# rock-paper-scissors.py
from game import Game

# -------------------------------------------------------
# Fonctions principales du menu et de la gestion du jeu
# -------------------------------------------------------

def get_user_menu_choice():
    """
    Affiche le menu principal et récupère le choix de l'utilisateur.
    Valide la saisie sans boucle interne.
    
    Retourne :
        str : le choix validé de l'utilisateur ("1", "2", "q")
    """
    print("\n" + "=" * 45)
    print("       🎮 PIERRE - FEUILLE - CISEAUX")
    print("=" * 45)
    print("  [1] Jouer une nouvelle partie")
    print("  [2] Afficher les scores")
    print("  [q] Quitter")
    print("-" * 45)

    choix = input("👉 Votre choix : ").strip().lower()

    # Validation : on accepte uniquement les choix valides
    if choix in ("1", "2", "q"):
        return choix
    else:
        print("❌ Choix invalide. Veuillez entrer 1, 2 ou q.")
        return None  # On retourne None pour signaler un choix invalide


def print_results(results):
    """
    Affiche un résumé convivial de toutes les parties jouées.
    
    Paramètres :
        results (dict) : dictionnaire au format
                         {"victoire": int, "défaite": int, "match nul": int}
    """
    total = results["victoire"] + results["défaite"] + results["match nul"]

    print("\n" + "=" * 45)
    print("       📊 RÉSUMÉ DE VOS PARTIES")
    print("=" * 45)
    print(f"  🎮 Parties jouées : {total}")
    print(f"  🏆 Victoires      : {results['victoire']}")
    print(f"  😢 Défaites       : {results['défaite']}")
    print(f"  🤝 Matchs nuls    : {results['match nul']}")
    print("-" * 45)

    # Message personnalisé selon les résultats
    if total == 0:
        print("  Vous n'avez joué aucune partie.")
    elif results["victoire"] > results["défaite"]:
        print("  🌟 Bravo ! Vous avez dominé l'ordinateur !")
    elif results["victoire"] < results["défaite"]:
        print("  💪 L'ordinateur a gagné cette fois... Revenez !")
    else:
        print("  ⚖️  Égalité parfaite entre vous et l'ordinateur !")

    print("=" * 45)
    print("\n  Merci d'avoir joué ! À bientôt ! 👋")
    print("=" * 45 + "\n")


def main():
    """
    Fonction principale du programme.
    Gère la boucle de menu, les parties et le résumé final.
    """
    # Initialisation du dictionnaire des résultats
    results = {
        "victoire":  0,
        "défaite":   0,
        "match nul": 0,
    }

    print("\n  Bienvenue dans Pierre - Feuille - Ciseaux ! 🎉")

    # Boucle principale du menu
    while True:
        choix = get_user_menu_choice()

        # --- Choix invalide : on recommence ---
        if choix is None:
            continue

        # --- Jouer une partie ---
        if choix == "1":
            partie = Game()           # Créer un nouvel objet Game
            result = partie.play()    # Lancer la partie et récupérer le résultat

            # Mémoriser le résultat
            results[result] += 1

        # --- Afficher les scores ---
        elif choix == "2":
            print_results(results)

        # --- Quitter ---
        elif choix == "q":
            # Afficher le résumé final avant de quitter
            print_results(results)
            break


# -------------------------------------------------------
# Point d'entrée du programme
# -------------------------------------------------------
if __name__ == "__main__":
    main()