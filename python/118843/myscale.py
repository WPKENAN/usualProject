import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from matplotlib_scalebar.scalebar import ScaleBar
plt.figure()
image = plt.imread("China per capita national income distribution map.jpg")
plt.imshow(image)
scalebar = ScaleBar(208*200) # 1 pixel = 0.2 meter
plt.gca().add_artist(scalebar)
plt.show()