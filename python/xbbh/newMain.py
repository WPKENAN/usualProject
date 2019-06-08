from EM3 import *
import numpy as np
import pywt
import scipy.io as scio
import matplotlib.pyplot as plt

import pandas as pd
from numpy.testing import (run_module_suite, assert_allclose, assert_,
                           assert_raises, assert_equal)

def myTest():
    N = 10000;
    N_boys = int(N * 0.6);
    N_girls = N - N_boys;

    np.random.seed(1);

    # 第一种分布
    mu1 = 1.74;
    sigma1 = 0.0865;
    BoyHeights = np.random.normal(mu1, sigma1, N_boys);
    BoyHeights.shape = N_boys, 1;
    # 第二种分布
    lanmda1 = 1.6;
    GirlHeights = np.random.exponential(lanmda1, N_girls);
    GirlHeights.shape = N_girls, 1;

    data = np.concatenate((BoyHeights, GirlHeights));

    print(data.shape)

    # 随机初始化模型参数
    lanmda = np.random.random()
    Mu = np.random.random();  # 平均值向量
    SigmaSquare = np.random.random();  # 模型迭代用Sigma平方

    a = np.random.random();
    b = 1 - a;
    Alpha = np.array([[a, b]]);
    # Alpha[0][0]#Alpha[0][1]
    em(data, Mu, SigmaSquare, lanmda, Alpha)

def wave():
    data=list(np.random.normal(0,1,1000));
    # print(data.shape)
    x = [1, 11, 3, 4, 5, 20, 7, 10]
    print(data)
    wp = pywt.WaveletPacket(data=data, wavelet='db1', mode='symmetric')

    # assert_(wp.data == [1, 2, 3, 4, 5, 6, 7, 8])
    # assert_(wp.path == '')
    # assert_(wp.level == 0)
    # assert_(wp['ad'].maxlevel == 3)
    print(wp.data)

def main():
    data_path = "./97.mat"
    data = scio.loadmat(data_path)
    print(data.keys())
    keyStr = ""
    for key in data.keys():
        if "DE" in key:
            keyStr = key
            break;

    data = data[keyStr]
    data = np.reshape(data, len(data))
    print(data.shape)
    # print(data)
    # data = data.tolist()
    # print(data)

    # 随机初始化模型参数
    lanmda = np.random.random()
    Mu = np.random.random();  # 平均值向量
    SigmaSquare = np.random.random();  # 模型迭代用Sigma平方

    a = np.random.random();
    b = 1 - a;
    Alpha = np.array([[a, b]]);
    # Alpha[0][0]#Alpha[0][1]
    Mus, SigmaSquares, lanmdas, Alphas=em(data, Mu, SigmaSquare, lanmda, Alpha)

    from pylab import mpl

    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    plt.subplot(221)
    plt.plot(Mus)
    plt.title('Mus')
    # plt.show()

    plt.subplot(222)
    plt.plot(SigmaSquares)
    plt.title("SigmaSquares")

    plt.subplot(223)
    plt.plot(lanmdas)
    plt.title("lanmdas")

    print(np.array(Alphas)[:,0,:])
    plt.subplot(224)
    plt.plot(np.array(Alphas)[:,0,0],label='正态分布权重')
    plt.plot(np.array(Alphas)[:, 0, 1],label='指数分布权重')
    plt.legend()
    # plt.plot(Alphas[:, 1])
    plt.title("Alphas")
    plt.show()




if __name__=="__main__":
    main()

    # wave()
