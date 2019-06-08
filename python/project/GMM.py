import numpy as np
import matplotlib.pyplot as plt


def Normal(x, mu, sigma):  # 一元正态分布概率密度函数
    return np.exp(-(x - mu) ** 2 / (2 * sigma ** 2)) / (np.sqrt(2 * np.pi) * sigma);


'''
下面给出K=2，即由两个高斯分布组成的混合模型，分别是男女生身高分布。

已经给出了各自分布的比重、参数。用来检验算法生成的参数估计是否准确。
'''

N = 10000;
N_boys = int(N * 0.6);
N_girls = N - N_boys;
k = 2;  # 高斯分布数量
np.random.seed(1);

# 男生身高
mu1 = 1.74;
sigma1 = 0.0865;
BoyHeights = np.random.normal(mu1, sigma1, N_boys);
BoyHeights.shape = N_boys, 1;

# 女生身高
mu2 = 1.63;
sigma2 = 0.0642;
GirlHeights = np.random.normal(mu2, sigma2, N_girls);
GirlHeights.shape = N_girls, 1;

# print(GirlHeights)
data = np.concatenate((BoyHeights, GirlHeights));
# print(data);

# 随机初始化模型参数
Mu = np.random.random((1, 2));  # 平均值向量
# Mu[0][0]#Mu[0][1]


SigmaSquare = np.random.random((1, 2));  # 模型迭代用Sigma平方
# SigmaSquare[0][0]#SigmaSquare[0][1]
# 随机初始化各模型比重系数（大于等于0，且和为1）

a=np.random.random();
b = 1 - a;
Alpha = np.array([[a, b]]);
# Alpha[0][0]#Alpha[0][1]


i = 0  # 迭代次数

while True:
    PreAlpha = Alpha.copy();
    i += 1;

    # Expectation
    gauss1 = Normal(data, Mu[0][0], np.sqrt(SigmaSquare[0][0]));  # 模型一
    gauss2 = Normal(data, Mu[0][1], np.sqrt(SigmaSquare[0][1]));

    Gamma1 = Alpha[0][0] * gauss1;
    Gamma2 = Alpha[0][1] * gauss2;

    M = Gamma1 + Gamma2;
    # print(M)
    # Gamma=np.concatenate((Gamma1/m,Gamma2/m),axis=1) 元素(j,k)为第j个样本来自第k个模型的概率，聚类时用来判别样本分类
    # Maximization
    # 更新Alpha
    Alpha[0][0] = np.sum(Gamma1 / M) / N;
    Alpha[0][1] = np.sum(Gamma2 / M) / N;

    # 更新mu
    Mu[0][0] = np.dot((Gamma1 / M).T, data) / np.sum(Gamma1 / M);
    Mu[0][1] = np.dot((Gamma2 / M).T, data) / np.sum(Gamma2 / M);

    # 更新sigma
    SigmaSquare[0][0] = np.dot((Gamma1 / M).T, (data - Mu[0][0]) ** 2) / np.sum(Gamma1 / M)
    SigmaSquare[0][1] = np.dot((Gamma2 / M).T, (data - Mu[0][1]) ** 2) / np.sum(Gamma2 / M)

    if i % 1000 == 0:
        print("第%d次迭代" % (i));
        print("Mu:", Mu);
        print("Sigma:", np.sqrt(SigmaSquare));
        print("Alpha:", Alpha);
        print(PreAlpha,Alpha,(PreAlpha - Alpha))

    # if ((PreAlpha - Alpha) ** 2).sum() < 1e-20:
        # break;
