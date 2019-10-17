import numpy as np
import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

from sklearn.gaussian_process import GaussianProcessRegressor

from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from sklearn.metrics import mean_squared_error,mean_absolute_error
from mpl_toolkits.mplot3d import Axes3D


def readCsv(path):
    df=pd.read_csv(path,header=None)
    data=df.values
    x,y=data[:,:-1],data[:,-1]
    return x,y

def draw(x1set, x2set,i,j,output, err,sigma):


    output, err = output.reshape(x1set.shape), err.reshape(x1set.shape)

    up, down = output * (1 + 1.96 * err), output * (1 - 1.96 * err)

    # 作图，并画出

    fig = plt.figure(figsize=(10.5, 5))

    ax1 = fig.add_subplot(121, projection='3d')

    surf = ax1.plot_wireframe(x1set, x2set, output, rstride=10, cstride=2, antialiased=True)

    surf_u = ax1.plot_wireframe(x1set, x2set, up, colors='lightgreen', linewidths=1,

                                rstride=10, cstride=2, antialiased=True)

    surf_d = ax1.plot_wireframe(x1set, x2set, down, colors='lightgreen', linewidths=1,

                                rstride=10, cstride=2, antialiased=True)

    ax1.scatter(x[:, 0], x[:, 1], y, c='red')

    ax1.set_title('{}-{}'.format(i,j))

    ax1.set_xlabel('{}'.format(i))

    ax1.set_ylabel('{}'.format(j))

    plt.show()


def gs(x,y,i,j):
    kernel = C(0.1, (0.001, 0.1)) * RBF(0.5, (1e-4, 10))
    reg = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10, alpha=0.1)
    reg.fit(x, y)

    pred, err = reg.predict(x, return_std=True)
    print("RMSE ", np.sqrt(mean_squared_error(pred, y)))
    print("MAE ", mean_absolute_error(pred, y))
    print("相对预测误差百分比: {}%".format(np.mean(np.abs(pred - y) / y) * 100))
    print("最大预测误差百分比: {}%".format(np.max(np.abs(pred - y) / y) * 100))


    # print("yes")
    # print(reg.alpha_,reg.kernel_,reg.L_,reg.)
    x1_min, x1_max = x[:, 0].min() - 1, x[:, 0].max() + 1
    x2_min, x2_max = x[:, 1].min() - 1, x[:, 1].max() + 1

    x1set, x2set = np.meshgrid(np.arange(x1_min, x1_max, 0.5), np.arange(x2_min, x2_max, 0.5))

    # 查看网格测试数据输出结果，并返回标准差。

    output, err = reg.predict(np.c_[x1set.ravel(), x2set.ravel()], return_std=True)

    output, err = output.reshape(x1set.shape), err.reshape(x1set.shape)

    sigma = np.sum(reg.predict(x, return_std=True)[1])

    up, down = output * (1 + 1.96 * err), output * (1 - 1.96 * err)

    # 作图，并画出

    fig = plt.figure(figsize=(10.5, 5))

    ax1 = fig.add_subplot(111, projection='3d')

    surf = ax1.plot_wireframe(x1set, x2set, output, rstride=10, cstride=2, antialiased=True)

    surf_u = ax1.plot_wireframe(x1set, x2set, up, colors='lightgreen', linewidths=1,

                                rstride=10, cstride=2, antialiased=True)

    surf_d = ax1.plot_wireframe(x1set, x2set, down, colors='lightgreen', linewidths=1,

                                rstride=10, cstride=2, antialiased=True)

    ax1.scatter(x[:, 0], x[:, 1], y, c='red')

    ax1.set_title('{}-{}'.format(i, j))

    ax1.set_xlabel('{}'.format(i))

    ax1.set_ylabel('{}'.format(j))

    plt.show()



if __name__=="__main__":
    path='./6.csv'
    x,y=readCsv(path)

    kernel = C(0.1, (0.001, 0.1)) * RBF(0.5, (1e-4, 10))
    reg = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10, alpha=0.1)
    reg.fit(x, y)

    print("All features")
    pred,err = reg.predict(x,return_std=True)
    sigma = np.sum(reg.predict(x, return_std=True)[1])
    print("RMSE ", np.sqrt(mean_squared_error(pred, y)))
    print("MAE ", mean_absolute_error(pred, y))
    print("相对预测误差百分比: {}%".format(np.mean(np.abs(pred - y) / y) * 100))
    print("最大预测误差百分比: {}%".format(np.max(np.abs(pred - y) / y) * 100))

    #draw
    # x_list=[]
    # for i in range(x.shape[1]):
    #     print(i)
    #     x_list.append(np.arange(np.min(x[:,i]),np.max(x[:,i]),0.5))
    #
    # x_mesh=np.meshgrid(*x_list)
    #
    # x_ravel=[]
    # for i in range(x.shape[1]):
    #     x_ravel.append(x_mesh[i].ravel())
    #
    # print(np.array(*x_ravel))


    # output, err = reg.predict(10, return_std=True)
    # print(output.shape)
    # output, err = output.reshape(xset.shape), err.reshape(xset.shape)
    # sigma = np.sum(reg.predict(data[:, :-1], return_std=True)[1])
    print("*"*50)
    for i in range(x.shape[1]):
        for j in range(i,x.shape[1]):
            if i==j:
                continue
            print("Features {}-{}".format(i,j))
            gs(x[:,[i,j]],y,i,j)

