import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('your_file.csv')
batch = data.iloc[:, 0]
mean_weight = data.iloc[:, 1]
std_weight = data.iloc[:, 2]

fig, ax1 = plt.subplots()

ax1.plot(batch, mean_weight, 'b-')
ax1.set_xlabel('Batch Number')
ax1.set_ylabel('Mean Weight', color='b')

ax2 = ax1.twinx()
ax2.plot(batch, std_weight, 'r-')
ax2.set_ylabel('Standard Deviation of Weights', color='r')

plt.show()
