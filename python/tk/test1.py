import matplotlib.pyplot as plt
from pylab import *
import matplotlib.cm as cm
x = linspace(0, 5, 10)
y = x ** 2

fig = plt.figure()
axes = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # left, bottom, width, height (range 0 to 1)
plt.plot(x, y, 'r')
axes2 = fig.add_axes([0.2, 0.5, 0.4, 0.3]) # inset axes


# plt.plot(x, y, 'r')
cax=axes.plot(x, y)

fig.colorbar(cax,ax=axes)
# axes.set_ylim(-2.0, 92.0)
axes.set_xlabel('x1')
axes.set_ylabel('y1')
axes.set_title('title1')



# insert
axes2.plot(y, x, 'g')
axes2.set_xlabel('y2')
axes2.set_ylabel('x2')
axes2.set_title('insert title2');

plt.show()