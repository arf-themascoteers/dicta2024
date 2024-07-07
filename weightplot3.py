import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

paths = {
    'weight/weights_v0_weight_indian_pines_30_weights.csv' : "v0",
    'weight/weights_v2_weight_indian_pines_30_weights.csv' : "v2"
}

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

for path in paths:
    data = pd.read_csv(path).values[:, 1:]
    means = np.mean(data, axis=1)
    stds = np.std(data, axis=1)
    cv = stds / means

    axes[0].plot(cv, linestyle='-', label=paths[path])
    axes[1].plot(means, linestyle='-', label=paths[path])

axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Coefficient of Variation (CV)')
axes[0].set_title('Coefficient of Variation (CV) of weights across the samples')
axes[0].legend(loc='center left', bbox_to_anchor=(1, 0.5))
axes[0].legend()

axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Mean weight')
axes[1].set_title('Mean weight across the samples')
axes[1].legend(loc='center left', bbox_to_anchor=(1, 0.5))
axes[1].legend()

plt.savefig('stored_figs/weightplot.png')