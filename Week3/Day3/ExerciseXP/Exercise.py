import pandas as pd
import pip
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

import mplfinance as mpf
from scipy import stats

plt.style.use('seaborn-v0_8-darkgrid')

# Chargement des données
try:
    df = pd.read_csv('AAPL.csv')
except FileNotFoundError:
    print("AAPL.csv not found. Creating a dummy dataset.")
    # Create a dummy DataFrame if the file is not found
    dates = pd.date_range(start='2000-01-01', periods=1000, freq='D')
    np.random.seed(42)
    open_prices = np.random.rand(1000) * 100 + 100
    close_prices = open_prices + np.random.randn(1000) * 5
    high_prices = np.maximum(open_prices, close_prices) + np.random.rand(1000) * 2
    low_prices = np.minimum(open_prices, close_prices) - np.random.rand(1000) * 2
    volume = np.random.randint(1_000_000, 10_000_000, 1000)
    
    df = pd.DataFrame({
        'Date': dates,
        'Open': open_prices,
        'High': high_prices,
        'Low': low_prices,
        'Close': close_prices,
        'Adj Close': close_prices * (1 + np.random.rand(1000)*0.01),
        'Volume': volume
    })

df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
df.sort_index(inplace=True)

print("Aperçu des données :")
print(df.head())
print("\nValeurs manquantes :")
print(df.isnull().sum())
print("\nTypes de données :")
print(df.dtypes)
print(f"\nPériode : {df.index.min()} à {df.index.max()}")
print(f"Nombre de jours : {len(df)}")

# Visualisation
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
ax1.plot(df.index, df['Adj Close'], color='blue', linewidth=0.8)
ax1.set_ylabel('Cours ajusté (USD)')
ax1.set_title('AAPL - Cours de clôture ajusté')
ax2.bar(df.index, df['Volume'], color='green', alpha=0.6, width=1.5)
ax2.set_ylabel('Volume')
plt.tight_layout()
plt.show()

df_subset = df.loc[df.index.max() - pd.Timedelta(days=730):df.index.max()] # Use last 2 years for subset
mpf.plot(df_subset, type='candle', volume=True, style='charles',
         title='Graphique en chandeliers AAPL (Dernières 2 années)',
         ylabel='Prix (USD)', ylabel_lower='Volume')

# Statistiques descriptives
cols = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
print(df[cols].describe())
stats_desc = pd.DataFrame({
    'Moyenne': df[cols].mean(),
    'Médiane': df[cols].median(),
    'Écart-type': df[cols].std()
})
print(stats_desc)

# Moyennes mobiles
df['SMA_20'] = df['Adj Close'].rolling(20).mean()
df['SMA_50'] = df['Adj Close'].rolling(50).mean()

plt.figure(figsize=(12,6))
plt.plot(df.loc[df.index.max() - pd.Timedelta(days=1000):]['Adj Close'], label='Clôture', alpha=0.5) # Plot last 1000 days
plt.plot(df.loc[df.index.max() - pd.Timedelta(days=1000):]['SMA_20'], label='SMA20')
plt.plot(df.loc[df.index.max() - pd.Timedelta(days=1000):]['SMA_50'], label='SMA50')
plt.legend()
plt.title('Moyennes mobiles 20 et 50 jours')
plt.show()

# Test t entre deux périodes (adjusting for dummy data time range)
# Using two distinct periods from the dummy data, e.g., first 100 days vs last 100 days
close_period1 = df['Adj Close'].iloc[0:100]
close_period2 = df['Adj Close'].iloc[-100:]

t_stat, p_value = stats.ttest_ind(close_period1, close_period2, equal_var=False)
print(f"t-test Période 1 vs Période 2 : t={t_stat:.4f}, p={p_value:.4e}")

# Rendements et test de normalité
df['Returns'] = df['Adj Close'].pct_change()
returns_clean = df['Returns'].dropna()
print(returns_clean.describe())

plt.figure(figsize=(10,5))
plt.hist(returns_clean, bins=100, density=True, alpha=0.6, color='skyblue', edgecolor='black')
mu, std = returns_clean.mean(), returns_clean.std()
x = np.linspace(returns_clean.min(), returns_clean.max(), 200)
plt.plot(x, stats.norm.pdf(x, mu, std), 'r-', label=f'Normale (μ={mu:.4f}, σ={std:.4f})')
plt.legend()
plt.title('Distribution des rendements')
plt.show()

stat_norm, p_norm = stats.normaltest(returns_clean)
print(f"Test de normalité : p={p_norm:.4e}")

# Convolution pour moyenne mobile
def moving_average_convolve(data, window):
    return np.convolve(data, np.ones(window)/window, mode='valid')

prices = df['Adj Close'].values
sma_conv = moving_average_convolve(prices, 20)
sma_pd = df['Adj Close'].rolling(20).mean().dropna().values
# Ensure lengths match for comparison
sma_conv = sma_conv[-len(sma_pd):]
print(f"Différence max entre convolve et rolling : {np.max(np.abs(sma_conv - sma_pd))}")

# Corrélation SMA / Volume
corr_data = df[['SMA_20', 'SMA_50', 'Volume']].dropna()
corr20 = np.corrcoef(corr_data['SMA_20'], corr_data['Volume'])[0,1]
corr50 = np.corrcoef(corr_data['SMA_50'], corr_data['Volume'])[0,1]
print(f"Corrélation SMA20/Volume : {corr20:.4f}")
print(f"Corrélation SMA50/Volume : {corr50:.4f}")
