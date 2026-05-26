import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Génération des données simulées (2015-2024)
np.random.seed(42)
years = np.arange(2015, 2025)
months = np.arange(1, 13)

data = []
for year in years:
    for month in months:
        # Saisonnalité : pic en juillet-août
        seasonal = 1 + 0.5 * np.sin((month - 6) * np.pi / 6)
        # Tendance : croissance annuelle d'environ 6% à partir de 2020 (mise en place analyse)
        if year < 2020:
            trend = 1 + 0.02 * (year - 2015)   # croissance lente avant analyse
        else:
            trend = 1 + 0.06 * (year - 2015)   # accélération après analyse
        sales = 100 * seasonal * trend + np.random.normal(0, 5)
        price = 4.5 - 0.2 * (year - 2015) + np.random.normal(0, 0.3)
        demand = 80 * seasonal * trend + np.random.normal(0, 8)
        data.append([year, month, sales, price, demand])

df = pd.DataFrame(data, columns=['Year', 'Month', 'Sales_tons', 'Price_dollar_per_kg', 'Demand_units'])

# 2. Ajout de colonnes temporelles
df['Date'] = pd.to_datetime(df[['Year', 'Month']].assign(day=1))
df.set_index('Date', inplace=True)

print("=== Aperçu des données ===")
print(df.head())

# 3. Analyse de tendance : ventes annuelles moyennes
annual_sales = df.groupby('Year')['Sales_tons'].mean().reset_index()
print("\n=== Ventes annuelles moyennes (tonnes) ===")
print(annual_sales)

# 4. Mise en évidence de l'impact de l'analyse de données (rupture en 2020)
annual_sales['Growth'] = annual_sales['Sales_tons'].pct_change() * 100
print("\n=== Croissance annuelle (%) ===")
print(annual_sales)

# 5. Visualisation : avant / après 2020
plt.figure(figsize=(10,5))
plt.plot(annual_sales['Year'], annual_sales['Sales_tons'], marker='o', linestyle='-')
plt.axvline(x=2019.5, color='red', linestyle='--', label='Déploiement analyse données (2020)')
plt.title('Évolution des ventes de myrtilles en Amérique du Nord')
plt.xlabel('Année')
plt.ylabel('Ventes moyennes (tonnes)')
plt.legend()
plt.grid(True)
plt.show()

# 6. Comparaison des périodes avant et après 2020
before = df[df['Year'] < 2020]['Sales_tons'].mean()
after = df[df['Year'] >= 2020]['Sales_tons'].mean()
print(f"\nVentes moyennes avant 2020 : {before:.1f} tonnes")
print(f"Ventes moyennes à partir de 2020 : {after:.1f} tonnes")
print(f"Augmentation : {((after - before)/before)*100:.1f}%")

# 7. Analyse de la relation prix / demande
correlation = df['Price_dollar_per_kg'].corr(df['Demand_units'])
print(f"\nCorrélation entre prix et demande : {correlation:.2f} (négative = logique économique)")

# 8. Simulation de décision : recommander une promotion
# Groupement par mois pour identifier la période de faible demande
monthly_demand = df.groupby('Month')['Demand_units'].mean()
low_demand_month = monthly_demand.idxmin()
print(f"\nMois avec la plus faible demande : {low_demand_month} → recommander une promotion")

# 9. Export du rapport synthétique
summary = pd.DataFrame({
    'Indicateur': ['Ventes moyennes avant 2020', 'Ventes moyennes après 2020', 'Croissance post-analyse', 'Mois promo recommandé'],
    'Valeur': [f"{before:.1f} t", f"{after:.1f} t", f"{((after-before)/before)*100:.1f}%", low_demand_month]
})
print("\n=== RAPPORT D'ANALYDE DONNÉES ===")
print(summary.to_string(index=False))

# Sauvegarde en CSV
df.to_csv('blueberry_analysis.csv')
print("\nFichier 'blueberry_analysis.csv' créé.")