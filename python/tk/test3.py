import matplotlib.pyplot as plt
import numpy as np


fig=plt.figure()
ax=fig.add_axes([0.1, 0.1, 0.8, 0.8])
ax.setp
cm = plt.cm.get_cmap('RdYlBu')
xy = range(20)
z = xy
data = np.random.rand(6,6)
print([z,z])
# sc = ax.scatter(xy, xy, c=z, vmin=0, vmax=20, s=35, cmap=cm)
img = ax.imshow([[1,2,5],[3,4,6]],vmin=0.5, vmax=0.99)
fig.colorbar(img)
plt.show()