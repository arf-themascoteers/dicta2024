import pandas as pd
import numpy as np

df = pd.read_csv("data/indian_pines.csv")
data = df.to_numpy()
print("toal",data.shape[0])

classes = np.unique(data[:,-1])

total = 0

for c in classes:
    cnt = len(data[data[:,-1]==c])
    print(c,cnt)
    total=total+cnt

print("rec total", total)