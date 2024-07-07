import pandas as pd
from sklearn.model_selection import train_test_split
import os


for f in os.listdir("data"):
    if not f.endswith(".csv"):
        continue
    p = os.path.join("data", f)
    df = pd.read_csv(p)
    print(p)
    unique_classes = df.groupby('class').size()
    print(len(unique_classes))
    print(len(df))
    print(len(df[df['class'] == 0]))
    print(len(df.columns)-1)
