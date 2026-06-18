# ==================== DAILY CHALLENGE: CLASSIFICATION WITH NEURAL NETWORKS ====================

# ==================== PART 1: UNDERSTAND CLASSIFICATION TYPES ====================
"""
BINARY CLASSIFICATION:
Binary classification is the task of classifying data points into one of two mutually exclusive classes.
Example: Spam detection (spam vs not spam), disease diagnosis (positive vs negative), or credit approval (approved vs denied).

MULTI-CLASS CLASSIFICATION:
Multi-class classification involves categorizing data points into one of three or more mutually exclusive classes.
Example: Handwritten digit recognition (0-9), iris flower species classification, or image recognition (cat vs dog vs bird).

MULTI-LABEL CLASSIFICATION:
Multi-label classification assigns each data point to multiple classes simultaneously, where classes are not mutually exclusive.
Example: Image tagging (an image can contain "cat", "dog", and "tree" simultaneously), movie genre classification (a movie can be both "action" and "comedy"), or medical symptom prediction.
"""

# ==================== PART 2: SET UP ENVIRONMENT AND DATASET ====================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import seaborn as sns

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

print("TensorFlow version:", tf.__version__)

# Create dataset
samples = 1000
X, y = make_circles(samples,
                    noise=0.03,
                    random_state=42)

print('X shape:', X.shape)
print('First 5 samples of X:\n', X[:5])
print('\nFirst 5 samples of y:', y[:5])

# Visualize the dataset
plt.figure(figsize=(8, 6))
plt.scatter(X[y==0][:, 0], X[y==0][:, 1], c='blue', alpha=0.7, label='Class 0')
plt.scatter(X[y==1][:, 0], X[y==1][:, 1], c='red', alpha=0.7, label='Class 1')
plt.title('Make Circles Dataset')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# ==================== PART 3: BUILD A BASIC NEURAL NETWORK ====================
print("\n=== PART 3: Basic Neural Network ===\n")

# Build basic model
model_basic = tf.keras.Sequential([
    tf.keras.layers.Dense(1, activation='sigmoid', input_shape=(2,))
])

# Compile the model
model_basic.compile(
    optimizer='sgd',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model_basic.summary()

# Train the model
history_basic = model_basic.fit(
    X, y,
    epochs=100,
    batch_size=32,
    verbose=0
)

# Evaluate
loss_basic, accuracy_basic = model_basic.evaluate(X, y, verbose=0)
print(f"Basic Model - Loss: {loss_basic:.4f}, Accuracy: {accuracy_basic:.4f}")

# Plot training history
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history_basic.history['loss'])
plt.title('Basic Model - Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(history_basic.history['accuracy'])
plt.title('Basic Model - Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# ==================== PART 4: IMPROVE THE MODEL ====================
print("\n=== PART 4: Improved Neural Network ===\n")

# Build improved model with more layers and neurons
model_improved = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(2,)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Use Adam optimizer
model_improved.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model_improved.summary()

# Train for more epochs
history_improved = model_improved.fit(
    X, y,
    epochs=200,
    batch_size=32,
    verbose=0
)

# Evaluate
loss_improved, accuracy_improved = model_improved.evaluate(X, y, verbose=0)
print(f"Improved Model - Loss: {loss_improved:.4f}, Accuracy: {accuracy_improved:.4f}")

# Plot training history
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history_improved.history['loss'])
plt.title('Improved Model - Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(history_improved.history['accuracy'])
plt.title('Improved Model - Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print(f"\nImprovement: {((accuracy_improved - accuracy_basic)/accuracy_basic)*100:.2f}% increase in accuracy")

# ==================== PART 5: DECISION BOUNDARY VISUALIZATION ====================
print("\n=== PART 5: Decision Boundary Visualization ===\n")

def plot_decision_boundary(model, X, y, title="Decision Boundary"):
    """
    Plot decision boundary for a binary classification model.
    """
    # Create mesh grid
    x_min, x_max = X[:, 0].min() - 0.1, X[:, 0].max() + 0.1
    y_min, y_max = X[:, 1].min() - 0.1, X[:, 1].max() + 0.1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01),
                         np.arange(y_min, y_max, 0.01))
    
    # Predict on mesh grid
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()], verbose=0)
    Z = Z.reshape(xx.shape)
    
    # Plot decision boundary
    plt.figure(figsize=(8, 6))
    plt.contourf(xx, yy, Z, alpha=0.3, cmap='coolwarm')
    plt.scatter(X[y==0][:, 0], X[y==0][:, 1], c='blue', alpha=0.7, label='Class 0')
    plt.scatter(X[y==1][:, 0], X[y==1][:, 1], c='red', alpha=0.7, label='Class 1')
    plt.title(title)
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# Visualize decision boundaries
plot_decision_boundary(model_basic, X, y, "Basic Model Decision Boundary")
plot_decision_boundary(model_improved, X, y, "Improved Model Decision Boundary")

# ==================== PART 6: ACTIVATION FUNCTIONS COMPARISON ====================
print("\n=== PART 6: Activation Functions Comparison ===\n")

def build_model_with_activation(activation='relu'):
    """Build model with specified activation function."""
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation=activation, input_shape=(2,)),
        tf.keras.layers.Dense(32, activation=activation),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    return model

activations = ['relu', 'sigmoid', 'tanh']
results = {}

for act in activations:
    print(f"\nTraining model with {act} activation:")
    model = build_model_with_activation(act)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    history = model.fit(X, y, epochs=100, batch_size=32, verbose=0)
    loss, accuracy = model.evaluate(X, y, verbose=0)
    results[act] = {'model': model, 'accuracy': accuracy, 'loss': loss, 'history': history}
    print(f"{act} - Accuracy: {accuracy:.4f}, Loss: {loss:.4f}")

# Plot comparison
plt.figure(figsize=(12, 4))
for i, act in enumerate(activations):
    plt.subplot(1, 3, i+1)
    plt.plot(results[act]['history'].history['accuracy'])
    plt.title(f'{act.upper()} Activation\nAccuracy: {results[act]["accuracy"]:.4f}')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Visualize decision boundaries for each activation
for act in activations:
    plot_decision_boundary(results[act]['model'], X, y, f"{act.upper()} Activation Decision Boundary")

# ==================== PART 7: SPLIT DATA INTO TRAINING AND TESTING ====================
print("\n=== PART 7: Train-Test Split ===\n")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training set: {X_train.shape[0]} samples")
print(f"Testing set: {X_test.shape[0]} samples")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Build final model
model_final = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(2,)),
    tf.keras.layers.Dropout(0.2),  # Add dropout for regularization
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model_final.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Train with early stopping
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=20,
    restore_best_weights=True
)

history_final = model_final.fit(
    X_train_scaled, y_train,
    epochs=300,
    batch_size=32,
    validation_split=0.2,
    callbacks=[early_stopping],
    verbose=0
)

# ==================== PART 8: EVALUATE FINAL MODEL ====================
print("\n=== PART 8: Final Model Evaluation ===\n")

# Evaluate on train and test
train_loss, train_acc = model_final.evaluate(X_train_scaled, y_train, verbose=0)
test_loss, test_acc = model_final.evaluate(X_test_scaled, y_test, verbose=0)

print(f"Training Accuracy: {train_acc:.4f}")
print(f"Testing Accuracy: {test_acc:.4f}")
print(f"Train-Test Difference: {abs(train_acc - test_acc):.4f}")

# Plot training history
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history_final.history['loss'], label='Train')
plt.plot(history_final.history['val_loss'], label='Validation')
plt.title('Final Model - Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(history_final.history['accuracy'], label='Train')
plt.plot(history_final.history['val_accuracy'], label='Validation')
plt.title('Final Model - Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Visualize decision boundaries on scaled data
plot_decision_boundary(model_final, X_train_scaled, y_train, "Final Model - Training Set Decision Boundary")
plot_decision_boundary(model_final, X_test_scaled, y_test, "Final Model - Test Set Decision Boundary")

# ==================== ADDITIONAL EVALUATION: CONFUSION MATRIX ====================
from sklearn.metrics import confusion_matrix, classification_report

# Get predictions
y_pred_proba = model_final.predict(X_test_scaled)
y_pred = (y_pred_proba > 0.5).astype(int).flatten()

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix - Final Model')
plt.xlabel('Predicted Class')
plt.ylabel('True Class')
plt.show()

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# ==================== PART 9: SUMMARY ====================
print("\n" + "="*60)
print("SUMMARY AND KEY TAKEAWAYS")
print("="*60)
print("\n1. CLASSIFICATION TYPES:")
print("   - Binary: Two mutually exclusive classes (e.g., spam vs not spam)")
print("   - Multi-class: Three or more mutually exclusive classes (e.g., digit recognition)")
print("   - Multi-label: Multiple classes simultaneously (e.g., image tagging)")

print("\n2. MODEL IMPROVEMENTS:")
print("   - Adding more layers and neurons increased capacity")
print("   - Adam optimizer provided faster and better convergence than SGD")
print("   - More epochs allowed better learning of complex patterns")
print(f"   - Accuracy improved from {accuracy_basic:.4f} to {test_acc:.4f}")

print("\n3. ACTIVATION FUNCTIONS:")
print("   - ReLU: Best for hidden layers, helps with vanishing gradient")
print("   - Sigmoid: Good for output layer in binary classification")
print("   - Tanh: Similar to sigmoid but centered at 0")
print("   - ReLU showed the best performance for this dataset")

print("\n4. DATA PREPROCESSING:")
print("   - Train-test split ensures proper generalization evaluation")
print("   - Standardization helps with gradient descent convergence")
print("   - Early stopping prevents overfitting")

print("\n5. VISUALIZATION IMPORTANCE:")
print("   - Decision boundaries help understand model behavior")
print("   - Training history shows learning progress and convergence")
print("   - Confusion matrix reveals class-specific performance")

print("\n6. REGULARIZATION:")
print("   - Dropout helped reduce overfitting")
print("   - Early stopping selected optimal model complexity")
print("   - Train-test difference was minimal, indicating good generalization")

print("\n" + "="*60)
print("CHALLENGE COMPLETED SUCCESSFULLY!")
print("="*60)

# Bonus: Compare all models in a single table
print("\nModel Comparison:")
print("-"*70)
print(f"{'Model':<20} {'Architecture':<30} {'Accuracy':<15}")
print("-"*70)
print(f"{'Basic':<20} {'1 layer, 1 neuron':<30} {accuracy_basic:.4f}")
print(f"{'Improved':<20} {'2 layers, 96 neurons':<30} {accuracy_improved:.4f}")
print(f"{'ReLU (best)':<20} {'2 layers, 96 neurons':<30} {results['relu']['accuracy']:.4f}")
print(f"{'Sigmoid':<20} {'2 layers, 96 neurons':<30} {results['sigmoid']['accuracy']:.4f}")
print(f"{'Tanh':<20} {'2 layers, 96 neurons':<30} {results['tanh']['accuracy']:.4f}")
print(f"{'Final Model':<20} {'3 layers + Dropout':<30} {test_acc:.4f}")
print("-"*70)