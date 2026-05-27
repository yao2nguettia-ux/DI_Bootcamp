# Importation des bibliothèques et chargement des données

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.impute import SimpleImputer

# Chargement du fichier
df = pd.read_csv('train.csv')

print("Forme initiale du DataFrame :", df.shape)
df.head()

# Exercice 1 – Détection et suppression des doublons

# Vérifier les doublons parfaits (toutes les colonnes)
duplicates_count = df.duplicated().sum()
print(f"Nombre de lignes strictement dupliquées : {duplicates_count}")

# Supprimer les doublons s'il y en a
df = df.drop_duplicates()

print("Forme après suppression des doublons :", df.shape)

# Résultat : Le jeu de données Titanic ne contient aucun doublon parfait. L’opération ne change rien.

# Exercice 2 – Gestion des valeurs manquantes
# Identifier les colonnes avec des NaN

missing = df.isnull().sum()
missing_percent = 100 * missing / len(df)
missing_df = pd.DataFrame({'missing_count': missing, 'missing_percent': missing_percent})
print(missing_df[missing_df['missing_count'] > 0].sort_values('missing_percent', ascending=False))

#Cabin : ~77% de NaN → colonne à supprimer

#Age : ~20% de NaN → imputation

#Embarked : 2 valeurs manquantes → imputation par le mode

# Application des stratégies

# Suppression de 'Cabin' (trop de manquants, peu d'info)
df.drop('Cabin', axis=1, inplace=True)

# Imputation de 'Embarked' par la valeur la plus fréquente (mode)
mode_embarked = df['Embarked'].mode()[0]
df['Embarked'].fillna(mode_embarked, inplace=True)

# Imputation de 'Age' par la médiane (robuste aux outliers)
median_age = df['Age'].median()
df['Age'].fillna(median_age, inplace=True)

# Vérification finale
print("Valeurs manquantes restantes :", df.isnull().sum().sum())
# Exercice 3 – Ingénierie des fonctionnalités
# Création de FamilySize et extraction du Title depuis le nom.
# Taille de la famille (passager lui-même + conjoints + enfants)
df['FamilySize'] = df['SibSp'] + df['Parch'] + 1

# Extraire le titre (Mr, Mrs, Miss, Master, etc.)
df['Title'] = df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)

# Regrouper les titres rares (occurrence < 10) dans une catégorie 'Rare'
title_counts = df['Title'].value_counts()
rare_titles = title_counts[title_counts < 10].index
df['Title'] = df['Title'].replace(rare_titles, 'Rare')

# Vérification
print(df['Title'].value_counts())

# Exercice 4 – Détection et traitement des outliers
# On traite les colonnes Age et Fare (et éventuellement FamilySize).

#Visualisation

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
sns.boxplot(data=df, y='Age', ax=axes[0])
axes[0].set_title('Age (avant traitement)')
sns.boxplot(data=df, y='Fare', ax=axes[1])
axes[1].set_title('Fare (avant traitement)')
plt.show()

#Traitement par la méthode IQR pour Fare

Q1 = df['Fare'].quantile(0.25)
Q3 = df['Fare'].quantile(0.75)
IQR = Q3 - Q1
upper_bound = Q3 + 1.5 * IQR

print(f"Borne supérieure (IQR) pour Fare : {upper_bound:.2f}")

# Plafonnement (capping) au 98e percentile (plus doux que IQR)
cap = df['Fare'].quantile(0.98)
df['Fare_capped'] = df['Fare'].clip(upper=cap)

# Comparaison
print("Avant plafonnement - max :", df['Fare'].max())
print("Après plafonnement - max :", df['Fare_capped'].max())

#Traitement de l’âge
#L’âge présente quelques valeurs élevées (80 ans). On peut soit les conserver, soit les plafonner.

# Option : plafonnement au 99e percentile
age_cap = df['Age'].quantile(0.99)
df['Age_capped'] = df['Age'].clip(upper=age_cap)

print(f"Age max avant : {df['Age'].max():.1f} -> après : {df['Age_capped'].max():.1f}")

# Exercice 5 – Standardisation et normalisation
#On va standardiser Age_capped et Fare_capped (distributions approximativement normales après transformation ?).
#FamilySize sera normalisée entre 0 et 1.

# Choix des colonnes
cols_standard = ['Age_capped', 'Fare_capped']
cols_minmax = ['FamilySize']

# Standardisation (moyenne=0, écart-type=1)
scaler_std = StandardScaler()
df[cols_standard] = scaler_std.fit_transform(df[cols_standard])

# Normalisation MinMax (entre 0 et 1)
scaler_mm = MinMaxScaler()
df[cols_minmax] = scaler_mm.fit_transform(df[cols_minmax])

# Vérification rapide
print(df[cols_standard].describe())
print(df[cols_minmax].describe())

# Exercice 6 – Encodage des caractéristiques
#Il reste les variables catégorielles : Sex, Embarked, Title.
#Sex : binaire → mapping 0/1
#Embarked : nominal → one-hot encoding
#Title : nominal → one-hot encoding
# Sexe : male=0, female=1
df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})

# One-hot pour Embarked
df = pd.get_dummies(df, columns=['Embarked'], prefix='Emb', drop_first=True)

# One-hot pour Title
title_dummies = pd.get_dummies(df['Title'], prefix='Title')
df = pd.concat([df, title_dummies], axis=1)
df.drop('Title', axis=1, inplace=True)

print("Colonnes finales après encodage :", df.columns.tolist())

# Exercice 7 – Transformation de l’âge en groupes d’âge
#On utilise la colonne Age originale (non standardisée) pour créer des catégories.
#Ici on travaille sur Age (après imputation mais avant plafonnement).
#On peut aussi utiliser Age_capped si on préfère.

# Définition des bornes et des libellés
bins = [0, 12, 18, 60, 100]
labels = ['Enfant', 'Adolescent', 'Adulte', 'Senior']

# Création de la colonne catégorielle
df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

# One-hot encoding
agegroup_dummies = pd.get_dummies(df['AgeGroup'], prefix='AgeGroup')
df = pd.concat([df, agegroup_dummies], axis=1)

# (Optionnel) suppression de la colonne AgeGroup si vous ne voulez que les dummies
# df.drop('AgeGroup', axis=1, inplace=True)

print(df.filter(like='AgeGroup').head())

# Vérification finale et sauvegarde

print("Forme finale du DataFrame :", df.shape)
print("\nAperçu des colonnes :")
print(df.columns.tolist())

# Sauvegarde du DataFrame nettoyé et transformé (optionnel)
# df.to_csv('titanic_cleaned.csv', index=False)