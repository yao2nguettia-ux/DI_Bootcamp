# 1. Import des bibliothèques
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import mplcursors

# Style Seaborn
sns.set_theme(style="whitegrid")

# 2. Chargement et nettoyage des données
print("Chargement des données...")
df = pd.read_excel("US Superstore data (1).xls", sheet_name="Orders")

# Conversion des dates
df["Order Date"] = pd.to_datetime(df["Order Date"])
# Création d'une colonne année
df["Year"] = df["Order Date"].dt.year

# Suppression des lignes sans ventes ou profit (non significatif)
df.dropna(subset=["Sales", "Profit", "Discount"], inplace=True)

print(f"Données chargées : {df.shape[0]} lignes, {df.shape[1]} colonnes")
print(f"Période : {df['Year'].min()} - {df['Year'].max()}")

# 3. Graphique linéaire interactif avec Matplotlib (tendance des ventes)
sales_by_year = df.groupby("Year")["Sales"].sum().reset_index()

fig1, ax = plt.subplots(figsize=(10, 6))
line, = ax.plot(sales_by_year["Year"], sales_by_year["Sales"], marker='o', linestyle='-', color='b')
ax.set_title("Tendance des ventes totales par année (interactif)", fontsize=14)
ax.set_xlabel("Année", fontsize=12)
ax.set_ylabel("Ventes totales (USD)", fontsize=12)
ax.grid(True, linestyle='--', alpha=0.7)

# Interactivité : affichage des valeurs au survol
cursor = mplcursors.cursor(line, hover=True)
cursor.connect("add", lambda sel: sel.annotation.set_text(
    f"Année : {sales_by_year['Year'][sel.index]}\nVentes : {sales_by_year['Sales'][sel.index]:,.0f} USD"
))
plt.tight_layout()
plt.show()

# 4. Carte interactive des ventes par État (USA) avec Plotly
# Dictionnaire de correspondance nom d'état -> code postal
state_abbr = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
    'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY',
    'District of Columbia': 'DC'
}
sales_by_state = df.groupby("State")["Sales"].sum().reset_index()
sales_by_state["code"] = sales_by_state["State"].map(state_abbr)
sales_by_state.dropna(subset=["code"], inplace=True)

fig_map = px.choropleth(
    sales_by_state,
    locations="code",
    color="Sales",
    locationmode="USA-states",
    scope="usa",
    color_continuous_scale="Viridis",
    title="Ventes totales par État (USA)",
    labels={"Sales": "Ventes (USD)"}
)
fig_map.show()

# 5. Graphique à barres Seaborn : top 10 produits les plus vendus (quantité)
top_products = df.groupby("Product Name")["Quantity"].sum().sort_values(ascending=False).head(10).reset_index()

plt.figure(figsize=(12, 6))
sns.barplot(data=top_products, y="Product Name", x="Quantity", palette="rocket", orient='h')
plt.title("Top 10 des produits les plus vendus (quantité totale)", fontsize=14)
plt.xlabel("Quantité totale vendue", fontsize=12)
plt.ylabel("Nom du produit", fontsize=12)
plt.tight_layout()
plt.show()

# 6. Nuage de points Seaborn : Profit vs Remise
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="Discount", y="Profit", alpha=0.5, color="green")
plt.title("Relation entre le profit et la remise accordée", fontsize=14)
plt.xlabel("Remise (0 = aucune, 1 = 100%)", fontsize=12)
plt.ylabel("Profit (USD)", fontsize=12)
plt.axhline(y=0, color='red', linestyle='--', alpha=0.6, label="Seuil de rentabilité")
plt.legend()
plt.tight_layout()
plt.show()

# 7. Analyse comparative (affichée en console)
print("\n" + "="*60)
print("ANALYSE COMPARATIVE : MATPLOTLIB vs SEABORN")
print("="*60)
print("""
- Facilité d'utilisation :
    * Seaborn : syntaxe plus simple, thèmes élégants par défaut, idéal pour l'exploration rapide.
    * Matplotlib : plus de code pour un rendu similaire, mais contrôle absolu.
- Interactivité :
    * Matplotlib + mplcursors permet une interactivité basique (survol, clic) – adapté pour des graphiques simples.
    * Seaborn n'offre pas d'interactivité native, nécessite de passer par Matplotlib en sous-jacent.
- Cartes :
    * Matplotlib nécessite des librairies additionnelles lourdes (cartopy, geopandas).
    * Seaborn ne gère pas les cartes. Plotly (utilisé ici) est bien plus adapté et interactif.
- Graphiques statistiques :
    * Seaborn intègre nativement régressions, distributions, boxplots, heatmaps.
    * Matplotlib impose de tout coder à la main.
- Performance :
    * Les deux sont équivalents pour des volumes de données modérés.
- Cas d'usage recommandé :
    * Seaborn : analyse exploratoire, rapports standards, grilles de graphiques.
    * Matplotlib : personnalisation avancée, intégration d'interactivité simple, graphiques très spécifiques.
    * Plotly : cartes et visualisations interactives riches (dashboard léger).
""")
