import numpy as np
import matplotlib.pyplot as plt


def Normal(x, mu, sigma):  # 一元正态分布概率密度函数
    return np.exp(-(x - mu) ** 2 / (2 * sigma ** 2)) / (np.sqrt(2 * np.pi) * sigma);

def Exp(x,lanmda):#指数分布
    result=lanmda*np.exp(-lanmda*x);
    result[x<0]=0
    return result

def Wb(x,k,lanmda):
    result = k/lanmda*((x/lanmda)**(k-1))*np.exp(-(x/lanmda)**k)
    result[x < 0] = 0
    return result;



'''
下面给出K=2，即由两个高斯分布组成的混合模型，分别是男女生身高分布。

已经给出了各自分布的比重、参数。用来检验算法生成的参数估计是否准确。
'''

N = 10000;
N_boys = int(N * 0.6);
N_girls = N-N_boys;

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
lanmda=np.random.random()
Mu = np.random.random();  # 平均值向量
SigmaSquare = np.random.random();  # 模型迭代用Sigma平方


a=np.random.random();
b = 1 - a;
Alpha = np.array([[a, b]]);
# Alpha[0][0]#Alpha[0][1]


i = 0  # 迭代次数
print("********************************初始化参数:**********************************")
print("第%d次迭代" % (i));
print("Mu:", Mu);
print("Sigma:", np.sqrt(SigmaSquare));
print("lanmda", lanmda)
print("Alpha:", Alpha);
print("****************************迭代开始******************************************")
while True:
    if i>10000:
        break
    PreAlpha = Alpha.copy();
    i += 1;

    # Expectation
    gauss1 = Normal(data, Mu, np.sqrt(SigmaSquare));  # 模型一
    gauss2 = Exp(data, lanmda);

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
    Mu = np.dot((Gamma1 / M).T, data) / np.sum(Gamma1 / M);
    # 更新sigma
    SigmaSquare = np.dot((Gamma1 / M).T, (data - Mu) ** 2) / np.sum(Gamma1 / M)

    #更新指数分布的参数
    lanmda=np.dot((Gamma2 / M).T, data)/np.sum(Gamma2 / M)

    if i % 2 == 0:
        print("第%d次迭代" % (i));
        print("Mu:", Mu);
        print("Sigma:", np.sqrt(SigmaSquare));
        print("lanmda", lanmda)
        print("Alpha:", Alpha);

    # if ((PreAlpha - Alpha) ** 2).sum() < 1e-20:
        # break;
