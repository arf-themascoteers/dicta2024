import os
import shutil

s = "saved_results/v42"
t = "saved_results/v4"

os.makedirs(t, exist_ok=True)

for f in os.listdir(s):
    path = os.path.join(s, f)
    t_path = path.replace("v42","v4")
    shutil.copy(path, t_path)