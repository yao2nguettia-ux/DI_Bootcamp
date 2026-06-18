# ==================== DÉFI QUOTIDIEN : MNIST ====================

# ==================== ÉTAPE 1 : Charger et prétraiter MNIST ====================
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import layers, models
from sklearn.metrics import confusion_matrix, classification_report

print("=== ÉTAPE 1 : Chargement et prétraitement de MNIST ===\n")

# Charger le jeu de données
(x_train, y_train), (x_test, y_test) = mnist.load_data()

print(f"Données d'entraînement : {x_train.shape}")
print(f"Données de test : {x_test.shape}")
print(f"Étiquettes d'entraînement : {y_train.shape}")
print(f"Étiquettes de test : {y_test.shape}")

# Normaliser les valeurs des pixels entre 0 et 1
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

# Convertir les étiquettes au format one-hot
y_train_oh = to_categorical(y_train, num_classes=10)
y_test_oh = to_categorical(y_test, num_classes=10)

print(f"\nÉtiquettes one-hot : {y_train_oh.shape}")

# Afficher des exemples d'images
plt.figure(figsize=(12, 4))
for i in range(10):
    plt.subplot(2, 5, i + 1)
    plt.imshow(x_train[i], cmap="gray")
    plt.title(f"Label: {y_train[i]}")
    plt.axis("off")
plt.suptitle("Exemples d'images MNIST avec leurs étiquettes")
plt.tight_layout()
plt.show()


# ==================== ÉTAPE 2 : Construire le réseau neuronal ====================
print("\n=== ÉTAPE 2 : Construction du réseau neuronal ===\n")

model = models.Sequential([
    layers.Flatten(input_shape=(28, 28), name="flatten"),
    layers.Dense(128, activation='relu', name="hidden_1"),
    layers.Dense(64, activation='relu', name="hidden_2"),
    layers.Dense(10, activation='softmax', name="output")
])

model.summary()

# Compiler le modèle
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("\nModèle compilé avec succès!")


# ==================== ÉTAPE 3 : Entraîner le réseau neuronal ====================
print("\n=== ÉTAPE 3 : Entraînement du réseau neuronal ===\n")

history = model.fit(
    x_train, y_train_oh,
    epochs=10,
    batch_size=128,
    validation_split=0.1,
    verbose=1
)

# Visualiser les tendances d'entraînement
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Entraînement')
plt.plot(history.history['val_loss'], label='Validation')
plt.title('Évolution de la perte')
plt.xlabel('Époques')
plt.ylabel('Perte')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Entraînement')
plt.plot(history.history['val_accuracy'], label='Validation')
plt.title('Évolution de la précision')
plt.xlabel('Époques')
plt.ylabel('Précision')
plt.legend()

plt.tight_layout()
plt.show()


# ==================== ÉTAPE 4 : Évaluer les performances ====================
print("\n=== ÉTAPE 4 : Évaluation des performances ===\n")

# Calculer la précision sur l'ensemble de test
test_loss, test_accuracy = model.evaluate(x_test, y_test_oh, verbose=0)
print(f"Précision sur l'ensemble de test : {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
print(f"Perte sur l'ensemble de test : {test_loss:.4f}")

# Faire des prédictions
y_pred_proba = model.predict(x_test)
y_pred = np.argmax(y_pred_proba, axis=1)

# Afficher la matrice de confusion
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=range(10), yticklabels=range(10))
plt.title('Matrice de confusion - Classification des chiffres MNIST')
plt.xlabel('Prédictions')
plt.ylabel('Vraies étiquettes')
plt.show()

# Rapport de classification
print("\nRapport de classification :")
print(classification_report(y_test, y_pred))

# Identifier les chiffres avec lesquels le modèle a le plus de difficultés
class_accuracy = []
for i in range(10):
    mask = (y_test == i)
    acc = np.mean(y_pred[mask] == y_test[mask])
    class_accuracy.append(acc)
    print(f"Chiffre {i} : Précision = {acc:.4f} ({acc*100:.2f}%)")

# Afficher les pires performances
worst_classes = np.argsort(class_accuracy)[:3]
print(f"\nLes chiffres les plus difficiles à classifier : {worst_classes}")


# ==================== EXTRA : Visualiser les erreurs ====================
print("\n=== EXTRA : Visualisation des erreurs ===\n")

# Trouver les indices des erreurs
errors = np.where(y_pred != y_test)[0]
n_errors = min(20, len(errors))

if len(errors) > 0:
    plt.figure(figsize=(15, 6))
    for i, idx in enumerate(np.random.choice(errors, size=n_errors, replace=False)):
        plt.subplot(2, 10, i + 1)
        plt.imshow(x_test[idx], cmap="gray")
        plt.title(f"Vrai: {y_test[idx]}\nPrédit: {y_pred[idx]}")
        plt.axis("off")
    plt.suptitle("Exemples d'images mal classifiées")
    plt.tight_layout()
    plt.show()
else:
    print("Aucune erreur trouvée!")

# Afficher les prédictions avec leurs probabilités
print("\nExemples de prédictions avec probabilités :")
sample_indices = np.random.choice(len(x_test), size=5, replace=False)
for idx in sample_indices:
    probs = y_pred_proba[idx]
    pred_class = np.argmax(probs)
    print(f"Image {idx}: Vrai={y_test[idx]}, Prédit={pred_class}, "
          f"Confiance={probs[pred_class]*100:.2f}%")


# ==================== OPTIMISATION : Réglage des hyperparamètres ====================
print("\n=== OPTIMISATION : Réglage des hyperparamètres ===\n")

# Tester différentes architectures
def create_model(hidden_units=[128, 64], activation='relu', dropout_rate=0.0):
    model = models.Sequential()
    model.add(layers.Flatten(input_shape=(28, 28)))
    for units in hidden_units:
        model.add(layers.Dense(units, activation=activation))
        if dropout_rate > 0:
            model.add(layers.Dropout(dropout_rate))
    model.add(layers.Dense(10, activation='softmax'))
    return model

# Tester différents taux d'apprentissage
learning_rates = [0.001, 0.0005, 0.01]
results = []

print("Test de différents taux d'apprentissage :")
for lr in learning_rates:
    print(f"\nTaux d'apprentissage : {lr}")
    model_test = create_model()
    model_test.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    history_test = model_test.fit(x_train, y_train_oh, epochs=5, batch_size=128, 
                                  validation_split=0.1, verbose=0)
    val_acc = history_test.history['val_accuracy'][-1]
    results.append({"lr": lr, "val_accuracy": val_acc})
    print(f"Précision de validation : {val_acc:.4f}")

# Meilleur taux d'apprentissage
best_lr = max(results, key=lambda x: x['val_accuracy'])
print(f"\nMeilleur taux d'apprentissage : {best_lr['lr']} (précision: {best_lr['val_accuracy']:.4f})")

# Tester avec dropout pour réduire le surapprentissage
print("\nTest avec Dropout pour réduire le surapprentissage :")
dropout_rates = [0.0, 0.2, 0.5]

for dropout in dropout_rates:
    print(f"\nTaux de dropout : {dropout}")
    model_dropout = create_model(hidden_units=[128, 64], dropout_rate=dropout)
    model_dropout.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    history_dropout = model_dropout.fit(x_train, y_train_oh, epochs=5, batch_size=128,
                                        validation_split=0.1, verbose=0)
    val_acc = history_dropout.history['val_accuracy'][-1]
    print(f"Précision de validation : {val_acc:.4f}")

print("\n=== FIN DU DÉFI QUOTIDIEN ===")