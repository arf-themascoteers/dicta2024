import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

paths = [
    'newest/dummyv0/dummyv0_v0_indian_pines_5_weights.csv',
    'newest/dummyv2/dummyv2_v2_indian_pines_5_weights.csv'
]

num_paths = len(paths)
fig, axes = plt.subplots(num_paths, 2, figsize=(15, 6 * num_paths))

if num_paths == 1:
    axes = [axes]

for i, path in enumerate(paths):
    data = pd.read_csv(path).values[:, 1:]
    means = np.mean(data, axis=1)
    stds = np.std(data, axis=1)
    cv = stds / means

    axes[i][0].plot(cv, linestyle='-')
    axes[i][0].set_xlabel('Feature Index')
    axes[i][0].set_ylabel('Coefficient of Variation (CV)')
    axes[i][0].set_title(f'Coefficient of Variation (CV) for {path}')

    axes[i][1].plot(means, linestyle='-')
    axes[i][1].set_xlabel('Feature Index')
    axes[i][1].set_ylabel('Mean')
    axes[i][1].set_title(f'Mean for {path}')

plt.tight_layout()
plt.show()
