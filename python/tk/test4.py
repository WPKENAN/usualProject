import matplotlib.pyplot as plt
import numpy as np

x = np.arange(-np.pi, np.pi, 0.01)

fig = plt.figure()
fig.suptitle('Main figure title')

ax1 = fig.add_subplot(311, title='Subplot 1 title')
ax1.plot(x, np.sin(x))

ax2 = fig.add_subplot(312)
ax2.set_title('Subplot 2 title')
ax2.plot(x, np.cos(x))

ax3 = fig.add_subplot(313)
ax3.set_title('Subplot 3 title')
ax3.plot(x, np.tan(x))

plt.show()