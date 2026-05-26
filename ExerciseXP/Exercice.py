import pandas as pd
import numpy as np
from io import StringIO

# ------------------------------------------------------------
# EXERCICE 1 : Qu'est-ce que l'analyse de données ?
# ------------------------------------------------------------
print("=== EXERCICE 1 ===")
print("L'analyse de données consiste à extraire des informations utiles à partir de données brutes.")
print("Exemple concret : analyse des ventes d'une boutique")

# Simulation des données de boutique
ventes = pd.DataFrame({
    'Jour': ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'],
    'Produit_A': [12, 15, 10, 18, 22, 30],
    'Produit_B': [5, 7, 6, 8, 10, 12],
    'Nb_clients': [30, 35, 28, 40, 55, 70]
})
print("Données de ventes sur une semaine :")
print(ventes)

# Réponses aux questions
produit_plus_vendu = ventes[['Produit_A', 'Produit_B']].sum().idxmax()
jour_moins_monde = ventes.loc[ventes['Nb_clients'].idxmin(), 'Jour']
print(f"\n→ Quel produit se vend le plus ? {produit_plus_vendu} → en commander plus.")
print(f"→ Quel jour y a-t-il le moins de monde ? {jour_moins_monde} → faire une promotion ce jour-là.")

# ------------------------------------------------------------
# EXERCICE 2 : Présentation des trois jeux de données
# ------------------------------------------------------------
print("\n=== EXERCICE 2 ===")
print("Trois jeux de données présentés :")
print("1. Sommeil des Américains (Time Americans Spend Sleeping.csv)")
print("2. Troubles de santé mentale (Mental health Depression disorder Data.csv)")
print("3. Approbation de cartes de crédit (clean_dataset.csv)")

# ------------------------------------------------------------
# EXERCICE 3 : Typage des colonnes (exemple avec le dataset Sommeil)
# ------------------------------------------------------------
print("\n=== EXERCICE 3 ===")
print("Typage des colonnes du jeu de données 'Sommeil des Américains' :")
# On crée un DataFrame fictif représentant la structure
sleep_data = pd.DataFrame({
    'index': [1, 2],
    'Year': [2003, 2004],
    'Period': ['Annual', 'Annual'],
    'Avg hrs per day sleeping': [7.8, 7.9],
    'Standard Error': [0.05, 0.04],
    'Type of Days': ['All days', 'Weekend days and holidays'],
    'Age Group': ['15 to 24 years', '25 to 34 years'],
    'Activity': ['Sleeping', 'Sleeping'],
    'Sex': ['Both', 'Men']
})

type_info = []
for col in sleep_data.columns:
    if col in ['index', 'Year', 'Avg hrs per day sleeping', 'Standard Error']:
        typ = "Quantitative"
    else:
        typ = "Qualitative"
    type_info.append((col, typ))
print(pd.DataFrame(type_info, columns=['Colonne', 'Type']))

# ------------------------------------------------------------
# EXERCICE 4 : Charger Iris.csv et distinguer qualitatives/quantitatives
# ------------------------------------------------------------
print("\n=== EXERCICE 4 ===")
# Chargement du dataset Iris depuis une URL
url_iris = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
cols = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm', 'Species']
df_iris = pd.read_csv(url_iris, names=cols)
print("Aperçu du dataset Iris :")
print(df_iris.head())

qualitatives = df_iris.select_dtypes(include=['object']).columns.tolist()
quantitatives = df_iris.select_dtypes(include=['float64', 'int64']).columns.tolist()
print(f"\nColonnes qualitatives : {qualitatives}")
print(f"Colonnes quantitatives : {quantitatives}")

# ------------------------------------------------------------
# EXERCICE 5 : Analyse du dataset Sommeil (simulation)
# ------------------------------------------------------------
print("\n=== EXERCICE 5 ===")
# Génération de données simulées pour le sommeil
np.random.seed(42)
years = list(range(2003, 2018))
age_groups = ['15-24', '25-34', '35-44', '45-54', '55-64', '65+']
sexes = ['Men', 'Women', 'Both']
day_types = ['All days', 'Weekdays', 'Weekend']

data_rows = []
for y in years:
    for age in age_groups:
        for sex in sexes:
            for day in day_types:
                avg_sleep = 7.5 + np.random.normal(0, 0.3)
                std_err = np.random.uniform(0.02, 0.1)
                data_rows.append([y, age, sex, day, avg_sleep, std_err])
df_sleep = pd.DataFrame(data_rows, columns=['Year', 'AgeGroup', 'Sex', 'TypeOfDays', 'AvgSleep', 'StdError'])

# 1. Tendance temporelle
trend = df_sleep.groupby('Year')['AvgSleep'].mean()
print("Tendance moyenne du sommeil par année :")
print(trend.head())

# 2. Comparaison hommes/femmes
comp_sex = df_sleep.groupby('Sex')['AvgSleep'].mean()
print("\nComparaison hommes/femmes :")
print(comp_sex)

# 3. Effet week-end/semaine
comp_days = df_sleep.groupby('TypeOfDays')['AvgSleep'].mean()
print("\nComparaison type de jour :")
print(comp_days)

# 4. Effet de l'âge
comp_age = df_sleep.groupby('AgeGroup')['AvgSleep'].mean()
print("\nComparaison tranches d'âge :")
print(comp_age)

# ------------------------------------------------------------
# EXERCICE 6 : Structuré vs Non structuré
# ------------------------------------------------------------
print("\n=== EXERCICE 6 ===")
sources = [
    ("Rapports financiers dans un fichier Excel", "Structuré"),
    ("Photographies sur une plateforme de médias sociaux", "Non structuré"),
    ("Collection d'articles de presse sur un site web", "Non structuré"),
    ("Données d'inventaire dans une base de données relationnelle", "Structuré"),
    ("Enregistrements d'entretiens d'une étude de marché", "Non structuré")
]
df_types = pd.DataFrame(sources, columns=["Source de données", "Type"])
print(df_types.to_string(index=False))

# ------------------------------------------------------------
# EXERCICE 7 : Transformation de non structuré en structuré
# ------------------------------------------------------------
print("\n=== EXERCICE 7 ===")
print("Exemples de transformations :")
print("- Articles de blog (texte) → tableau CSV via NLP (extraction destination, budget, etc.)")
print("- Enregistrements audio → transcription ASR puis extraction de données structurées")
print("- Notes manuscrites → OCR puis mise en tableau (thème, idée, priorité)")
print("- Tutoriel vidéo → découpage temporel + extraction des étapes (ingrédients, durée)")

# Simulation pour les articles de blog
articles = [
    "Je suis allé à Paris en mai pour 5 jours, budget 800€. J'ai adoré la Tour Eiffel.",
    "Séjour à Londres en juillet, 3 jours, 600€. Visite du British Museum."
]
print("\nExemple de structuration d'articles :")
structured = []
for i, art in enumerate(articles):
    # Extraction basique (simulée)
    if "Paris" in art:
        dest = "Paris"
    else:
        dest = "Londres"
    if "5 jours" in art:
        duree = 5
    else:
        duree = 3
    structured.append({"article_id": i+1, "destination": dest, "duree_jours": duree})
print(pd.DataFrame(structured))

# ------------------------------------------------------------
# EXERCICE 8 : Charger train.csv (Titanic) depuis URL
# ------------------------------------------------------------
print("\n=== EXERCICE 8 ===")
url_titanic = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df_titanic = pd.read_csv(url_titanic)
print("Aperçu du dataset Titanic (5 premières lignes) :")
print(df_titanic.head())

# ------------------------------------------------------------
# EXERCICE 9 : Créer un DataFrame et exporter en Excel + JSON
# ------------------------------------------------------------
print("\n=== EXERCICE 9 ===")
data = {"Nom": ["Alice", "Bob", "Charlie"], "Âge": [25, 30, 35], "Ville": ["Paris", "Lyon", "Marseille"]}
df_export = pd.DataFrame(data)
df_export.to_excel("sortie_exercice9.xlsx", index=False)
df_export.to_json("sortie_exercice9.json", orient="records", indent=4)
print("Fichiers créés : sortie_exercice9.xlsx et sortie_exercice9.json")

# ------------------------------------------------------------
# EXERCICE 10 : Lire un fichier JSON
# ------------------------------------------------------------
print("\n=== EXERCICE 10 ===")
json_posts = '''
[
  {
    "userId": 1,
    "id": 1,
    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
    "body": "quia et suscipit\\nsuscipit recusandae consequuntur expedita et cum\\nreprehenderit molestiae ut ut quas totam\\nnostrum rerum est autem sunt rem eveniet architecto"
  },
  {
    "userId": 1,
    "id": 2,
    "title": "qui est esse",
    "body": "est rerum tempore vitae\\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\\nqui aperiam non debitis possimus qui neque nisi nulla"
  }
]
'''
df_posts = pd.read_json(StringIO(json_posts))
print("Données JSON (5 premières lignes) :")
print(df_posts.head())