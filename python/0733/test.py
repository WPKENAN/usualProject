import numpy as np

a=np.array([[5,4,3,2,1],[5,4,3,2,1]])
print(np.argsort(a)[:,-5:])

# a[np.argsort(a)[:,-5:]]
print(a[0,[1,2]])