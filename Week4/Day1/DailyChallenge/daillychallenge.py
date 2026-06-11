from IPython.display import Markdown, display, Image
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

# Cellule 2 : Résumé général (affichage Markdown)
display(Markdown("""
## 1. Résumé : Bases et importance du ML pour les analystes

L’**apprentissage automatique** permet aux ordinateurs d’apprendre à partir de données sans programmation explicite.
- Détection automatique de patterns
- Prédiction sur de nouvelles données
- Complément aux stats traditionnelles

Pour l’analyste : gain de temps, détection de relations complexes, automatisabilité.

---

## 2. Applications sectorielles

| Secteur | Exemple |
|---------|---------|
| Finance | Détection de fraudes bancaires |
| Santé | Diagnostic assisté par IRM |
| E‑commerce | Système de recommandation |

---

## 3. Types d’apprentissage

| Type | Définition | Exemple |
|------|-------------|---------|
| Supervisé | Données étiquetées | Classification spam / non spam |
| Non supervisé | Données non étiquetées | Segmentation clients (clustering) |
| Renforcement | Apprentissage par récompenses | Robot qui apprend à marcher |

"""))

# Cellule 3 : Organigramme du processus ML (avec matplotlib)
display(Markdown("## 4. Processus ML : sélection des caractéristiques → modèle → évaluation"))

# Création d'un organigramme simple avec matplotlib
fig, ax = plt.subplots(figsize=(10, 5))
ax.axis('off')

# Définir les boîtes
steps = [
    "Données brutes", "Nettoyage", "Sélection\ncaractéristiques",
    "Sélection\nmodèle", "Entraînement", "Évaluation", "Déploiement"
]
x_pos = np.linspace(0, 10, len(steps))
y_pos = [2] * len(steps)

for i, (step, x) in enumerate(zip(steps, x_pos)):
    ax.add_patch(plt.Rectangle((x-0.4, y_pos[i]-0.3), 0.8, 0.6, 
                                facecolor='lightblue', edgecolor='black'))
    ax.text(x, y_pos[i], step, ha='center', va='center', fontsize=9)

# Flèches
for i in range(len(steps)-1):
    ax.annotate('', xy=(x_pos[i+1]-0.4, y_pos[i]), xytext=(x_pos[i]+0.4, y_pos[i]),
                arrowprops=dict(arrowstyle='->', lw=1.5))

ax.set_xlim(-1, 11)
ax.set_ylim(1.5, 2.5)
plt.title("Organigramme du développement d'un modèle ML", fontsize=14)
plt.show()

# Cellule 4 : Exemple concret - Classification supervisée
display(Markdown("## 5. Exemple pratique : Classification supervisée (Random Forest)"))

# Générer un petit jeu de données
X, y = make_classification(n_samples=200, n_features=5, n_informative=4,
                           n_redundant=1, random_state=42)

# Séparation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Sélection du modèle
model = RandomForestClassifier(n_estimators=50, random_state=42)

# Entraînement
model.fit(X_train, y_train)

# Évaluation
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print(f"Précision du modèle : {acc:.2f}")
print("\nRapport de classification :")
print(classification_report(y_test, y_pred, target_names=["Classe 0", "Classe 1"]))

# Feature importance (sélection des caractéristiques)
importances = model.feature_importances_
features_names = [f"Caractéristique {i+1}" for i in range(5)]

plt.figure(figsize=(6,4))
plt.barh(features_names, importances, color='skyblue')
plt.xlabel("Importance")
plt.title("Importance des caractéristiques (sélection implicite)")
plt.tight_layout()
plt.show()

display(Markdown("""
### 🔍 Explication des 3 étapes dans cet exemple :

1. **Sélection des caractéristiques** :  
   - Ici, nous avons gardé les 5 variables de base.  
   - Le Random Forest a calculé une importance : on pourrait supprimer les moins importantes.

2. **Sélection du modèle** :  
   - On a choisi une forêt aléatoire (RandomForestClassifier).  
   - On pourrait comparer avec SVM, régression logistique, etc.

3. **Évaluation du modèle** :  
   - Métrique : précision (accuracy) + rapport complet.  
   - Validation sur données de test non vues pendant l’entraînement.

"""))

# Cellule 5 : Différence rapide - Non supervisé (clustering)
display(Markdown("## 6. Illustration - Apprentissage non supervisé (K‑means)"))

from sklearn.cluster import KMeans

# Générer des données non étiquetées
X_nonsup, _ = make_classification(n_samples=150, n_features=2, n_informative=2,
                                   n_redundant=0, n_clusters_per_class=1, random_state=42)

kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_nonsup)

plt.scatter(X_nonsup[:,0], X_nonsup[:,1], c=clusters, cmap='viridis', alpha=0.7)
plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1],
            marker='X', s=200, c='red', label='Centroïdes')
plt.title("Clustering non supervisé (K‑means)")
plt.legend()
plt.show()

display(Markdown("""
> Ici, le modèle a trouvé 2 groupes sans aucune étiquette.  
> C’est typique du **non supervisé**.
"""))