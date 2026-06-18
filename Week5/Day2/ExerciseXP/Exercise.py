# ==================== EXERCISE 1: DEEP LEARNING VS TRADITIONAL ML ====================
# (Written answers - see markdown cells in notebook)

# ==================== EXERCISE 2: ARTIFICIAL NEURAL NETWORKS ====================
# (Written answers - see markdown cells in notebook)

# ==================== EXERCISE 3: CREATING THE DATASET ====================
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

# Set seed for reproducibility
np.random.seed(0)

# Create 20 points from -1 to <1 with step 0.1
x = np.arange(-1, 1, 0.1)
print("x shape:", x.shape)

# Generate y with noise: y = -x^2 + Gaussian noise (0, 0.05)
y = -x**2 + np.random.normal(0, 0.05, len(x))
print("y shape:", y.shape)

# Visualize the noisy dataset
plt.figure(figsize=(8, 5))
plt.scatter(x, y, color='blue', alpha=0.7, label='Noisy data')
plt.plot(x, -x**2, color='red', linestyle='--', label='True function y = -x²')
plt.title("Noisy dataset sampled from y = -x^2")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Split into train (first 12 points) and test (last 8 points)
x_train, y_train = x[:12], y[:12]
x_test, y_test = x[12:], y[12:]
print("train sizes:", x_train.shape, y_train.shape, "test sizes:", x_test.shape, y_test.shape)

# ==================== EXERCISE 4: FITTING POLYNOMIAL MODELS ====================
def polynomial_fit(degree: int):
    """Fit polynomial of given degree on training data and return callable polynomial."""
    coeffs = np.polyfit(x_train, y_train, degree)
    return np.poly1d(coeffs)

def plot_polyfit(degree: int):
    """Plot training data, test data, and fitted polynomial curve."""
    # Fit polynomial
    poly = polynomial_fit(degree)
    
    # Create a dense linspace over x range
    x_dense = np.linspace(-1, 1, 200)
    
    # Evaluate fitted polynomial
    y_dense = poly(x_dense)
    
    # Plot
    plt.figure(figsize=(8, 5))
    plt.scatter(x_train, y_train, color='blue', alpha=0.7, label='Training data')
    plt.scatter(x_test, y_test, color='green', alpha=0.7, label='Test data')
    plt.plot(x_dense, y_dense, color='red', linewidth=2, label=f'Degree {degree} polynomial')
    plt.plot(x_dense, -x_dense**2, color='black', linestyle='--', alpha=0.5, label='True function')
    
    # Calculate RMSE
    train_pred = poly(x_train)
    test_pred = poly(x_test)
    rmse_train = np.sqrt(mean_squared_error(y_train, train_pred))
    rmse_test = np.sqrt(mean_squared_error(y_test, test_pred))
    
    plt.title(f'Polynomial Degree {degree} (Train RMSE: {rmse_train:.4f}, Test RMSE: {rmse_test:.4f})')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    return rmse_train, rmse_test

# Visualize degrees 1, 7, and 11
print("\n=== Visualizing Polynomial Fits ===\n")
for degree in [1, 7, 11]:
    print(f"Degree {degree}:")
    rmse_train, rmse_test = plot_polyfit(degree)
    print(f"  Train RMSE: {rmse_train:.6f}")
    print(f"  Test RMSE: {rmse_test:.6f}\n")

# ==================== EXERCISE 5: CROSS-VALIDATION ====================
def rmse(y_true, y_pred):
    """Calculate Root Mean Squared Error."""
    return np.sqrt(np.mean((y_true - y_pred)**2))

# Compute RMSE for degrees 1 to 11
degrees = range(1, 12)
rows = []  # each row: (degree, rmse_train, rmse_test)

for d in degrees:
    # Fit on training data
    poly = polynomial_fit(d)
    
    # Evaluate on train and test
    train_pred = poly(x_train)
    test_pred = poly(x_test)
    
    rmse_train = rmse(y_train, train_pred)
    rmse_test = rmse(y_test, test_pred)
    
    rows.append((d, rmse_train, rmse_test))

# Display results
print("\n=== RMSE Results ===\n")
print("Degree | Train RMSE | Test RMSE")
print("-" * 40)
for row in rows:
    print(f"{row[0]:6d} | {row[1]:10.6f} | {row[2]:9.6f}")

# Plot RMSE curves
degs = [r[0] for r in rows]
rmse_tr = [r[1] for r in rows]
rmse_te = [r[2] for r in rows]

plt.figure(figsize=(10, 6))
plt.plot(degs, rmse_tr, label="Train RMSE", marker='o', linewidth=2, color='blue')
plt.plot(degs, rmse_te, label="Test RMSE", marker='s', linewidth=2, color='red')
plt.yscale("log")
plt.xlabel("Polynomial Degree", fontsize=12)
plt.ylabel("RMSE (log scale)", fontsize=12)
plt.title("RMSE vs Polynomial Degree", fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()

# Find optimal degree
optimal_idx = np.argmin(rmse_te)
optimal_degree = degs[optimal_idx]
optimal_rmse = rmse_te[optimal_idx]

print(f"\n=== Optimal Degree Analysis ===")
print(f"Optimal degree: {optimal_degree}")
print(f"Minimum Test RMSE: {optimal_rmse:.6f}")
print(f"True model is degree 2 (y = -x²)")
print(f"Degree 2 Test RMSE: {rows[1][2]:.6f}")

# Additional analysis: Show overfitting pattern
print("\n=== Overfitting Analysis ===")
for d in [1, 2, 3, 5, 7, 9, 11]:
    if d <= len(rows):
        print(f"Degree {d}: Train RMSE = {rows[d-1][1]:.6f}, Test RMSE = {rows[d-1][2]:.6f}, "
              f"Difference = {abs(rows[d-1][1] - rows[d-1][2]):.6f}")

# ==================== EXTRA: 5-FOLD CROSS-VALIDATION ====================
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline

print("\n=== 5-Fold Cross-Validation Analysis ===\n")

# Prepare full dataset
X_full = x.reshape(-1, 1)
y_full = y

cv_scores = []
for d in range(1, 12):
    # Create polynomial features pipeline
    model = make_pipeline(PolynomialFeatures(d), LinearRegression())
    # Perform 5-fold cross-validation
    scores = cross_val_score(model, X_full, y_full, cv=5, scoring='neg_mean_squared_error')
    rmse_cv = np.sqrt(-scores.mean())
    cv_scores.append((d, rmse_cv))
    print(f"Degree {d}: CV RMSE = {rmse_cv:.6f}")

# Find optimal degree using CV
optimal_cv_idx = np.argmin([score[1] for score in cv_scores])
optimal_cv_degree = cv_scores[optimal_cv_idx][0]
optimal_cv_rmse = cv_scores[optimal_cv_idx][1]

print(f"\nOptimal degree using cross-validation: {optimal_cv_degree}")
print(f"Minimum CV RMSE: {optimal_cv_rmse:.6f}")

# ==================== FINAL SUMMARY ====================
print("\n" + "="*60)
print("FINAL SUMMARY")
print("="*60)
print(f"1. True underlying function: y = -x² (degree 2)")
print(f"2. Optimal polynomial degree (test set): {optimal_degree}")
print(f"3. Optimal polynomial degree (cross-validation): {optimal_cv_degree}")
print(f"4. Key insight: The optimal degree identifies the true model complexity")
print(f"   while balancing the bias-variance tradeoff.")
print("\nInterpretation:")
print("- Low degrees (1-2): High bias, underfitting the data")
print("- Optimal degree (~2-3): Best generalization, captures true pattern")
print("- High degrees (7+): High variance, overfitting the noise")
print("="*60)