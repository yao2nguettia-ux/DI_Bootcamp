# Import des bibliothèques nécessaires
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------------------------------------
# Exercice 1 : Comprendre la visualisation des données
# ------------------------------------------------------------
# 1. Importance : facilite l'identification des tendances, valeurs aberrantes,
#    aide à la prise de décision, rend les données accessibles.
# 2. Utilité du graphique linéaire : montrer l'évolution d'une variable dans le temps
#    (séries temporelles) ou une tendance continue.

# ------------------------------------------------------------
# Exercice 2 : Graphique linéaire pour la variation de température
# ------------------------------------------------------------
jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
temperatures = [72, 74, 76, 80, 82, 78, 75]

plt.figure(figsize=(8, 5))
plt.plot(jours, temperatures, marker='o', linestyle='-', color='orange', linewidth=2)
plt.xlabel('Jour')
plt.ylabel('Température (°F)')
plt.title('Variation de température sur une semaine')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

# ------------------------------------------------------------
# Exercice 3 : Graphique à barres pour les ventes mensuelles
# ------------------------------------------------------------
mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai']
ventes = [5000, 5500, 6200, 7000, 7500]

plt.figure(figsize=(8, 5))
plt.bar(mois, ventes, color='teal', edgecolor='black')
plt.xlabel('Mois')
plt.ylabel('Montant des ventes ($)')
plt.title('Ventes mensuelles du magasin')
plt.show()

# ------------------------------------------------------------
# Exercice 4 : Visualisation de la distribution des CGPA
# (utilisation du dataset Student Mental health.csv)
# ------------------------------------------------------------
# Chargement du dataset
df = pd.read_csv('Student Mental health.csv')

# Nettoyage : supprimer les espaces dans les noms de colonnes
df.columns = df.columns.str.strip()

# La colonne CGPA est catégorielle : "3.00 - 3.49", "3.50 - 4.00", etc.
# Pour un histogramme, on peut convertir en valeur numérique (ex: moyenne de l'intervalle)
def cgpa_to_numeric(cgpa_str):
    if pd.isna(cgpa_str):
        return np.nan
    cgpa_str = cgpa_str.strip()
    if ' - ' in cgpa_str:
        parts = cgpa_str.split(' - ')
        try:
            low = float(parts[0])
            high = float(parts[1])
            return (low + high) / 2
        except:
            return np.nan
    return np.nan

df['CGPA_num'] = df['What is your CGPA?'].apply(cgpa_to_numeric)

# Supprimer les valeurs manquantes
df_cgpa = df.dropna(subset=['CGPA_num'])

# Histogramme avec Seaborn
plt.figure(figsize=(8, 5))
sns.histplot(df_cgpa['CGPA_num'], bins=10, color='skyblue', edgecolor='black')
plt.title('Distribution des moyennes cumulatives (CGPA)')
plt.xlabel('CGPA')
plt.ylabel('Fréquence')
plt.show()

# ------------------------------------------------------------
# Exercice 5 : Comparaison des niveaux d'anxiété selon le sexe
# ------------------------------------------------------------
# Colonnes : 'Choose your gender' et 'Do you have Anxiety?'
# Supprimer les lignes avec valeurs manquantes
df_anxiety = df.dropna(subset=['Choose your gender', 'Do you have Anxiety?'])

# Graphique à barres (countplot)
plt.figure(figsize=(8, 5))
sns.countplot(data=df_anxiety, x='Choose your gender', hue='Do you have Anxiety?',
              palette='Set2')
plt.title('Niveaux d\'anxiété par sexe')
plt.xlabel('Sexe')
plt.ylabel('Nombre d\'étudiants')
plt.legend(title='Anxiété')
plt.show()

# Pour avoir des proportions:
# proportions = pd.crosstab(df_anxiety['Choose your gender'], df_anxiety['Do you have Anxiety?'], normalize='index')
# proportions.plot(kind='bar', stacked=True, color=['lightgreen', 'salmon'])
# plt.title('Proportion d\'anxiété par sexe')
# plt.ylabel('Proportion')
# plt.show()

# ------------------------------------------------------------
# Exercice 6 : Relation entre l'âge et les crises de panique
# ------------------------------------------------------------
# Colonnes : 'Age' et 'Do you have Panic attack?'
# Convertir 'Age' en numérique (certaines lignes ont des valeurs vides)
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
df_panic = df.dropna(subset=['Age', 'Do you have Panic attack?'])

# Convertir les réponses en numérique : Yes -> 1, No -> 0
df_panic['Panic_num'] = df_panic['Do you have Panic attack?'].map({'Yes': 1, 'No': 0})

# Nuage de points avec jitter pour éviter la superposition
plt.figure(figsize=(8, 5))
sns.stripplot(data=df_panic, x='Age', y='Panic_num', jitter=True, alpha=0.6, color='coral')
plt.xlabel('Âge')
plt.ylabel('Crises de panique (1 = Oui, 0 = Non)')
plt.title('Relation entre l\'âge et les crises de panique')
plt.yticks([0, 1], ['Non', 'Oui'])
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.show()