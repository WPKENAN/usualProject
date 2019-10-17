import numpy as np
# import pywt
import scipy.io as scio
import matplotlib.pyplot as plt
from pylab import mpl

import pandas as pd
from numpy.testing import (run_module_suite, assert_allclose, assert_,
                           assert_raises, assert_equal)

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


def em_my(data,Mu,SigmaSquare,lanmda,Alpha):
    Mus, SigmaSquares, lanmdas, Alphas,Probability=[],[],[],[],[]

    N=len(data)
    i = 0  # 迭代次数
    print("第%d次迭代" % (i));
    print("Mu:", Mu);
    print("Sigma:", np.sqrt(SigmaSquare));
    print("lanmda", lanmda)
    print("Alpha:", Alpha);

    for i in range(10):
        PreAlpha = Alpha.copy();

        # Expectation
        gauss1 = Normal(data, Mu, np.sqrt(SigmaSquare));
        gauss2 = Exp(data, lanmda);

        Gamma1 = Alpha[0][0] * gauss1;
        Gamma2 = Alpha[0][1] * gauss2;

        M = Gamma1 + Gamma2;

        Probability.append(np.sum(M) / 2 / N)

        Alpha[0][0] = np.sum(Gamma1 / M) / N;
        Alpha[0][1] = np.sum(Gamma2 / M) / N;

        Mu = np.dot((Gamma1 / M).T, data) / np.sum(Gamma1 / M);
        SigmaSquare = np.dot((Gamma1 / M).T, (data - Mu) ** 2) / np.sum(Gamma1 / M)
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

        print("************************Over***************************")
        print("第%d次迭代" % (i));
        print("Mu:", Mu);
        print("Sigma:", np.sqrt(SigmaSquare));
        print("lanmda", lanmda)
        print("Alpha:", Alpha);

    return np.array(Mus),np.array(SigmaSquares),np.array(lanmdas),Alphas,Probability


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

    lanmda = np.random.random()
    Mu = np.random.random();
    SigmaSquare = np.random.random();

    a = np.random.random();
    b = 1 - a;
    Alpha = np.array([[a, b]]);
    # Alpha[0][0]#Alpha[0][1]
    Mus, SigmaSquares, lanmdas, Alphas,Probability=em_my(data, Mu, SigmaSquare, lanmda, Alpha)

    df = pd.DataFrame(np.array(Probability))
    df.to_csv("result.csv")
    print(np.array(Probability).shape)

    plt.figure()
    mpl.rcParams['font.sans-serif'] = ['FangSong']
    mpl.rcParams['axes.unicode_minus'] = False
    plt.plot(Mus)
    plt.title('Mus')

    plt.figure()
    plt.plot(SigmaSquares)
    plt.title("SigmaSquares")

    plt.figure()
    plt.plot(lanmdas)
    plt.title("lanmdas")

    plt.figure()
    plt.plot(np.array(Alphas)[:,0,0],label='正态分布权重')
    plt.plot(np.array(Alphas)[:, 0, 1],label='指数分布权重')
    plt.legend()

    plt.title("Alphas")

    plt.figure()
    plt.plot(Probability)
    plt.title("联合分布概率")
    plt.show()




if __name__=="__main__":
    main()

