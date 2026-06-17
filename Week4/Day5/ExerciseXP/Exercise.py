# ====================================================================
# PROJET : PRÉDICTION DES MALADIES CARDIAQUES PAR RÉGRESSION LOGISTIQUE
# ====================================================================
# Auteur : [Votre Nom]
# Date : [Date]
# Description : Utilisation du dataset UCI Heart Disease pour prédire
#              la présence de maladie cardiaque.
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
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report, roc_curve, auc
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

# Configuration des visualisations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
%matplotlib inline

# ====================================================================
# 2. CHARGEMENT ET EXPLORATION DES DONNÉES (EDA)
# ====================================================================

# Chargement du dataset
df = pd.read_csv('heart_disease_uci.csv')
print("="*60)
print("ANALYSE EXPLORATOIRE DES DONNÉES (EDA)")
print("="*60)
print(f"\n📊 Shape du dataset: {df.shape}")
print(f"📋 Nombre de colonnes: {len(df.columns)}")
print(f"👥 Nombre de patients: {len(df)}")

# Aperçu des données
print("\n🔍 Aperçu des 5 premières lignes:")
print(df.head())

# Informations générales
print("\n📄 Informations sur les colonnes:")
print(df.info())

# Statistiques descriptives
print("\n📊 Statistiques descriptives:")
print(df.describe())

# ====================================================================
# 3. ANALYSE DES VALEURS MANQUANTES
# ====================================================================

print("\n" + "="*60)
print("ANALYSE DES VALEURS MANQUANTES")
print("="*60)

missing_values = df.isnull().sum()
missing_percentage = (missing_values / len(df)) * 100
missing_df = pd.DataFrame({
    'Valeurs manquantes': missing_values,
    'Pourcentage (%)': missing_percentage
}).sort_values(by='Pourcentage (%)', ascending=False)
missing_df = missing_df[missing_df['Valeurs manquantes'] > 0]

print("\n📊 Colonnes avec valeurs manquantes:")
print(missing_df)

# Visualisation des valeurs manquantes
plt.figure(figsize=(12, 6))
plt.barh(missing_df.index, missing_df['Pourcentage (%)'], color='steelblue')
plt.xlabel('Pourcentage de valeurs manquantes (%)')
plt.title('Valeurs manquantes par colonne')
plt.tight_layout()
plt.show()

# ====================================================================
# 4. ANALYSE DE LA VARIABLE CIBLE
# ====================================================================

print("\n" + "="*60)
print("ANALYSE DE LA VARIABLE CIBLE")
print("="*60)

# Création de la variable cible binaire (0 = pas de maladie, 1 = maladie)
df['target'] = (df['num'] > 0).astype(int)

print(f"\n📊 Distribution de 'num' (0-4):")
print(df['num'].value_counts().sort_index())

print(f"\n📊 Distribution binaire (target):")
print(df['target'].value_counts())
print(f"\n📈 Pourcentage:")
print(df['target'].value_counts(normalize=True) * 100)

# Visualisation de la cible
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Distribution originale
df['num'].value_counts().sort_index().plot(kind='bar', ax=axes[0], color='skyblue')
axes[0].set_title('Distribution de num (0-4)')
axes[0].set_xlabel('Niveau de maladie (0 = aucune)')
axes[0].set_ylabel('Nombre de patients')
axes[0].grid(axis='y', alpha=0.3)

# Distribution binaire
colors = ['lightgreen', 'salmon']
df['target'].value_counts().plot(kind='bar', ax=axes[1], color=colors)
axes[1].set_title('Distribution binaire (0 = Pas de maladie, 1 = Maladie)')
axes[1].set_xlabel('Classe')
axes[1].set_ylabel('Nombre de patients')
axes[1].set_xticklabels(['Pas de maladie', 'Maladie'], rotation=0)
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

# ====================================================================
# 5. ANALYSE DES VARIABLES NUMÉRIQUES
# ====================================================================

print("\n" + "="*60)
print("ANALYSE DES VARIABLES NUMÉRIQUES")
print("="*60)

numeric_cols = ['age', 'trestbps', 'chol', 'thalch', 'oldpeak']

# Statistiques des variables numériques
print("\n📊 Statistiques des variables numériques:")
print(df[numeric_cols].describe())

# Visualisation des distributions
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for i, col in enumerate(numeric_cols):
    if col in df.columns:
        sns.histplot(df[col].dropna(), kde=True, ax=axes[i], color='steelblue')
        axes[i].set_title(f'Distribution de {col}')
        axes[i].set_xlabel(col)
        axes[i].set_ylabel('Fréquence')
        axes[i].grid(alpha=0.3)

# Supprimer le sous-graphique vide
if len(numeric_cols) < len(axes):
    for j in range(len(numeric_cols), len(axes)):
        fig.delaxes(axes[j])

plt.tight_layout()
plt.show()

# ====================================================================
# 6. ANALYSE DES VARIABLES CATÉGORIELLES
# ====================================================================

print("\n" + "="*60)
print("ANALYSE DES VARIABLES CATÉGORIELLES")
print("="*60)

categorical_cols = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal']

print("\n📊 Fréquences des variables catégorielles:")
for col in categorical_cols:
    if col in df.columns:
        print(f"\n{col}:")
        print(df[col].value_counts())

# Visualisation des variables catégorielles
fig, axes = plt.subplots(2, 4, figsize=(16, 10))
axes = axes.flatten()

for i, col in enumerate(categorical_cols):
    if col in df.columns and i < len(axes):
        df[col].value_counts().plot(kind='bar', ax=axes[i], color='coral')
        axes[i].set_title(f'Distribution de {col}')
        axes[i].set_xlabel(col)
        axes[i].set_ylabel('Nombre')
        axes[i].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

# ====================================================================
# 7. RELATION ENTRE LES VARIABLES ET LA CIBLE
# ====================================================================

print("\n" + "="*60)
print("RELATION AVEC LA VARIABLE CIBLE")
print("="*60)

# Variables catégorielles vs cible
fig, axes = plt.subplots(2, 4, figsize=(16, 10))
axes = axes.flatten()

for i, col in enumerate(categorical_cols):
    if col in df.columns and i < len(axes):
        pd.crosstab(df[col], df['target'], normalize='index').plot(
            kind='bar', ax=axes[i], stacked=True, color=['lightgreen', 'salmon']
        )
        axes[i].set_title(f'{col} vs Cible')
        axes[i].set_xlabel(col)
        axes[i].set_ylabel('Proportion')
        axes[i].legend(title='Maladie', labels=['Non', 'Oui'])
        axes[i].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

# Variables numériques vs cible
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for i, col in enumerate(numeric_cols):
    if col in df.columns and i < len(axes):
        sns.boxplot(x='target', y=col, data=df, ax=axes[i], palette=['lightgreen', 'salmon'])
        axes[i].set_title(f'{col} vs Cible')
        axes[i].set_xlabel('Cible (0 = Pas maladie, 1 = Maladie)')
        axes[i].set_ylabel(col)

# Supprimer les sous-graphiques vides
for j in range(len(numeric_cols), len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.show()

# ====================================================================
# 8. MATRICE DE CORRÉLATION
# ====================================================================

print("\n" + "="*60)
print("MATRICE DE CORRÉLATION")
print("="*60)

# Calcul de la corrélation
numeric_df = df[numeric_cols + ['target']].copy()
correlation_matrix = numeric_df.corr()

print("\n📊 Corrélations avec la cible:")
print(correlation_matrix['target'].sort_values(ascending=False))

# Visualisation de la matrice de corrélation
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f', 
            square=True, linewidths=0.5)
plt.title('Matrice de corrélation des variables numériques')
plt.tight_layout()
plt.show()

# ====================================================================
# 9. PRÉTRAITEMENT DES DONNÉES
# ====================================================================

print("\n" + "="*60)
print("PRÉTRAITEMENT DES DONNÉES")
print("="*60)

# Séparation des features et de la target
X = df.drop(['id', 'num', 'target'], axis=1)
y = df['target']

print(f"\n📊 Features: {X.shape[1]} colonnes")
print(f"📊 Target: {y.shape[0]} échantillons")

# Identification des types de colonnes
numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()

print(f"\n📋 Colonnes numériques ({len(numeric_cols)}): {numeric_cols}")
print(f"📋 Colonnes catégorielles ({len(categorical_cols)}): {categorical_cols}")

# ====================================================================
# 9.1 Gestion des valeurs manquantes
# ====================================================================

print("\n" + "-"*40)
print("GESTION DES VALEURS MANQUANTES")
print("-"*40)

# Imputation numérique avec la médiane
num_imputer = SimpleImputer(strategy='median')
X[numeric_cols] = num_imputer.fit_transform(X[numeric_cols])
print(f"✅ Valeurs numériques imputées avec la médiane")

# Imputation catégorielle avec le mode
cat_imputer = SimpleImputer(strategy='most_frequent')
X[categorical_cols] = cat_imputer.fit_transform(X[categorical_cols])
print(f"✅ Valeurs catégorielles imputées avec le mode")

print(f"\n📊 Valeurs manquantes restantes: {X.isnull().sum().sum()}")

# ====================================================================
# 9.2 Encodage des variables catégorielles
# ====================================================================

print("\n" + "-"*40)
print("ENCODAGE DES VARIABLES CATÉGORIELLES")
print("-"*40)

label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    label_encoders[col] = le
    print(f"✅ {col}: {len(le.classes_)} catégories encodées")

print("\n📊 Aperçu des données après encodage:")
print(X.head())

# ====================================================================
# 9.3 Mise à l'échelle des caractéristiques
# ====================================================================

print("\n" + "-"*40)
print("MISE À L'ÉCHELLE DES CARACTÉRISTIQUES")
print("-"*40)

scaler = StandardScaler()
X_scaled = pd.DataFrame(
    scaler.fit_transform(X),
    columns=X.columns
)

print("✅ Standardisation terminée")
print(f"\n📊 Statistiques après scaling:")
print(f"Moyennes: {X_scaled.mean().round(3)}")
print(f"Écarts-types: {X_scaled.std().round(3)}")

# ====================================================================
# 10. DIVISION DES DONNÉES
# ====================================================================

print("\n" + "="*60)
print("DIVISION DES DONNÉES")
print("="*60)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.3, random_state=42, stratify=y
)

print(f"\n📊 Taille de l'ensemble d'entraînement: {X_train.shape[0]} échantillons")
print(f"📊 Taille de l'ensemble de test: {X_test.shape[0]} échantillons")
print(f"\n📈 Distribution des classes - Entraînement:")
print(y_train.value_counts())
print(f"\n📈 Distribution des classes - Test:")
print(y_test.value_counts())

# ====================================================================
# 11. ENTRAÎNEMENT DU MODÈLE
# ====================================================================

print("\n" + "="*60)
print("ENTRAÎNEMENT DU MODÈLE")
print("="*60)

# Création du modèle
model = LogisticRegression(
    max_iter=1000, 
    random_state=42,
    class_weight='balanced'  # Pour gérer le déséquilibre
)

print("\n🔧 Paramètres du modèle:")
print(f"   • Max iterations: {model.max_iter}")
print(f"   • Class weight: {model.class_weight}")
print(f"   • Random state: {model.random_state}")

# Entraînement
model.fit(X_train, y_train)
print(f"\n✅ Modèle entraîné en {model.n_iter_[0]} itérations")

# Prédictions
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)
y_train_proba = model.predict_proba(X_train)
y_test_proba = model.predict_proba(X_test)

# ====================================================================
# 12. ÉVALUATION DU MODÈLE
# ====================================================================

print("\n" + "="*60)
print("ÉVALUATION DU MODÈLE")
print("="*60)

# Fonction d'évaluation
def evaluate_model(y_true, y_pred, dataset_name="Test"):
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    
    print(f"\n📊 {dataset_name}:")
    print("-"*40)
    print(f"✅ Exactitude (Accuracy):  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"🎯 Précision (Precision):  {precision:.4f} ({precision*100:.2f}%)")
    print(f"📈 Rappel (Recall):        {recall:.4f} ({recall*100:.2f}%)")
    print(f"⚖️ Score F1:               {f1:.4f} ({f1*100:.2f}%)")
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1
    }

# Évaluation
train_metrics = evaluate_model(y_train, y_train_pred, "Ensemble d'entraînement")
test_metrics = evaluate_model(y_test, y_test_pred, "Ensemble de test")

# ====================================================================
# 13. RAPPORT DE CLASSIFICATION
# ====================================================================

print("\n" + "="*60)
print("RAPPORT DE CLASSIFICATION")
print("="*60)

print("\n📋 Rapport détaillé - Ensemble de Test:")
print("-"*50)
print(classification_report(y_test, y_test_pred, target_names=['Pas de maladie', 'Maladie']))

# ====================================================================
# 14. MATRICE DE CONFUSION
# ====================================================================

print("\n" + "="*60)
print("MATRICE DE CONFUSION")
print("="*60)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

def plot_confusion_matrix(y_true, y_pred, ax, title):
    cm = confusion_matrix(y_true, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                xticklabels=['Pas de maladie', 'Maladie'],
                yticklabels=['Pas de maladie', 'Maladie'],
                cbar=False)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel('Prédit', fontsize=12)
    ax.set_ylabel('Réel', fontsize=12)
    
    # Ajout des pourcentages
    cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j+0.5, i+1.1, f'({cm_norm[i,j]:.1%})', 
                   ha='center', va='center', color='black', fontsize=10)

plot_confusion_matrix(y_test, y_test_pred, axes[0], 'Matrice de Confusion - Test')
plot_confusion_matrix(y_train, y_train_pred, axes[1], 'Matrice de Confusion - Entraînement')

plt.tight_layout()
plt.show()

# ====================================================================
# 15. COURBE ROC ET AUC
# ====================================================================

print("\n" + "="*60)
print("COURBE ROC ET AUC")
print("="*60)

# Calcul de la courbe ROC
fpr, tpr, thresholds = roc_curve(y_test, y_test_proba[:, 1])
roc_auc = auc(fpr, tpr)

print(f"\n📊 AUC (Area Under Curve): {roc_auc:.4f}")

# Visualisation
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC (AUC = {roc_auc:.4f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Aléatoire (AUC = 0.5)')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Taux de faux positifs (FPR)', fontsize=12)
plt.ylabel('Taux de vrais positifs (TPR)', fontsize=12)
plt.title('Courbe ROC - Régression Logistique', fontsize=14, fontweight='bold')
plt.legend(loc="lower right")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# ====================================================================
# 16. IMPORTANCE DES CARACTÉRISTIQUES
# ====================================================================

print("\n" + "="*60)
print("IMPORTANCE DES CARACTÉRISTIQUES")
print("="*60)

coef_df = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': model.coef_[0],
    'Abs_Coefficient': np.abs(model.coef_[0])
}).sort_values('Abs_Coefficient', ascending=False)

print("\n📊 Top 10 caractéristiques les plus importantes:")
print(coef_df.head(10).to_string(index=False))

# Visualisation des coefficients
plt.figure(figsize=(12, 8))
colors = ['green' if c > 0 else 'red' for c in coef_df['Coefficient']]
plt.barh(coef_df['Feature'], coef_df['Coefficient'], color=colors, alpha=0.7)
plt.xlabel('Coefficient', fontsize=12)
plt.ylabel('Caractéristique', fontsize=12)
plt.title('Coefficients du modèle de régression logistique', fontsize=14, fontweight='bold')
plt.axvline(x=0, color='black', linestyle='--', alpha=0.3)
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.show()

# ====================================================================
# 17. DISTRIBUTION DES PROBABILITÉS PRÉDITES
# ====================================================================

print("\n" + "="*60)
print("DISTRIBUTION DES PROBABILITÉS PRÉDITES")
print("="*60)

# Probabilités pour l'ensemble de test
test_proba_positive = y_test_proba[:, 1]

plt.figure(figsize=(10, 6))
plt.hist(test_proba_positive[y_test==0], bins=30, alpha=0.7, 
         label='Pas de maladie (Classe 0)', color='blue', edgecolor='black')
plt.hist(test_proba_positive[y_test==1], bins=30, alpha=0.7, 
         label='Maladie (Classe 1)', color='red', edgecolor='black')
plt.xlabel('Probabilité de maladie', fontsize=12)
plt.ylabel('Fréquence', fontsize=12)
plt.title('Distribution des probabilités prédites - Ensemble de Test', fontsize=14, fontweight='bold')
plt.legend()
plt.axvline(x=0.5, color='black', linestyle='--', linewidth=2, alpha=0.5)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# ====================================================================
# 18. STATISTIQUES DÉTAILLÉES DE PERFORMANCE
# ====================================================================

print("\n" + "="*60)
print("STATISTIQUES DÉTAILLÉES")
print("="*60)

# Calcul des métriques supplémentaires
tn, fp, fn, tp = confusion_matrix(y_test, y_test_pred).ravel()

print(f"\n📊 Matrice de confusion - Test:")
print(f"   • Vrais négatifs (TN): {tn}")
print(f"   • Faux positifs (FP): {fp}")
print(f"   • Faux négatifs (FN): {fn}")
print(f"   • Vrais positifs (TP): {tp}")

# Métriques supplémentaires
specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
negative_predictive_value = tn / (tn + fn) if (tn + fn) > 0 else 0
balanced_accuracy = (test_metrics['recall'] + specificity) / 2

print(f"\n📈 Métriques supplémentaires:")
print(f"   • Spécificité: {specificity:.4f} ({specificity*100:.2f}%)")
print(f"   • Valeur prédictive négative: {negative_predictive_value:.4f} ({negative_predictive_value*100:.2f}%)")
print(f"   • Balanced Accuracy: {balanced_accuracy:.4f} ({balanced_accuracy*100:.2f}%)")

# ====================================================================
# 19. CONCLUSION
# ====================================================================

print("\n" + "="*60)
print("📈 CONCLUSION FINALE")
print("="*60)

print(f"""
📊 RÉSULTATS DU MODÈLE DE RÉGRESSION LOGISTIQUE:

   PERFORMANCES GÉNÉRALES:
   • Exactitude:  {test_metrics['accuracy']:.4f} ({test_metrics['accuracy']*100:.2f}%)
   • Précision:   {test_metrics['precision']:.4f} ({test_metrics['precision']*100:.2f}%)
   • Rappel:      {test_metrics['recall']:.4f} ({test_metrics['recall']*100:.2f}%)
   • Score F1:    {test_metrics['f1_score']:.4f} ({test_metrics['f1_score']*100:.2f}%)
   • AUC:         {roc_auc:.4f} ({roc_auc*100:.2f}%)

   PRINCIPALES CARACTÉRISTIQUES PRÉDICTIVES:
   1. {coef_df.iloc[0]['Feature']} (coef: {coef_df.iloc[0]['Coefficient']:.3f})
   2. {coef_df.iloc[1]['Feature']} (coef: {coef_df.iloc[1]['Coefficient']:.3f})
   3. {coef_df.iloc[2]['Feature']} (coef: {coef_df.iloc[2]['Coefficient']:.3f})
   4. {coef_df.iloc[3]['Feature']} (coef: {coef_df.iloc[3]['Coefficient']:.3f})
   5. {coef_df.iloc[4]['Feature']} (coef: {coef_df.iloc[4]['Coefficient']:.3f})

   ANALYSE:
   • Le modèle montre de bonnes performances avec une exactitude de {test_metrics['accuracy']*100:.1f}%
   • Le score F1 de {test_metrics['f1_score']*100:.1f}% indique un bon équilibre entre précision et rappel
   • L'AUC de {roc_auc*100:.1f}% confirme la bonne capacité discriminante du modèle
   • Les caractéristiques les plus influentes sont liées aux paramètres cardiaques
   • Le modèle identifie correctement les patients à risque

   PERSPECTIVES D'AMÉLIORATION:
   • Tester d'autres algorithmes (Random Forest, XGBoost, SVM)
   • Optimiser les hyperparamètres avec GridSearchCV
   • Ajouter des interactions entre variables
   • Utiliser la validation croisée pour plus de robustesse
   • Intégrer des techniques de sélection de features
   • Explorer l'utilisation de réseaux de neurones
""")

print("="*60)
print("✅ PROJET TERMINÉ AVEC SUCCÈS")
print("="*60)