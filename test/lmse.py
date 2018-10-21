import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
x=np.matrix([
    [0,0,0,1],
    [1,0,0,1],
    [1,0,1,1],
    [1,1,0,1],

    [0,0,-1,-1],
    [0,-1,-1,-1],
    [0,-1,0,-1],
    [-1,-1,-1,-1],
])

#伪逆解 w* =(x'x)^-1 x'b
c=2;
x_sharp=(x.T*x).I*x.T;
b=np.matrix([1,1,1,1,1,1,1,1]).T;
w=x_sharp*b;





for i in range(100000):
    print("第%d代"%(i));
    print(w.T)
    E=x*w-b;
    count=0;

    if abs(E.all())==0:
        break;

    w=w+c*x_sharp*abs(E);
    b=b+c*(E+abs(E))

print(w)

fig=plt.figure();
ax = fig.add_subplot(111, projection="3d")
# ax=Axes3D(fig);
X, Y, Z = x[:, 0], x[:, 1], x[:, 2]

ax.scatter(X[0:4], Y[0:4], Z[0:4], c='r');
ax.scatter(-X[4:8], -Y[4:8], -Z[4:8], c='g');

wx = np.linspace(0, 1, 2);
wx, wy = np.meshgrid(wx, wx);

wz = -w[0,0]/w[2,0]*wx-w[1,0]/w[2,0]*wy-w[3,0]/w[2,0];
ax.plot_surface(wx, wy, wz)

# # # 设置坐标轴范围
# ax.set_xlim(0, 1)
# ax.set_ylim(0, 1)
# ax.set_zlim(-0.25, 1.25)

plt.show()
