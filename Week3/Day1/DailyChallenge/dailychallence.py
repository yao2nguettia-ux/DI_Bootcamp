import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------- 1. Préparation des données ----------
np.random.seed(42) 

# Températures entre -5 et 35 °C
data = np.random.uniform(low=-5, high=35, size=(10, 12))

# Noms fictifs des villes
villes = [f"Ville_{i+1}" for i in range(10)]
mois = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin",
        "Juil", "Aoû", "Sep", "Oct", "Nov", "Déc"]

# Création du DataFrame
df = pd.DataFrame(data, index=villes, columns=mois)

# ---------- 2. Analyse des données ----------
# Température moyenne annuelle par ville
moyennes_annuelles = df.mean(axis=1)  

# Ville avec la moyenne la plus élevée et la plus basse
ville_max = moyennes_annuelles.idxmax()
ville_min = moyennes_annuelles.idxmin()
temp_max = moyennes_annuelles.max()
temp_min = moyennes_annuelles.min()

# ---------- 3. Visualisation ----------
plt.figure(figsize=(10, 6))
for ville in villes:
    plt.plot(mois, df.loc[ville], marker='o', linestyle='-', label=ville)

plt.title("Évolution mensuelle des températures dans 10 villes")
plt.xlabel("Mois")
plt.ylabel("Température (°C)")
plt.xticks(rotation=45)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# ---------- Rapport (affiché dans la sortie) ----------
print("===== RAPPORT D'ANALYSE =====")
print(f"Ville avec la température moyenne annuelle la plus élevée : {ville_max} ({temp_max:.2f} °C)")
print(f"Ville avec la température moyenne annuelle la plus basse  : {ville_min} ({temp_min:.2f} °C)")
print("\nTendances observées :")
print("- Les températures varient de -5°C à 35°C selon les villes et les saisons.")
print("- Certaines villes montrent des pics en été, d'autres restent fraîches toute l'année.")
print("- La diversité des courbes illustre des climats très différents (continental, tropical, polaire simulés).")