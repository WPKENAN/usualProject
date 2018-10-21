import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
x=np.array([
    [0,0,0,1,1],
    [1,0,0,1,1],
    [1,0,1,1,1],
    [1,1,0,1,1],

    [0,0,1,1,-1],
    [0,1,1,1,-1],
    [0,1,0,1,-1],
    [1,1,1,1,-1],
])


w=np.array([[-1,-2,-2,0]]);
c=1;
# print(w);


m,n=x.shape;

def Refresh1(x,w,c):
    for t in range(10000):
        print("第%d代"%(t))
        print(w[-1])
        errorset=[];
        for i in range(m):
            if np.dot(x[i,0:4],w[-1].transpose()) * x[i,-1]<=0:
                errorset.append(i);
        print(errorset)
        if len(errorset)==0:
            break;
        print(x[errorset, -1].reshape(len(errorset), 1))
        print(x[errorset, 0:4])

        print(c * x[errorset, -1].reshape(len(errorset), 1) * x[errorset, 0:4])

        w_new=w[-1]+(c*x[errorset,-1].reshape(len(errorset),1)*x[errorset,0:4]).sum(axis=0);
        w=np.row_stack((w,w_new));
    return w


def Refresh2(x,w,c):
    step = 0;
    for t in range(10000):
        flag=1;
        for i in range(m):
            errorset = [];
            if np.dot(x[i,0:4],w[-1].transpose()) * x[i,-1]<=0:
                print("第%d代w:" % (step))
                print(w[-1])
                errorset.append(i);
                # print(c * x[errorset, -1].reshape(len(errorset), 1) * x[errorset, 0:4])
                w_new = w[-1] + (c * x[errorset, -1].reshape(len(errorset), 1) * x[errorset, 0:4]).sum(axis=0);
                w = np.row_stack((w, w_new));
                flag=0;
                step = step + 1;

        if flag:
            break;

    return w


w=Refresh2(x,w,c);
fig=plt.figure();
n=len(w);

print('开始做图')
# plt.ion()
for i in range(n):

    # 清除原有图像
    fig.clf()
    ax = fig.add_subplot(111, projection="3d")
    # ax=Axes3D(fig);
    X, Y, Z = x[:, 0], x[:, 1], x[:, 2]

    ax.scatter(X[0:4], Y[0:4], Z[0:4], c='r');
    ax.scatter(X[4:8], Y[4:8], Z[4:8], c='g');
    #
    #
    wx = np.linspace(0, 1, 2);
    wx, wy = np.meshgrid(wx, wx);
    print(w[i%n]);
    wz = -w[i%n,0]/w[i%n,2]*wx-w[i%n,1]/w[i%n,2]*wy-w[i%n,3]/w[i%n,2];
    ax.plot_surface(wx, wy, wz)

    # # 设置坐标轴范围
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_zlim(-0.25, 1.25)

    # 暂停
    plt.pause(c)
# 关闭交互模式
# plt.ioff()
plt.show()


# def update(i):
#     label = 'timestep {0}'.format(i)
#     print(label)
#     # 更新直线和x轴（用一个新的x轴的标签）。
#     # 用元组（Tuple）的形式返回在这一帧要被重新绘图的物体
#     line.set_zdata(-w[i%4,0]/w[i%4,2]*wx-w[i%4,1]/w[i%4,2]*wy-w[i%4,3]/w[i%4,2])
#     return line
#
# # FuncAnimation 会在每一帧都调用“update” 函数。
# # 在这里设置一个10帧的动画，每帧之间间隔200毫秒
# anim = FuncAnimation(fig, update, frames=np.arange(0, 10), interval=200)
# 打开交互模式
