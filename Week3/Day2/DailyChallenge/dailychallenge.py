import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 1. Chargement et nettoyage
df = pd.read_csv('global_power_plant_database.csv', low_memory=False)

# Suppression des lignes sans capacité
df = df.dropna(subset=['capacity_mw'])

# Conversion des colonnes utiles
df['commissioning_year'] = pd.to_numeric(df['commissioning_year'], errors='coerce')
gen_cols = ['generation_gwh_2013', 'generation_gwh_2014', 'generation_gwh_2015',
            'generation_gwh_2016', 'generation_gwh_2017', 'generation_gwh_2018',
            'generation_gwh_2019']
for col in gen_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Création de la génération moyenne
gen_data = df[gen_cols].values
df['avg_generation_gwh'] = np.nanmean(gen_data, axis=1)

# Suppression des coordonnées manquantes
df = df.dropna(subset=['latitude', 'longitude'])

# Filtrage des types de combustibles les plus fréquents (≥100 centrales)
fuel_counts = df['primary_fuel'].value_counts()
top_fuels = fuel_counts[fuel_counts >= 100].index
df = df[df['primary_fuel'].isin(top_fuels)].copy()

# 2. Analyse exploratoire
print(df[['capacity_mw', 'avg_generation_gwh']].describe())
print(df['primary_fuel'].value_counts())

# 3. Statistiques par combustible
fuels = df['primary_fuel'].unique()
for fuel in fuels:
    caps = df[df['primary_fuel'] == fuel]['capacity_mw'].values
    print(f"{fuel}: moyenne={np.mean(caps):.1f} MW, médiane={np.median(caps):.1f}")

# Test t entre Hydro et Gas
hydro = df[df['primary_fuel'] == 'Hydro']['capacity_mw'].values
gas = df[df['primary_fuel'] == 'Gas']['capacity_mw'].values
t_stat, p = stats.ttest_ind(hydro, gas, equal_var=False)
print(f"Hydro vs Gas: p-value={p:.3e}")

# 4. Série temporelle
df_time = df.dropna(subset=['commissioning_year'])
df_time = df_time[(df_time['commissioning_year'] >= 1900) & (df_time['commissioning_year'] <= 2020)]

year_fuel = pd.crosstab(df_time['commissioning_year'], df_time['primary_fuel'])
year_fuel_pct = year_fuel.div(year_fuel.sum(axis=1), axis=0) * 100

plt.figure(figsize=(12,6))
for fuel in ['Coal', 'Gas', 'Hydro', 'Solar', 'Wind', 'Oil']:
    if fuel in year_fuel_pct:
        plt.plot(year_fuel_pct.index, year_fuel_pct[fuel], label=fuel)
plt.xlabel('Année')
plt.ylabel('Proportion (%)')
plt.title('Évolution du type de combustible des nouvelles centrales')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# Moyenne mobile de la capacité
yearly_mean = df_time.groupby('commissioning_year')['capacity_mw'].mean()
window = 10
weights = np.ones(window)/window
smooth = np.convolve(yearly_mean.values, weights, mode='valid')
plt.figure(figsize=(10,5))
plt.plot(yearly_mean.index, yearly_mean.values, alpha=0.5)
plt.plot(yearly_mean.index[window-1:], smooth, 'r-', linewidth=2)
plt.xlabel('Année')
plt.ylabel('Capacité moyenne (MW)')
plt.title('Tendance de la capacité (moyenne mobile)')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# 5. Visualisations avancées
plt.figure(figsize=(12,6))
sns.boxplot(data=df, x='primary_fuel', y='capacity_mw')
plt.yscale('log')
plt.xticks(rotation=45)
plt.title('Capacité par combustible (échelle log)')
plt.tight_layout()
plt.show()

# Carte (échantillon pour éviter surcharge)
sample = df.sample(min(5000, len(df)))
plt.figure(figsize=(12,8))
plt.scatter(sample['longitude'], sample['latitude'], s=2, alpha=0.4)
plt.xlabel('Longitude'); plt.ylabel('Latitude')
plt.title('Localisation des centrales')
plt.tight_layout()
plt.show()

# 6. Opérations matricielles (ACP simple)
X = df[['capacity_mw', 'latitude', 'longitude']].dropna().values
X_norm = (X - X.mean(axis=0)) / X.std(axis=0)
cov = np.cov(X_norm, rowvar=False)
eigvals, eigvecs = np.linalg.eig(cov)
print("Valeurs propres de la matrice de covariance :", eigvals)

# 7. Intégration NumPy/Pandas/Matplotlib : filtrage avancé et ajustement polynomial
med_cap = np.median(df['capacity_mw'].values)
south = df['latitude'].values < 0
selected = df[(df['capacity_mw'].values > med_cap) & south]
print(f"Centrales sélectionnées (capacité > médiane, hémisphère sud) : {len(selected)}")

# Ajustement polynomial de la tendance de capacité moyenne
years = yearly_mean.index.values
caps = yearly_mean.values
coeffs = np.polyfit(years[~np.isnan(caps)], caps[~np.isnan(caps)], 2)
poly = np.poly1d(coeffs)
x_fit = np.linspace(years.min(), years.max(), 200)
plt.figure(figsize=(10,5))
plt.scatter(years, caps, alpha=0.5)
plt.plot(x_fit, poly(x_fit), 'r-', label='Tendance quadratique')
plt.xlabel('Année')
plt.ylabel('Capacité moyenne (MW)')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()