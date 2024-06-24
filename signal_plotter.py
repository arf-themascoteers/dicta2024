import pandas as pd

import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("data/indian_pines_min.csv")

signal = df.iloc[10,:-1]
x = list(range(len(signal)))


fig, (ax1, ax2) = plt.subplots(1, 2)

sc1 = ax1.scatter(x, signal, c=signal, cmap='viridis')
sc2 = ax2.scatter(x, signal, c=signal, cmap='viridis')

fig.colorbar(sc1, ax=ax1)
fig.colorbar(sc2, ax=ax2)

plt.show()