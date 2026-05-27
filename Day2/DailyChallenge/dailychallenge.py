python
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.decomposition import PCA
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt

# Chargement du fichier (adapter le chemin)
df = pd.read_csv('datascience_salaries.csv', index_col=0)  # première colonne est un index

print("Forme du DataFrame :", df.shape)
print("\nPremières lignes :")
print(df.head())
print("\nInformations :")
print(df.info())

# Initialiser le scaler Min-Max
scaler_mm = MinMaxScaler()

# Appliquer sur la colonne salary (attention : il faut un tableau 2D)
df['salary_normalized'] = scaler_mm.fit_transform(df[['salary']])

# Vérification
print("Salaire brut - min :", df['salary'].min(), "max :", df['salary'].max())
print("Salaire normalisé - min :", df['salary_normalized'].min(), "max :", df['salary_normalized'].max())

# Sélection des colonnes catégorielles (on exclut salary et salary_normalized)
categorical_cols = ['job_title', 'job_type', 'experience_level', 'location', 'salary_currency']

# One-hot encoding
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
encoded_array = encoder.fit_transform(df[categorical_cols])

# Récupérer les noms des nouvelles colonnes
encoded_columns = encoder.get_feature_names_out(categorical_cols)

# Créer un DataFrame avec les variables encodées
df_encoded = pd.DataFrame(encoded_array, columns=encoded_columns, index=df.index)

# Ajouter la colonne salary_normalized (ou salary) pour la PCA
# Ici on utilise salary_normalized pour rester cohérent avec l'échelle
df_for_pca = pd.concat([df_encoded, df[['salary_normalized']]], axis=1)

print("Nombre de colonnes après encodage :", df_for_pca.shape[1])

# Standardisation préalable (recommandée pour la PCA)
scaler_std = StandardScaler()
data_scaled = scaler_std.fit_transform(df_for_pca)

# PCA avec 2 composantes
pca = PCA(n_components=2)
pca_result = pca.fit_transform(data_scaled)

# Ajouter les deux composantes au DataFrame original
df['PC1'] = pca_result[:, 0]
df['PC2'] = pca_result[:, 1]

# Afficher la variance expliquée
print("Variance expliquée par chaque composante :", pca.explained_variance_ratio_)
print("Variance totale expliquée :", sum(pca.explained_variance_ratio_))

# Grouper par experience_level
grouped = df.groupby('experience_level')['salary'].agg(['mean', 'median']).round(2)

# Renommer les colonnes pour plus de clarté
grouped.columns = ['salaire_moyen', 'salaire_median']

# Afficher le résultat
print(grouped)

plt.figure(figsize=(8,6))
colors = {'Entry': 'blue', 'Mid': 'green', 'Senior': 'orange', 'Executive': 'red'}
for level, color in colors.items():
    subset = df[df['experience_level'] == level]
    plt.scatter(subset['PC1'], subset['PC2'], c=color, label=level, alpha=0.5)
plt.xlabel('Première composante principale')
plt.ylabel('Deuxième composante principale')
plt.title('Projection PCA des données salariales (colorée par niveau d’expérience)')
plt.legend()
plt.show()
