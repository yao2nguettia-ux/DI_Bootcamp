# ==================== EXERCICE 2 ====================
from typing import Tuple

W_TEMP = 0.6
W_RAIN = 0.4
BIAS   = 2.0

def step_activation(s: float, threshold: float = 20.0) -> int:
    return 1 if s > threshold else 0

def weighted_sum(temperature_f: float, rain01: int) -> float:
    return temperature_f * W_TEMP + rain01 * W_RAIN + BIAS

case1 = (70, 0)
case2 = (50, 1)

s1 = weighted_sum(*case1)
s2 = weighted_sum(*case2)
y1 = step_activation(s1)
y2 = step_activation(s2)

print({"case1": {"sum": s1, "decision": y1}, "case2": {"sum": s2, "decision": y2}})


# ==================== EXERCICE 3 ====================
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import mnist

print("TensorFlow:", tf.__version__)

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.astype("float32") / 255.0
x_test  = x_test.astype("float32") / 255.0

print("Train shape:", x_train.shape, "Test shape:", x_test.shape)

y_train_oh = to_categorical(y_train, num_classes=10)
y_test_oh = to_categorical(y_test, num_classes=10)

print("Labels one-hot:", y_train_oh.shape, y_test_oh.shape)

model = models.Sequential([
    layers.Flatten(input_shape=(28, 28)),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax'),
])

model.summary()

model.compile(optimizer='adam', 
              loss='categorical_crossentropy', 
              metrics=['accuracy'])

history = model.fit(x_train, y_train_oh, 
                    epochs=5, 
                    batch_size=128, 
                    validation_split=0.1, 
                    verbose=1)

test_loss, test_acc = model.evaluate(x_test, y_test_oh, verbose=0)
print({"test_loss": float(test_loss), "test_acc": float(test_acc)})


# ==================== EXERCICE 4 ====================
x1, x2 = 2000.0, 3.0
w1, w2 = 0.5, 0.7
b = 50000.0

z = x1*w1 + x2*w2 + b
y = max(0, z)

print({"z": z, "prediction": y})


# ==================== EXERCICE 5 (OPTIONNEL) ====================
import numpy as np

x = np.array([4, 80])
w = np.array([0.6, 0.3])
b = 10

def forward_propagation(x, w, b):
    z = np.dot(x, w) + b
    return z

y_pred = forward_propagation(x, w, b)
y_true = 85

loss = 0.5 * (y_true - y_pred) ** 2

grad_w = -(y_true - y_pred) * x
grad_b = -(y_true - y_pred)

learning_rate = 0.01
w_new = w - learning_rate * grad_w
b_new = b - learning_rate * grad_b

print("Initial Prediction:", y_pred)
print("Loss:", loss)
print("Gradients w:", grad_w)
print("Gradient b:", grad_b)
print("Updated Weights:", w_new)
print("Updated Bias:", b_new)

# Modification avec différents taux d'apprentissage
print("\n--- Avec learning_rate = 0.001 ---")
lr_small = 0.001
w_small = w - lr_small * grad_w
b_small = b - lr_small * grad_b
print("Weights:", w_small)
print("Bias:", b_small)

print("\n--- Avec learning_rate = 0.1 ---")
lr_large = 0.1
w_large = w - lr_large * grad_w
b_large = b - lr_large * grad_b
print("Weights:", w_large)
print("Bias:", b_large)


# ==================== EXERCICE 6 (OPTIONNEL) ====================
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0
y_train_oh = to_categorical(y_train, num_classes=10)
y_test_oh = to_categorical(y_test, num_classes=10)

model = models.Sequential([
    layers.Flatten(input_shape=(28, 28)),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax'),
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train_oh, epochs=3, batch_size=128, verbose=0)

n_samples = 12
idx = np.random.choice(len(x_test), size=n_samples, replace=False)
x_vis = x_test[idx]
y_true = y_test[idx]

y_prob = model.predict(x_vis)
y_pred = np.argmax(y_prob, axis=1)

cols = 6
rows = int(np.ceil(len(idx)/cols))
plt.figure(figsize=(12, 2*rows))
for i, k in enumerate(idx, 1):
    plt.subplot(rows, cols, i)
    plt.imshow(x_test[k], cmap="gray")
    confidence = np.max(y_prob[i-1]) * 100
    plt.title(f"pred={y_pred[i-1]} (conf: {confidence:.1f}%)\ntrue={y_true[i-1]}")
    plt.axis("off")
plt.tight_layout()
plt.show()