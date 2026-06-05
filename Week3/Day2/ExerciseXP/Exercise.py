import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Exercice 1

A = np.array([[2, 1, 1], [4, -6, 0], [-2, 7, 2]])
det = np.linalg.det(A)
inv = np.linalg.inv(A) if det != 0 else None
print(f"Déterminant : {det:.4f}")
if inv is not None:
    print(f"Inverse :\n{inv}")

# Exercice 2

data = np.random.randint(1, 100, 50)
print(f"Moyenne : {np.mean(data):.2f}")
print(f"Médiane : {np.median(data):.2f}")
print(f"Écart-type : {np.std(data):.2f}")

# Exercice 3

dates = np.array([datetime(2023, 1, 1) + timedelta(days=i) for i in range(31)])
formatted = np.array([d.strftime("%Y/%m/%d") for d in dates])
print(formatted[:3])

# Exercice 4

df = pd.DataFrame(np.random.randint(0, 100, (10, 4)), columns=['A','B','C','D'])
print(df[df['A'] > 50])
print("Somme :\n", df.sum())
print("Moyenne :\n", df.mean())

# Exercice 5

img = np.random.randint(0, 256, (5, 5))
print("Image 5x5 (niveaux de gris) :\n", img)
plt.imshow(img, cmap='gray')
plt.title("Image 5x5")
plt.show()

# Exercice 6

np.random.seed(123)
before = np.random.normal(50, 10, 30)
after = before + np.random.normal(5, 3, 30)
diff = after - before
t = np.mean(diff) / (np.std(diff, ddof=1) / np.sqrt(30))
print(f"Statistique t = {t:.3f}")
if t > 1.699:
    print("Amélioration significative.")
else:
    print("Pas d'amélioration significative.")

# Exercice 7

a = np.array([5, 8, 12, 3, 7])
b = np.array([4, 9, 10, 5, 6])
print(a > b)

# Exercice 8
dates = pd.date_range('2023-01-01', '2023-12-31')
values = np.random.randn(len(dates))
ts = pd.Series(values, index=dates)
q1 = ts['2023-01':'2023-03']
q2 = ts['2023-04':'2023-06']
q3 = ts['2023-07':'2023-09']
q4 = ts['2023-10':'2023-12']
print(f"Q1: {len(q1)} jours, Q2: {len(q2)}, Q3: {len(q3)}, Q4: {len(q4)}")

# Exercice 9
arr = np.array([[1,2,3],[4,5,6]])
df2 = pd.DataFrame(arr, columns=['X','Y','Z'])
arr2 = df2.to_numpy()
print("NumPy -> DataFrame :\n", df2)
print("DataFrame -> NumPy :\n", arr2)

# Exercice 10
x = np.arange(100)
y = np.random.randn(100).cumsum()
plt.plot(x, y)
plt.title("Graphique linéaire")
plt.show()