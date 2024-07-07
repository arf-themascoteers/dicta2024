import pandas as pd
import matplotlib.pyplot as plt

path = "weight/weights_v0_weight_all_indian_pines_30_weights_all.csv"
df = pd.read_csv(path)

batch_numbers = df.iloc[:, 0]
mean_weights = df.iloc[:, 1]

plt.figure(figsize=(10, 6))
plt.bar(batch_numbers, mean_weights)

plt.xlabel('Batch Number')
plt.ylabel('Mean Weight')
plt.title('Mean Weight for Each Batch')

plt.show()
