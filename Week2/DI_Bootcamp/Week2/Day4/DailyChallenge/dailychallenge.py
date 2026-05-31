# %% [markdown]
# # Défi quotidien : Analyse stratégique des performances des supermarchés
# 
# ## Import des bibliothèques et chargement des données

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ipywidgets as widgets
from ipywidgets import interact, Dropdown, IntSlider
from IPython.display import display
import warnings
warnings.filterwarnings('ignore')

# Chargement du dataset
df = pd.read_csv('superstore_dataset.csv')

# Exploration préliminaire
print("Dataset Shape:", df.shape)
print("\nColumn Names:")
print(df.columns.tolist())
df.info()
df.describe()
print("\nMissing values per column:\n", df.isnull().sum())

# %% [markdown]
# ## 1. Définition et préparation des données
# 
# ### Gestion des doublons et valeurs manquantes

# Supprimer les doublons
initial_rows = len(df)
df = df.drop_duplicates()
print(f"Doublons supprimés : {initial_rows - len(df)} lignes")

# Traitement des valeurs manquantes (exemple : code postal = 0)
if 'Postal Code' in df.columns:
    df['Postal Code'] = df['Postal Code'].fillna(0)

# Autres colonnes avec peu de valeurs manquantes (optionnel)
df = df.dropna(subset=['City', 'State'])  # suppression si essentielles

# %% [markdown]
# ### Correction des types de données

date_columns = ['Order Date', 'Ship Date']
for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col])
        print(f"{col} convertie en datetime")

# %% [markdown]
# ### Ingénierie des fonctionnalités

# Calcul de la marge bénéficiaire (éviter division par zéro)
df['Profit Margin'] = (df['Profit'] / df['Sales'].replace(0, np.nan)) * 100
# Extraire l'année et le mois
df['Order Year'] = df['Order Date'].dt.year
df['Order Month'] = df['Order Date'].dt.month
df['Order Month-Year'] = df['Order Date'].dt.to_period('M')
print("Nouvelles colonnes créées :", [c for c in df.columns if c not in ['Profit Margin', 'Order Year', 'Order Month', 'Order Month-Year']])

# %% [markdown]
# ## 2. Analyse exploratoire approfondie (Matplotlib)
# 
# ### Graphique linéaire interactif des ventes mensuelles par catégorie

monthly_sales = df.groupby(['Order Month-Year', 'Category'])['Sales'].sum().reset_index()
monthly_sales['Date'] = monthly_sales['Order Month-Year'].dt.to_timestamp()

def plot_monthly_sales(category='All'):
    plt.figure(figsize=(12, 6))
    if category == 'All':
        total = df.groupby('Order Month-Year')['Sales'].sum()
        plt.plot(total.index.to_timestamp(), total.values, marker='o', linewidth=2)
        plt.title('Tendance mensuelle des ventes - Toutes catégories', fontweight='bold')
    else:
        cat_data = monthly_sales[monthly_sales['Category'] == category]
        plt.plot(cat_data['Date'], cat_data['Sales'], marker='o', linewidth=2)
        plt.title(f'Tendance mensuelle des ventes - {category}', fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('Ventes ($)')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

categories = ['All'] + list(df['Category'].unique())
category_dropdown = Dropdown(options=categories, value='All', description='Catégorie:')
interact(plot_monthly_sales, category=category_dropdown);

# %% [markdown]
# ### Graphique à barres horizontales des ventes par État (Top N interactif)

state_sales = df.groupby('State')['Sales'].sum().sort_values(ascending=True)

def plot_top_states(top_n=10):
    plt.figure(figsize=(12, max(6, top_n * 0.4)))
    top_states = state_sales.tail(top_n)
    plt.barh(range(len(top_states)), top_states.values, color='steelblue')
    plt.yticks(range(len(top_states)), top_states.index)
    plt.xlabel('Ventes totales ($)')
    plt.ylabel('État')
    plt.title(f'Top {top_n} États par ventes', fontweight='bold')
    for i, (state, val) in enumerate(top_states.items()):
        plt.text(val + max(top_states.values())*0.01, i, f'${val:,.0f}', va='center')
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.show()
    print(f"Total États analysés : {len(state_sales)}")
    print(f"Top {top_n} États représentent ${top_states.sum():,.0f} de ventes")

top_n_slider = IntSlider(min=5, max=25, value=10, description='Nombre d\'États:')
interact(plot_top_states, top_n=top_n_slider);

# %% [markdown]
# ## 3. Communiquer des informations (Seaborn)
# 
# ### Top 10 produits les plus rentables

product_profit = df.groupby('Product Name')['Profit'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12, 8))
ax = sns.barplot(x=product_profit.values, y=product_profit.index, palette='viridis')
plt.title('Top 10 des produits les plus rentables\nRésumé exécutif', fontweight='bold', fontsize=14)
plt.xlabel('Profit total ($)')
plt.ylabel('Nom du produit')
for i, (prod, profit) in enumerate(product_profit.items()):
    ax.text(profit + max(product_profit.values())*0.01, i, f'${profit:,.0f}', va='center')
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.show()

# %% [markdown]
# ### Diagramme de dispersion Remise vs Profit avec régression

plt.figure(figsize=(14, 8))
sns.scatterplot(data=df, x='Discount', y='Profit', hue='Category', alpha=0.6, s=50)
sns.regplot(data=df, x='Discount', y='Profit', scatter=False, color='red', line_kws={'linewidth':2, 'linestyle':'--'})
plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
plt.title('Impact des remises sur la rentabilité par catégorie', fontweight='bold')
plt.xlabel('Taux de remise')
plt.ylabel('Profit ($)')
plt.legend(title='Catégorie', bbox_to_anchor=(1.05, 1))
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# Analyse supplémentaire
high_discount = df[df['Discount'] > 0.2]
print(f"Transactions avec remise >20% : {len(high_discount)}")
print(f"Profit moyen : ${high_discount['Profit'].mean():.2f}")
print(f"% de pertes : {(high_discount['Profit'] < 0).mean()*100:.1f}%")

# %% [markdown]
# ## 4. Revue de la méthodologie et des outils
# 
# **Comparaison Matplotlib vs Seaborn** (cellule Markdown) – voir ci-dessous.
# 
# Ici nous ajoutons une démonstration de code de timing.

import time

# Matplotlib
start = time.time()
plt.figure(figsize=(8,6))
plt.plot(df.groupby('Order Year')['Sales'].sum())
plt.close()
mat_time = time.time() - start

# Seaborn
start = time.time()
sns.lineplot(data=df.groupby('Order Year')['Sales'].sum().reset_index(), x='Order Year', y='Sales')
plt.close()
sea_time = time.time() - start

print(f"Temps Matplotlib : {mat_time:.4f}s")
print(f"Temps Seaborn   : {sea_time:.4f}s")
print("Recommandation : exploration rapide → Matplotlib ; présentations stakeholders → Seaborn")

# %% [markdown]
# ## 5. Livrable final – Résumé exécutif automatisé

total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
profit_margin = (total_profit / total_sales) * 100
top_state = state_sales.index[-1]
top_state_sales = state_sales.iloc[-1]
top_category = df.groupby('Category')['Sales'].sum().sort_values(ascending=False).index[0]
top_product = product_profit.index[0]
high_discount_loss_rate = (df[df['Discount'] > 0.2]['Profit'] < 0).mean() * 100

print("\n=== RÉSUMÉ EXÉCUTIF - PRINCIPALES CONCLUSIONS ===")
print(f"📊 PERFORMANCE GÉNÉRALE :")
print(f"   • Chiffre d'affaires total : ${total_sales:,.0f}")
print(f"   • Profit total : ${total_profit:,.0f}")
print(f"   • Marge bénéficiaire : {profit_margin:.1f}%")
print(f"\n🗺️ PERFORMANCE GÉOGRAPHIQUE :")
print(f"   • État le plus performant : {top_state} (${top_state_sales:,.0f})")
print(f"   • Concentration des ventes : Top 5 États = {(state_sales.tail(5).sum()/total_sales)*100:.1f}%")
print(f"\n🏆 PERFORMANCE PRODUIT :")
print(f"   • Catégorie leader : {top_category}")
print(f"   • Produit le plus rentable : {top_product}")
print(f"\n💰 STRATÉGIE DE REMISE :")
print(f"   • Risque : {high_discount_loss_rate:.1f}% des remises >20% génèrent des pertes")
print(f"   • Seuil recommandé : limiter les remises à 20% maximum, sauf validation")

# %% [markdown]
# ## (Optionnel) Tableau de bord multi-graphiques

def create_dashboard():
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16,12))
    monthly = df.groupby('Order Month-Year')['Sales'].sum()
    ax1.plot(monthly.index.to_timestamp(), monthly.values, marker='o')
    ax1.set_title('Ventes mensuelles')
    ax1.tick_params(axis='x', rotation=45)
    cat_sales = df.groupby('Category')['Sales'].sum()
    ax2.bar(cat_sales.index, cat_sales.values)
    ax2.set_title('Ventes par catégorie')
    top10 = state_sales.tail(10)
    ax3.barh(range(len(top10)), top10.values)
    ax3.set_yticks(range(len(top10))); ax3.set_yticklabels(top10.index)
    ax3.set_title('Top 10 États')
    for cat in df['Category'].unique():
        sub = df[df['Category'] == cat]
        ax4.scatter(sub['Discount'], sub['Profit'], label=cat, alpha=0.5)
    ax4.axhline(0, color='k', linestyle='--')
    ax4.set_xlabel('Remise'); ax4.set_ylabel('Profit')
    ax4.set_title('Remise vs Profit')
    ax4.legend()
    plt.tight_layout()
    plt.show()

create_dashboard()

# %% [markdown]
# ## (Optionnel) Annotation des outliers et comparaison avec Plotly

# Outliers
plt.figure(figsize=(12,8))
sns.scatterplot(data=df, x='Discount', y='Profit', hue='Category', alpha=0.6)
top3 = df.nlargest(3, 'Profit')
bottom3 = df.nsmallest(3, 'Profit')
for _, row in top3.iterrows():
    plt.annotate(f'Best ${row["Profit"]:.0f}', (row['Discount'], row['Profit']),
                 xytext=(10,10), textcoords='offset points', bbox=dict(boxstyle='round', facecolor='green', alpha=0.7))
for _, row in bottom3.iterrows():
    plt.annotate(f'Worst ${row["Profit"]:.0f}', (row['Discount'], row['Profit']),
                 xytext=(10,-20), textcoords='offset points', bbox=dict(boxstyle='round', facecolor='red', alpha=0.7))
plt.title('Identification des outliers')
plt.show()

try:
    import plotly.express as px
    fig = px.scatter(df, x='Discount', y='Profit', color='Category',
                     hover_data=['Product Name', 'Sales'],
                     title='Analyse interactive remise vs profit')
    fig.show()
    print("Plotly offre interactivité immédiate, mais Matplotlib + ipywidgets donne plus de contrôle.")
except ImportError:
    print("Plotly non installé – passer à Matplotlib")