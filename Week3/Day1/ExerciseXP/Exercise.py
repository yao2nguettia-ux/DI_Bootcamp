import numpy as np

# Exercice 1
print(np.arange(10))

# Exercice 2
print(np.array([3.14, 2.17, 0, 1, 2]).astype(int))

# Exercice 3
print(np.arange(1, 10).reshape(3, 3))

# Exercice 4
print(np.random.rand(4, 5))

# Exercice 5
arr5 = np.array([[21,22,23,22,22],[20,21,22,23,24],[21,22,23,22,22]])
print(arr5[1])

# Exercice 6
arr6 = np.array([0,1,2,3,4,5,6,7,8,9])
print(arr6[::-1])

# Exercice 7
print(np.eye(4))

# Exercice 8
arr8 = np.arange(10)
print(f"Sum: {arr8.sum()}, Average: {arr8.mean()}")

# Exercice 9
print(np.arange(1, 21).reshape(4, 5))

# Exercice 10
arr10 = np.array([1,2,3,4,5,6,7,8,9,10])
print(arr10[arr10 % 2 == 1])