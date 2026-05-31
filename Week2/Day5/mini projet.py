# 1. Importer les bibliothèques nécessaires
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Pour un affichage correct des graphiques
%matplotlib inline

# Le fichier s'appelle "US Superstore data.xls" avec la feuille "Orders"
file_path = "US Superstore data.xls"   # à adapter si nécessaire
df = pd.read_excel(file_path, sheet_name="Orders")

# 3. Aperçu des données et prétraitement
print("Aperçu des données :")
print(df.head())
print("\nInformations :")
print(df.info())
print("\nValeurs manquantes :")
print(df.isnull().sum())

# Convertir les dates si nécessaire
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# Vérifier les types
print("\nTypes après conversion :")
print(df.dtypes)

# ------------------------------------------------------------
# Question 1 : Quels sont les États qui enregistrent le plus de ventes ?
state_sales = df.groupby("State")["Sales"].sum().sort_values(ascending=False)
top10_states = state_sales.head(10)

plt.figure(figsize=(10,6))
sns.barplot(x=top10_states.values, y=top10_states.index, palette="viridis")
plt.title("Top 10 des États par ventes totales")
plt.xlabel("Ventes totales ($)")
plt.ylabel("État")
plt.tight_layout()
plt.show()

print("\nTop 10 États par ventes :")
print(top10_states)

# ------------------------------------------------------------
# Question 2 : Différence entre New York et Californie (chiffre d'affaires et bénéfice)
ny_sales = df[df["State"] == "New York"]["Sales"].sum()
ca_sales = df[df["State"] == "California"]["Sales"].sum()
ny_profit = df[df["State"] == "New York"]["Profit"].sum()
ca_profit = df[df["State"] == "California"]["Profit"].sum()

print("\nComparaison New York vs Californie :")
print(f"New York - Ventes: ${ny_sales:,.2f}, Profit: ${ny_profit:,.2f}")
print(f"Californie - Ventes: ${ca_sales:,.2f}, Profit: ${ca_profit:,.2f}")
print(f"Différence de ventes (CA - NY) : ${ca_sales - ny_sales:,.2f}")
print(f"Différence de profit (CA - NY) : ${ca_profit - ny_profit:,.2f}")

# ------------------------------------------------------------
# Question 3 : Client exceptionnel à New York
ny_customers = df[df["State"] == "New York"].groupby("Customer Name")["Profit"].sum()
top_ny_customer = ny_customers.idxmax()
top_ny_profit = ny_customers.max()
print(f"\nClient exceptionnel à New York : {top_ny_customer} avec un profit de ${top_ny_profit:,.2f}")

# ------------------------------------------------------------
# Question 4 : Différences de rentabilité entre les États
state_profit = df.groupby("State")["Profit"].sum().sort_values(ascending=False)
plt.figure(figsize=(12,6))
state_profit.head(15).plot(kind="bar", color="teal")
plt.title("Top 15 des États par profit total")
plt.ylabel("Profit ($)")
plt.xlabel("État")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
print("\nTop 10 États par profit :")
print(state_profit.head(10))

# ------------------------------------------------------------
# Question 5 : Principe de Pareto sur les clients et le profit
customer_profit = df.groupby("Customer Name")["Profit"].sum().sort_values(ascending=False)
cumulative_profit = customer_profit.cumsum()
total_profit = cumulative_profit.iloc[-1]
cumulative_percent = (cumulative_profit / total_profit) * 100

# Trouver le nombre de clients nécessaires pour atteindre 80% du profit
n_customers = len(customer_profit)
threshold_80 = cumulative_percent[cumulative_percent >= 80].iloc[0]
n_top_customers = (cumulative_percent < 80).sum() + 1
percent_customers = (n_top_customers / n_customers) * 100

print(f"\nPrincipe de Pareto (profit) :")
print(f"Nombre total de clients : {n_customers}")
print(f"Les {n_top_customers} meilleurs clients représentent {percent_customers:.2f}% des clients")
print(f"Ils contribuent à {threshold_80:.2f}% du profit total.")
if percent_customers <= 20:
    print("=> Le principe de Pareto s'applique (20% des clients génèrent 80% du profit).")
else:
    print("=> Le principe de Pareto ne s'applique pas parfaitement (plus de 20% des clients sont nécessaires).")

# Tracé de la courbe cumulative
plt.figure(figsize=(8,6))
plt.plot(np.arange(1, n_customers+1), cumulative_percent, label="Profit cumulé")
plt.axhline(y=80, color='r', linestyle='--', label="80%")
plt.axvline(x=n_top_customers, color='g', linestyle='--', label=f"{percent_customers:.1f}% des clients")
plt.xlabel("Nombre de clients")
plt.ylabel("Pourcentage cumulé du profit")
plt.title("Courbe de Pareto – Profit par client")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# Question 6 : Top 20 villes par ventes et par profit
city_sales = df.groupby("City")["Sales"].sum().sort_values(ascending=False).head(20)
city_profit = df.groupby("City")["Profit"].sum().sort_values(ascending=False).head(20)

print("\nTop 20 villes par ventes :")
print(city_sales)
print("\nTop 20 villes par profit :")
print(city_profit)

# Comparaison des rentabilités : les villes présentes dans les deux tops
common_cities = set(city_sales.index) & set(city_profit.index)
print(f"\nVilles communes dans les deux tops : {len(common_cities)}")
print(common_cities)

# Visualisation : top 10 villes par profit
plt.figure(figsize=(10,6))
city_profit.head(10).plot(kind="bar", color="orange")
plt.title("Top 10 des villes par profit total")
plt.ylabel("Profit ($)")
plt.xlabel("Ville")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# Question 7 : Top 20 clients par ventes
customer_sales = df.groupby("Customer Name")["Sales"].sum().sort_values(ascending=False).head(20)
print("\nTop 20 clients par ventes :")
print(customer_sales)

# ------------------------------------------------------------
# Question 8 : Courbe cumulative des ventes par client (Pareto pour les ventes)
customer_sales_all = df.groupby("Customer Name")["Sales"].sum().sort_values(ascending=False)
cumulative_sales = customer_sales_all.cumsum()
total_sales = cumulative_sales.iloc[-1]
cumulative_sales_percent = (cumulative_sales / total_sales) * 100

n_customers_sales = len(customer_sales_all)
threshold_80_sales = cumulative_sales_percent[cumulative_sales_percent >= 80].iloc[0]
n_top_customers_sales = (cumulative_sales_percent < 80).sum() + 1
percent_customers_sales = (n_top_customers_sales / n_customers_sales) * 100

print(f"\nPrincipe de Pareto (ventes) :")
print(f"Les {n_top_customers_sales} meilleurs clients représentent {percent_customers_sales:.2f}% des clients")
print(f"Ils contribuent à {threshold_80_sales:.2f}% des ventes totales.")

plt.figure(figsize=(8,6))
plt.plot(np.arange(1, n_customers_sales+1), cumulative_sales_percent, label="Ventes cumulées")
plt.axhline(y=80, color='r', linestyle='--', label="80%")
plt.axvline(x=n_top_customers_sales, color='g', linestyle='--', label=f"{percent_customers_sales:.1f}% des clients")
plt.xlabel("Nombre de clients")
plt.ylabel("Pourcentage cumulé des ventes")
plt.title("Courbe de Pareto – Ventes par client")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# Question 9 : Recommandations marketing basées sur les États et les villes
print("\n" + "="*60)
print("RECOMMANDATIONS MARKETING")
print("="*60)
print("""
- Les États les plus performants en termes de ventes sont : Californie, New York, Texas.
  Concentrez vos efforts marketing sur ces États tout en surveillant la rentabilité.

- Bien que la Californie génère plus de ventes que New York, son profit est inférieur.
  Il faut analyser les raisons (réductions trop élevées, coûts, produits peu rentables).

- Le client exceptionnel à New York (à fort profit) peut être ciblé pour des programmes de fidélité ou des offres personnalisées.

- Les villes avec un fort volume de ventes mais un faible profit (ex: Los Angeles, Philadelphia)
  nécessitent une optimisation des marges ou des campagnes plus rentables.

- Le principe de Pareto s'applique partiellement : environ {percent_customers:.1f}% des clients génèrent 80% du profit.
  Il est donc crucial de fidéliser les clients à haute valeur ajoutée.

- Pour les ventes, {percent_customers_sales:.1f}% des clients génèrent 80% des ventes.
  Une stratégie de segmentation client est recommandée.

- Priorisez les villes apparaissant à la fois dans le top 20 ventes et top 20 profit
  (ex: New York City, Los Angeles, Seattle, San Francisco) pour des actions marketing ciblées.
""".format(percent_customers=percent_customers, percent_customers_sales=percent_customers_sales))

print("Fin de l'analyse.")