# %% [markdown]
# # Analyse complète des prix des téléphones mobiles
# 
# ## 1. Chargement et exploration des données

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Charger les données
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')  # on utilisera train pour l'analyse

print("Forme du dataset d'entraînement:", train.shape)
train.head()

# %%
# Informations sur les colonnes
train.info()

# %%
# Statistiques descriptives de base
train.describe()

# %%
# Distribution de la variable cible
train['price_range'].value_counts().sort_index()

# %% [markdown]
# ## 2. Nettoyage et prétraitement

# %%
# Vérifier les valeurs manquantes
train.isnull().sum()

# %%
# Toutes les colonnes sont numériques, pas de nettoyage nécessaire
# La variable cible est déjà numérique (0,1,2,3)

# %% [markdown]
# ## 3. Analyse statistique avec NumPy et SciPy

# %%
# Mesures de tendance centrale et de variabilité pour chaque caractéristique
features = ['battery_power', 'clock_speed', 'fc', 'int_memory', 'm_dep', 'mobile_wt', 
            'n_cores', 'pc', 'px_height', 'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time']

stats_df = pd.DataFrame(index=features)
stats_df['mean'] = train[features].mean()
stats_df['median'] = train[features].median()
stats_df['mode'] = train[features].mode().iloc[0]
stats_df['range'] = train[features].max() - train[features].min()
stats_df['variance'] = train[features].var()
stats_df['std'] = train[features].std()
stats_df['skew'] = train[features].skew()
stats_df['kurtosis'] = train[features].kurtosis()
stats_df.round(2)

# %%
# Test d'hypothèse : différence de RAM entre les gammes de prix
price_groups = [train[train['price_range'] == i]['ram'].values for i in range(4)]
f_stat, p_value = stats.f_oneway(*price_groups)
print(f"ANOVA sur RAM par gamme de prix: F={f_stat:.2f}, p={p_value:.2e}")
if p_value < 0.05:
    print("Différence significative entre les gammes de prix pour la RAM")

# %%
# Corrélation entre caractéristiques et prix (cible)
correlations = train[features + ['price_range']].corr()['price_range'].drop('price_range')
correlations.sort_values(ascending=False)

# %%
# Test de corrélation pour les caractéristiques les plus corrélées
for feat in ['ram', 'battery_power', 'px_height', 'px_width']:
    r, p = stats.pearsonr(train[feat], train['price_range'])
    print(f"{feat}: r={r:.3f}, p={p:.2e}")

# %% [markdown]
# ## 4. Visualisation des données avec Matplotlib

# %%
# Histogrammes des principales caractéristiques par gamme de prix
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
features_plot = ['ram', 'battery_power', 'px_height', 'px_width']
for ax, feat in zip(axes.flatten(), features_plot):
    for price in range(4):
        subset = train[train['price_range'] == price][feat]
        ax.hist(subset, bins=20, alpha=0.5, label=f'Prix {price}')
    ax.set_title(f'Distribution de {feat}')
    ax.legend()
plt.tight_layout()
plt.show()

# %%
# Boxplots pour visualiser la répartition des caractéristiques par prix
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
for ax, feat in zip(axes.flatten(), features_plot):
    data = [train[train['price_range'] == i][feat] for i in range(4)]
    ax.boxplot(data, labels=['0', '1', '2', '3'])
    ax.set_title(f'{feat} par gamme de prix')
    ax.set_xlabel('Gamme de prix')
    ax.set_ylabel(feat)
plt.tight_layout()
plt.show()

# %%
# Nuage de points : RAM vs prix
plt.figure(figsize=(8,6))
plt.scatter(train['ram'], train['price_range'], alpha=0.5, c='blue')
plt.xlabel('RAM')
plt.ylabel('Gamme de prix')
plt.title('Relation entre RAM et prix')
plt.grid(True)
plt.show()

# %%
# Matrice de corrélation avec heatmap
plt.figure(figsize=(12,10))
corr_matrix = train[features + ['price_range']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f')
plt.title('Matrice de corrélation')
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 5. Synthèse des insights et conclusion

# %%
# Synthèse
print("Insights principaux:")
print("- RAM est la caractéristique la plus corrélée avec le prix (r ≈ {:.2f})".format(correlations['ram']))
print("- La batterie, la résolution (px_height, px_width) ont aussi une corrélation modérée.")
print("- Les tests ANOVA confirment que la RAM diffère significativement entre gammes de prix.")
print("- Les boxplots montrent une augmentation claire de RAM, batterie, résolution avec le prix.")
print("- Les histogrammes par gamme révèlent des distributions décalées pour ces caractéristiques.")
print("\nConclusion: Les principaux déterminants du prix des téléphones sont la RAM, la capacité de la batterie,")
print("la résolution de l'écran (px_height, px_width) et, dans une moindre mesure, le stockage interne.")