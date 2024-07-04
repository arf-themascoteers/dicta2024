from sklearn.metrics import accuracy_score
import numpy as np


y_true = np.array([0,1,1,0])
y_pred = np.array([1,1,1,1])

ca = []
for c in np.unique(y_true):
    y_c = y_true[np.nonzero(y_true == c)]
    y_c_p = y_pred[np.nonzero(y_true == c)]
    acurracy = accuracy_score(y_c, y_c_p)
    ca.append(acurracy)
ca = np.array(ca)
aa = ca.mean()
print(ca)
print(aa)
