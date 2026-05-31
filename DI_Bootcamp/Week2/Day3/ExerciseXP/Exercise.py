#Exercice 1 : Utilisation de base de SciPy

import scipy
print("Version de SciPy :", scipy.__version__)

#Exercice 2 : Statistiques descriptives

import scipy.stats as stats

data = [12, 15, 13, 12, 18, 20, 22, 21]

moyenne = stats.tmean(data)           # moyenne tronquée (par défaut sans troncature) ou bien np.mean
mediane = stats.tmean(data, limits=(None, None))  # ou simplement np.median(data)
# Pour éviter toute confusion, utilisons directement numpy :
import numpy as np
moyenne = np.mean(data)
mediane = np.median(data)
variance = np.var(data, ddof=1)       # variance échantillonnale (ddof=1)
ecart_type = np.std(data, ddof=1)

print(f"Moyenne : {moyenne}")
print(f"Médiane : {mediane}")
print(f"Variance : {variance}")
print(f"Écart-type : {ecart_type}")
#Remarque : stats.tmean calcule la moyenne tronquée (ignore un pourcentage d’extrêmes). Pour la moyenne arithmétique classique, mieux vaut utiliser np.mean.

# Exercice 3 : Générer et tracer une distribution normale

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

mu, sigma = 50, 10
x = np.linspace(mu - 4*sigma, mu + 4*sigma, 200)
pdf = norm.pdf(x, mu, sigma)

plt.plot(x, pdf, color='blue')
plt.title(f"Distribution normale (μ={mu}, σ={sigma})")
plt.xlabel("Valeur")
plt.ylabel("Densité de probabilité")
plt.grid(alpha=0.3)
plt.show()

# Exercice 4 : Test T sur deux échantillons aléatoires

import numpy as np
from scipy.stats import ttest_ind

np.random.seed(42)  # pour reproductibilité
data1 = np.random.normal(50, 10, 100)
data2 = np.random.normal(60, 10, 100)

t_stat, p_val = ttest_ind(data1, data2)
print(f"Statistique T : {t_stat:.4f}")
print(f"Valeur p : {p_val:.4e}")

alpha = 0.05
if p_val < alpha:
    print("Rejet de H0 : les moyennes sont significativement différentes.")
else:
    print("On ne rejette pas H0 : pas de différence significative.")

# Exercice 5 : Régression linéaire (prix immobiliers)

import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt

house_sizes = np.array([50, 70, 80, 100, 120])      # m²
house_prices = np.array([150000, 200000, 210000, 250000, 280000])  # monnaie

slope, intercept, r_value, p_value, std_err = linregress(house_sizes, house_prices)

print(f"Pente : {slope:.2f}")          # environ 2125
print(f"Ordonnée à l'origine : {intercept:.2f}")  # environ 50000

# Estimation pour 90 m²
price_90 = slope * 90 + intercept
print(f"Prix estimé pour 90 m² : {price_90:.0f}")

# Interprétation
print("\nInterprétation : la pente indique qu'en moyenne, chaque mètre carré supplémentaire")
print(f"augmente le prix d'environ {slope:.0f} unités monétaires.")

# Graphique
plt.scatter(house_sizes, house_prices, color='red', label="Données")
plt.plot(house_sizes, slope*house_sizes + intercept, label="Régression linéaire")
plt.xlabel("Taille (m²)")
plt.ylabel("Prix (€)")
plt.legend()
plt.show()

# Exercice 6 : ANOVA (comparaison de trois engrais)

import numpy as np
from scipy.stats import f_oneway

fertilizer_1 = [5, 6, 7, 6, 5]
fertilizer_2 = [7, 8, 7, 9, 8]
fertilizer_3 = [4, 5, 4, 3, 4]

f_stat, p_val = f_oneway(fertilizer_1, fertilizer_2, fertilizer_3)

print(f"Valeur F : {f_stat:.4f}")
print(f"Valeur p : {p_val:.4e}")

alpha = 0.05
if p_val < alpha:
    print("Rejet de H0 : au moins un engrais a un effet significativement différent.")
else:
    print("Pas de différence significative entre les engrais.")

# Question supplémentaire :
print("\nSi la valeur p était > 0.05, on ne pourrait pas conclure à une différence significative.")
print("Cela signifierait que les différences observées entre les groupes peuvent être dues au hasard.")

# Exercice 7 (facultatif) : Distribution binomiale

from scipy.stats import binom

n, p = 10, 0.5   # 10 lancers, probabilité d'une face = 0.5
k = 5            # exactement 5 faces

prob_exacte = binom.pmf(k, n, p)
print(f"Probabilité d'obtenir exactement {k} faces en {n} lancers : {prob_exacte:.4f}")

# Pour visualiser toutes les probabilités
import matplotlib.pyplot as plt
x = range(0, n+1)
probs = binom.pmf(x, n, p)
plt.bar(x, probs)
plt.title(f"Distribution binomiale (n={n}, p={p})")
plt.xlabel("Nombre de succès")
plt.ylabel("Probabilité")
plt.show()

#Exercice 8 : Corrélation de Pearson et Spearman

import pandas as pd
from scipy.stats import pearsonr, spearmanr

data = pd.DataFrame({
    'age': [23, 25, 30, 35, 40],
    'income': [35000, 40000, 50000, 60000, 70000]
})

pearson_corr, _ = pearsonr(data['age'], data['income'])
spearman_corr, _ = spearmanr(data['age'], data['income'])

print(f"Corrélation de Pearson : {pearson_corr:.4f}")
print(f"Corrélation de Spearman : {spearman_corr:.4f}")

# Interprétation : valeurs proches de 1 indiquent une forte relation positive.