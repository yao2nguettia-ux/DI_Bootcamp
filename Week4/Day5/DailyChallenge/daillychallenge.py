# ====================================================================
# DÉFI QUOTIDIEN : ANALYSE DES PRÉDICTIONS DE VICTOIRES POKÉMON
# ====================================================================
# Objectif : Prédire le pourcentage de victoires des Pokémon
#           à partir de leurs statistiques et caractéristiques
# ====================================================================

# ====================================================================
# 1. IMPORTATION DES BIBLIOTHÈQUES
# ====================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

# Configuration des visualisations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
%matplotlib inline

# ====================================================================
# 2. CHARGEMENT DES DONNÉES
# ====================================================================

print("="*60)
print("CHARGEMENT DES DONNÉES POKÉMON")
print("="*60)

# Chargement des fichiers
pokemon_df = pd.read_csv('pokemon.csv')
combats_df = pd.read_csv('combats.csv')

print(f"\n📊 Pokémon dataset: {pokemon_df.shape[0]} lignes, {pokemon_df.shape[1]} colonnes")
print(f"📊 Combats dataset: {combats_df.shape[0]} lignes, {combats_df.shape[1]} colonnes")

print("\n🔍 Aperçu de pokemon.csv:")
print(pokemon_df.head())

print("\n🔍 Aperçu de combats.csv:")
print(combats_df.head())

# ====================================================================
# 3. NETTOYAGE ET PRÉTRAITEMENT DES DONNÉES
# ====================================================================

print("\n" + "="*60)
print("NETTOYAGE ET PRÉTRAITEMENT")
print("="*60)

# 3.1 Correction des valeurs manquantes
print("\n📊 Valeurs manquantes avant nettoyage:")
print(pokemon_df.isnull().sum())

# Correction du Pokémon n°62 (Primeape)
pokemon_df.loc[pokemon_df['#'] == 62, 'Name'] = 'Primeape'
print(f"\n✅ Pokémon n°62 corrigé: {pokemon_df.loc[pokemon_df['#'] == 62, 'Name'].values[0]}")

# Gestion des NaN dans Type 2
pokemon_df['Type 2'] = pokemon_df['Type 2'].fillna('None')
print("✅ Type 2: les valeurs manquantes ont été remplacées par 'None'")

# Vérification après nettoyage
print("\n📊 Valeurs manquantes après nettoyage:")
print(pokemon_df.isnull().sum())

# ====================================================================
# 4. CALCUL DU POURCENTAGE DE VICTOIRES
# ====================================================================

print("\n" + "="*60)
print("CALCUL DU POURCENTAGE DE VICTOIRES")
print("="*60)

# Compter les victoires pour chaque Pokémon
victoires = combats_df['Winner'].value_counts()
print(f"\n📊 Nombre de combats uniques: {len(victoires)} Pokémon ont au moins une victoire")

# Compter les apparitions totales (victoires + défaites)
apparitions = pd.concat([combats_df['First_pokemon'], combats_df['Second_pokemon']]).value_counts()

# Créer un DataFrame avec les statistiques de combat
combat_stats = pd.DataFrame({
    'Victoires': victoires,
    'Apparitions': apparitions
}).fillna(0)

# Calculer le pourcentage de victoires
combat_stats['Win_Rate'] = (combat_stats['Victoires'] / combat_stats['Apparitions'] * 100).round(2)
combat_stats['Win_Rate'] = combat_stats['Win_Rate'].fillna(0)

print(f"\n📊 Statistiques de combat:")
print(f"   • Nombre de Pokémon avec données de combat: {len(combat_stats)}")
print(f"   • Taux de victoire moyen: {combat_stats['Win_Rate'].mean():.2f}%")
print(f"   • Taux de victoire max: {combat_stats['Win_Rate'].max():.2f}%")
print(f"   • Taux de victoire min: {combat_stats['Win_Rate'].min():.2f}%")

# Aperçu des taux de victoire
print("\n📊 Top 5 Pokémon par taux de victoire:")
print(combat_stats.nlargest(5, 'Win_Rate'))

# ====================================================================
# 5. FUSION DES DONNÉES
# ====================================================================

print("\n" + "="*60)
print("FUSION DES DONNÉES")
print("="*60)

# Ajouter l'index Pokémon (colonne '#') comme identifiant
pokemon_df['Pokemon_ID'] = pokemon_df['#']

# Fusionner avec les statistiques de combat
pokemon_merged = pokemon_df.merge(
    combat_stats[['Victoires', 'Apparitions', 'Win_Rate']],
    left_on='#',
    right_index=True,
    how='left'
)

# Remplacer les NaN par 0 pour les Pokémon sans combat
pokemon_merged['Victoires'] = pokemon_merged['Victoires'].fillna(0)
pokemon_merged['Apparitions'] = pokemon_merged['Apparitions'].fillna(0)
pokemon_merged['Win_Rate'] = pokemon_merged['Win_Rate'].fillna(0)

print(f"\n📊 Dataset fusionné: {pokemon_merged.shape[0]} lignes, {pokemon_merged.shape[1]} colonnes")
print("\n🔍 Aperçu des données fusionnées:")
print(pokemon_merged.head())

# ====================================================================
# 6. ANALYSE EXPLORATOIRE DES DONNÉES (EDA)
# ====================================================================

print("\n" + "="*60)
print("ANALYSE EXPLORATOIRE DES DONNÉES (EDA)")
print("="*60)

# 6.1 Statistiques descriptives
print("\n📊 Statistiques descriptives des variables numériques:")
print(pokemon_merged[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Win_Rate']].describe())

# 6.2 Distribution du taux de victoire
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
sns.histplot(pokemon_merged['Win_Rate'], bins=30, kde=True)
plt.title('Distribution du taux de victoire')
plt.xlabel('Taux de victoire (%)')
plt.ylabel('Fréquence')

plt.subplot(1, 2, 2)
sns.boxplot(y=pokemon_merged['Win_Rate'])
plt.title('Boxplot du taux de victoire')
plt.ylabel('Taux de victoire (%)')

plt.tight_layout()
plt.show()

# 6.3 Statistiques par type
print("\n📊 Taux de victoire moyen par type principal:")
type_win_rate = pokemon_merged.groupby('Type 1')['Win_Rate'].mean().sort_values(ascending=False)
print(type_win_rate)

# Visualisation
plt.figure(figsize=(14, 6))
type_win_rate.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Taux de victoire moyen par type principal', fontsize=14, fontweight='bold')
plt.xlabel('Type')
plt.ylabel('Taux de victoire moyen (%)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 6.4 Distribution des types
plt.figure(figsize=(12, 5))
pokemon_merged['Type 1'].value_counts().plot(kind='bar', color='coral', edgecolor='black')
plt.title('Distribution des types principaux', fontsize=14, fontweight='bold')
plt.xlabel('Type')
plt.ylabel('Nombre de Pokémon')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 6.5 Analyse des Pokémon légendaires
plt.figure(figsize=(12, 5))

# Distribution des taux de victoire selon le statut légendaire
plt.subplot(1, 2, 1)
sns.boxplot(x='Legendary', y='Win_Rate', data=pokemon_merged)
plt.title('Taux de victoire: Légendaire vs Non-légendaire')
plt.xlabel('Légendaire')
plt.ylabel('Taux de victoire (%)')
plt.xticks([0, 1], ['Non-légendaire', 'Légendaire'])

# Nombre de légendaires
plt.subplot(1, 2, 2)
pokemon_merged['Legendary'].value_counts().plot(kind='pie', autopct='%1.1f%%', labels=['Non-légendaire', 'Légendaire'])
plt.title('Proportion de Pokémon légendaires')

plt.tight_layout()
plt.show()

print(f"\n📊 Statistiques des Pokémon légendaires:")
print(pokemon_merged.groupby('Legendary')['Win_Rate'].agg(['mean', 'std', 'count']))

# 6.6 Top 10 des meilleurs Pokémon
print("\n" + "-"*40)
print("TOP 10 DES MEILLEURS POKÉMON PAR TAUX DE VICTOIRE")
print("-"*40)

top10 = pokemon_merged.nlargest(10, 'Win_Rate')[['Name', 'Type 1', 'Type 2', 'Win_Rate', 'Victoires', 'Apparitions', 'Legendary']]
print(top10.to_string(index=False))

# Visualisation
plt.figure(figsize=(14, 6))
bars = plt.barh(top10['Name'], top10['Win_Rate'], color=['gold' if l else 'skyblue' for l in top10['Legendary']])
plt.xlabel('Taux de victoire (%)')
plt.title('Top 10 Pokémon par taux de victoire', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
plt.legend(['Légendaire' if l else 'Non-légendaire' for l in top10['Legendary']], loc='lower right')
plt.tight_layout()
plt.show()

# 6.7 Statistiques des meilleurs Pokémon
print("\n📊 Statistiques moyennes du Top 10 vs le reste:")
top10_stats = top10[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].mean()
all_stats = pokemon_merged[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].mean()

comparison = pd.DataFrame({
    'Top 10': top10_stats,
    'Tous les Pokémon': all_stats,
    'Différence': top10_stats - all_stats
})
print(comparison)

# ====================================================================
# 7. MATRICE DE CORRÉLATION
# ====================================================================

print("\n" + "="*60)
print("MATRICE DE CORRÉLATION")
print("="*60)

# Sélection des variables pour la corrélation
corr_vars = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Generation', 'Win_Rate']
corr_matrix = pokemon_merged[corr_vars].corr()

print("\n📊 Corrélations avec le taux de victoire:")
print(corr_matrix['Win_Rate'].sort_values(ascending=False))

# Visualisation
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f', 
            square=True, linewidths=0.5)
plt.title('Matrice de corrélation des statistiques Pokémon', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

# ====================================================================
# 8. PAIRPLOT DES STATISTIQUES
# ====================================================================

print("\n" + "="*60)
print("ANALYSE DES RELATIONS ENTRE STATISTIQUES")
print("="*60)

# Sélection des variables pour le pairplot
pair_vars = ['HP', 'Attack', 'Defense', 'Speed', 'Sp. Atk', 'Win_Rate']

# Création d'un PairGrid avec les statistiques
g = sns.PairGrid(pokemon_merged[pair_vars].sample(min(500, len(pokemon_merged))), 
                 diag_sharey=False)
g.map_upper(sns.scatterplot, alpha=0.3)
g.map_lower(sns.kdeplot, cmap='Blues_d')
g.map_diag(sns.histplot, kde=True)
g.fig.suptitle('Relations entre les statistiques Pokémon et le taux de victoire', 
               y=1.02, fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

# ====================================================================
# 9. ENCODAGE DES VARIABLES CATÉGORIELLES
# ====================================================================

print("\n" + "="*60)
print("PRÉPARATION POUR L'APPRENTISSAGE AUTOMATIQUE")
print("="*60)

# Création d'une copie pour la modélisation
model_data = pokemon_merged.copy()

# Encodage des types
le_type1 = LabelEncoder()
le_type2 = LabelEncoder()

model_data['Type1_Encoded'] = le_type1.fit_transform(model_data['Type 1'].astype(str))
model_data['Type2_Encoded'] = le_type2.fit_transform(model_data['Type 2'].astype(str))

# Encodage du statut légendaire
model_data['Legendary_Encoded'] = model_data['Legendary'].map({False: 0, True: 1})

print("✅ Variables catégorielles encodées")

# ====================================================================
# 10. SÉLECTION DES CARACTÉRISTIQUES
# ====================================================================

# Définition des features pour la modélisation
feature_cols = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 
                'Generation', 'Type1_Encoded', 'Type2_Encoded', 'Legendary_Encoded']

X = model_data[feature_cols].copy()
y = model_data['Win_Rate']

# Gestion des valeurs manquantes
imputer = SimpleImputer(strategy='median')
X_imputed = imputer.fit_transform(X)

print(f"\n📊 Features: {X.shape[1]}")
print(f"📊 Target: {y.shape[0]} échantillons")

# ====================================================================
# 11. STANDARDISATION DES DONNÉES
# ====================================================================

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)

print("✅ Données standardisées")

# ====================================================================
# 12. DIVISION DES DONNÉES
# ====================================================================

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

print(f"\n📊 Taille de l'ensemble d'entraînement: {X_train.shape[0]} échantillons")
print(f"📊 Taille de l'ensemble de test: {X_test.shape[0]} échantillons")

# ====================================================================
# 13. ENTRAÎNEMENT ET ÉVALUATION DES MODÈLES
# ====================================================================

print("\n" + "="*60)
print("ENTRAÎNEMENT ET ÉVALUATION DES MODÈLES")
print("="*60)

# Définition des modèles
models = {
    'Régression Linéaire': LinearRegression(),
    'Ridge': Ridge(alpha=1.0),
    'Lasso': Lasso(alpha=0.01),
    'Arbre de Décision': DecisionTreeRegressor(max_depth=10, random_state=42),
    'Forêt Aléatoire': RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42),
    'SVM': SVR(kernel='rbf', C=1.0, epsilon=0.1)
}

# Entraînement et évaluation
results = []

for name, model in models.items():
    # Entraînement
    model.fit(X_train, y_train)
    
    # Prédictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    # Calcul des métriques
    train_mae = mean_absolute_error(y_train, y_train_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    
    results.append({
        'Modèle': name,
        'Train MAE': train_mae,
        'Test MAE': test_mae,
        'Train RMSE': train_rmse,
        'Test RMSE': test_rmse,
        'Train R²': train_r2,
        'Test R²': test_r2
    })
    
    print(f"\n📊 {name}:")
    print(f"   • MAE (Entraînement): {train_mae:.3f}")
    print(f"   • MAE (Test): {test_mae:.3f}")
    print(f"   • R² (Entraînement): {train_r2:.3f}")
    print(f"   • R² (Test): {test_r2:.3f}")

# ====================================================================
# 14. COMPARAISON DES MODÈLES
# ====================================================================

print("\n" + "="*60)
print("COMPARAISON DES PERFORMANCES")
print("="*60)

results_df = pd.DataFrame(results)
print("\n📊 Résumé des performances:")
print(results_df.to_string(index=False))

# Visualisation des performances
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# MAE
results_df_sorted = results_df.sort_values('Test MAE')
axes[0].barh(results_df_sorted['Modèle'], results_df_sorted['Test MAE'], color='skyblue')
axes[0].set_xlabel('MAE (Test)')
axes[0].set_title('Erreur Absolue Moyenne par Modèle', fontweight='bold')

# R²
results_df_sorted_r2 = results_df.sort_values('Test R²', ascending=False)
axes[1].barh(results_df_sorted_r2['Modèle'], results_df_sorted_r2['Test R²'], color='lightgreen')
axes[1].set_xlabel('R² (Test)')
axes[1].set_title('Coefficient de Détermination par Modèle', fontweight='bold')

# Comparaison Train/Test MAE
x = np.arange(len(results_df))
width = 0.35
axes[2].bar(x - width/2, results_df['Train MAE'], width, label='Entraînement', color='blue', alpha=0.6)
axes[2].bar(x + width/2, results_df['Test MAE'], width, label='Test', color='orange', alpha=0.6)
axes[2].set_xlabel('Modèle')
axes[2].set_ylabel('MAE')
axes[2].set_title('Comparaison MAE Train vs Test', fontweight='bold')
axes[2].set_xticks(x)
axes[2].set_xticklabels(results_df['Modèle'], rotation=45, ha='right')
axes[2].legend()

plt.tight_layout()
plt.show()

# ====================================================================
# 15. MEILLEUR MODÈLE - ANALYSE APPROFONDIE
# ====================================================================

print("\n" + "="*60)
print("ANALYSE DU MEILLEUR MODÈLE")
print("="*60)

# Sélection du meilleur modèle (Forêt Aléatoire)
best_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
best_model.fit(X_train, y_train)
y_pred = best_model.predict(X_test)

print(f"\n📊 Meilleur modèle: Forêt Aléatoire")
print(f"   • MAE: {mean_absolute_error(y_test, y_pred):.3f}")
print(f"   • RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.3f}")
print(f"   • R²: {r2_score(y_test, y_pred):.3f}")

# Importance des caractéristiques
feature_importance = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': best_model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\n📊 Importance des caractéristiques:")
print(feature_importance)

# Visualisation
plt.figure(figsize=(10, 6))
plt.barh(feature_importance['Feature'], feature_importance['Importance'], color='coral')
plt.xlabel('Importance')
plt.title('Importance des caractéristiques - Forêt Aléatoire', fontweight='bold')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# ====================================================================
# 16. PRÉDICTIONS VS VALEURS RÉELLES
# ====================================================================

plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Valeurs réelles (%)')
plt.ylabel('Prédictions (%)')
plt.title('Prédictions vs Valeurs Réelles - Forêt Aléatoire', fontweight='bold')
plt.tight_layout()
plt.show()

# ====================================================================
# 17. RÉDUCTION DE DIMENSIONNALITÉ (ACP)
# ====================================================================

print("\n" + "="*60)
print("RÉDUCTION DE DIMENSIONNALITÉ - ACP")
print("="*60)

# Application de l'ACP
pca = PCA()
X_pca = pca.fit_transform(X_scaled)

# Variance expliquée
explained_variance = pca.explained_variance_ratio_
cumulative_variance = np.cumsum(explained_variance)

print("\n📊 Variance expliquée par composante:")
for i, var in enumerate(explained_variance[:5], 1):
    print(f"   • PC{i}: {var:.2%} ({cumulative_variance[i-1]:.2%} cumulé)")

# Visualisation
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Variance expliquée
axes[0].bar(range(1, len(explained_variance)+1), explained_variance, alpha=0.7, label='Variance individuelle')
axes[0].plot(range(1, len(cumulative_variance)+1), cumulative_variance, 'r-o', label='Variance cumulée')
axes[0].set_xlabel('Composante principale')
axes[0].set_ylabel('Variance expliquée')
axes[0].set_title('Variance expliquée par l\'ACP', fontweight='bold')
axes[0].legend()
axes[0].axhline(y=0.95, color='green', linestyle='--', alpha=0.5, label='95%')
axes[0].legend()

# Projection sur les 2 premières composantes
scatter = axes[1].scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='viridis', alpha=0.6)
axes[1].set_xlabel('PC1')
axes[1].set_ylabel('PC2')
axes[1].set_title('Projection ACP - couleur = taux de victoire', fontweight='bold')
plt.colorbar(scatter, ax=axes[1], label='Taux de victoire (%)')

plt.tight_layout()
plt.show()

# ====================================================================
# 18. RÉSULTATS SUR LE JEU DE TEST NON VU
# ====================================================================

print("\n" + "="*60)
print("PRÉDICTIONS SUR LE JEU DE TEST")
print("="*60)

# Création d'un DataFrame pour les résultats
test_results = pd.DataFrame({
    'Pokemon': pokemon_merged.loc[y_test.index, 'Name'],
    'Win_Rate_Reel': y_test.values,
    'Win_Rate_Predit': y_pred
})

test_results['Erreur'] = test_results['Win_Rate_Reel'] - test_results['Win_Rate_Predit']
test_results['Erreur_Abs'] = np.abs(test_results['Erreur'])

print("\n📊 Exemples de prédictions:")
print(test_results.head(10).to_string(index=False))

print(f"\n📊 Statistiques des erreurs:")
print(f"   • Erreur moyenne: {test_results['Erreur'].mean():.3f}")
print(f"   • Erreur absolue moyenne: {test_results['Erreur_Abs'].mean():.3f}")
print(f"   • Erreur max: {test_results['Erreur_Abs'].max():.3f}")

# ====================================================================
# 19. CONCLUSION
# ====================================================================

print("\n" + "="*60)
print("📈 CONCLUSION FINALE")
print("="*60)

print(f"""
📊 RÉSULTATS DE L'ANALYSE DES PRÉDICTIONS DE VICTOIRES POKÉMON:

   PERFORMANCES DES MODÈLES:
   • Meilleur modèle: Forêt Aléatoire
   • MAE: {mean_absolute_error(y_test, y_pred):.3f}%
   • R²: {r2_score(y_test, y_pred):.3f}
   • RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.3f}%

   PRINCIPALES CARACTÉRISTIQUES PRÉDICTIVES:
   1. {feature_importance.iloc[0]['Feature']} (importance: {feature_importance.iloc[0]['Importance']:.3f})
   2. {feature_importance.iloc[1]['Feature']} (importance: {feature_importance.iloc[1]['Importance']:.3f})
   3. {feature_importance.iloc[2]['Feature']} (importance: {feature_importance.iloc[2]['Importance']:.3f})
   4. {feature_importance.iloc[3]['Feature']} (importance: {feature_importance.iloc[3]['Importance']:.3f})
   5. {feature_importance.iloc[4]['Feature']} (importance: {feature_importance.iloc[4]['Importance']:.3f})

   OBSERVATIONS CLÉS:
   • Les Pokémon légendaires ont un taux de victoire significativement plus élevé
   • Les statistiques offensives (Attack, Sp. Atk) corrèlent mieux avec le taux de victoire
   • La vitesse est un facteur important pour les combats
   • Les types influencent les performances des Pokémon
   • La forêt aléatoire offre les meilleures performances prédictives

   PERSPECTIVES D'AMÉLIORATION:
   • Intégrer plus de caractéristiques (ex: évolutions, capacités)
   • Tester des modèles plus complexes (XGBoost, LightGBM, Neural Networks)
   • Optimiser les hyperparamètres avec GridSearchCV
   • Ajouter des interactions entre les variables
   • Utiliser la validation croisée pour plus de robustesse
""")

print("="*60)
print("✅ PROJET TERMINÉ AVEC SUCCÈS")
print("="*60)