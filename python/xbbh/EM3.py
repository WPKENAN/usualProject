import numpy as np
import matplotlib.pyplot as plt
import copy
from pylab import mpl
import pandas as pd
def Normal(x, mu, sigma):  # 一元正态分布概率密度函数
    return 1/(np.sqrt(2 * np.pi) * sigma)*np.exp(-((x - mu) *(x-mu) )/ (2 * sigma * sigma));

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

def em(data,Mu,SigmaSquare,lanmda,Alpha):
    Mus, SigmaSquares, lanmdas, Alphas,Probability=[],[],[],[],[]

    N=len(data)
    i = 0  # 迭代次数
    print("********************************初始化参数:**********************************")
    print("第%d次迭代" % (i));
    print("Mu:", Mu);
    print("Sigma:", np.sqrt(SigmaSquare));
    print("lanmda", lanmda)
    print("Alpha:", Alpha);
    print("****************************迭代开始******************************************")
    # print(Normal(1.7419813,1.7419813,0.09193604))
    while True:

        if i>10000:
            break
        PreAlpha = Alpha.copy();
        i += 1;

        # Expectation
        gauss1 = Normal(data, Mu, np.sqrt(SigmaSquare));  # 模型一
        gauss2 = Exp(data, lanmda);

        # print(data[3269],gauss1[3269],Mu,np.sqrt(SigmaSquare))
        # plt.plot(gauss2/np.max(gauss2))
        # plt.show()
        # print()

        # temp=1;
        # for i in gauss1:
        #     temp=temp*i;
        # for i in gauss2:
        #     temp=temp*i;
        # Probability.append(temp)
        Gamma1 = Alpha[0][0] * gauss1;
        Gamma2 = Alpha[0][1] * gauss2;

        M = Gamma1 + Gamma2;

        Probability.append(np.sum(M) / 2 / N)
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

        Mus.append(Mu)
        SigmaSquares.append(SigmaSquare)
        lanmdas.append(lanmda)
        Alphas.append(copy.deepcopy(Alpha))
        if i % 1 == 0:
            print("第%d次迭代" % (i));
            print("Mu:", Mu);
            print("Sigma:", np.sqrt(SigmaSquare));
            print("lanmda", lanmda)
            print("Alpha:", Alpha);

        eps=1e-20
        if i > 2 and (abs(Alphas[-1]-Alphas[-2]) < eps).all() and (abs(SigmaSquares[-1]-SigmaSquares[-2]) < eps).all()\
                and (abs(lanmdas[-1]-lanmdas[-2]) < eps).all() and (abs(Mus[-1]-Mus[-2]) < eps).all():

            print("************************Over***************************")
            print("第%d次迭代" % (i));
            print("Mu:", Mu);
            print("Sigma:", np.sqrt(SigmaSquare));
            print("lanmda", lanmda)
            print("Alpha:", Alpha);
            break;


    return np.array(Mus),np.array(SigmaSquares),np.array(lanmdas),Alphas,Probability

if __name__=="__main__":
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
    Mus, SigmaSquares, lanmdas, Alphas, Probability = em(data, Mu, SigmaSquare, lanmda, Alpha)

    df = pd.DataFrame(np.array(Probability))
    df.to_csv("Probability.csv")
    print(np.array(Probability).shape)

    # print(Probability)
    # print(Mus)
    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    plt.subplot(231)
    plt.plot(Mus[:,:,0])
    plt.title('Mus')
    # plt.show()

    plt.subplot(232)
    plt.plot(SigmaSquares[:,:,0])
    plt.title("SigmaSquares")

    plt.subplot(233)
    plt.plot(lanmdas[:,:,0])
    plt.title("lanmdas")

    # print(np.array(Alphas)[:,0,:])
    plt.subplot(234)
    plt.plot(np.array(Alphas)[:, 0, 0], label='正态分布权重')
    plt.plot(np.array(Alphas)[:, 0, 1], label='指数分布权重')
    plt.legend()
    # plt.plot(Alphas[:, 1])
    plt.title("Alphas")

    plt.subplot(235)
    plt.plot(Probability)
    plt.title("联合分布概率")
    plt.show()

