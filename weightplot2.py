import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#data = pd.read_csv('newest/dummyv0/dummyv0_v0_indian_pines_5_weights.csv').values[:, 1:]
data = pd.read_csv('newest/dummyv2/dummyv2_v2_indian_pines_5.csv').values[:, 1:]
means = np.mean(data, axis=1)
stds = np.std(data, axis=1)
cv = stds / means

plt.figure(figsize=(10, 6))
plt.plot(cv, linestyle='-')
plt.xlabel('Feature Index')
plt.ylabel('Coefficient of Variation (CV)')
plt.title('Coefficient of Variation among Features')
plt.show()