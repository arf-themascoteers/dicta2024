import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Generate sample data
df = pd.read_csv('newest/dummyv0/dummyv0_v0_indian_pines_5_weights.csv')
data = df.to_numpy()[:,1:]

# Create heatmap
plt.figure(figsize=(20, 10))
sns.heatmap(data.T, cmap='viridis', cbar=True)
plt.xlabel('Row Index')
plt.ylabel('Features')
plt.title('Variability among Features across Rows')
plt.show()
