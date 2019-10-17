import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR

def readCsv(path):
    df=pd.read_csv(path,header=None);
    #pos neu neg
    data=df.values;

    return data[:,0:3],data[:,-1]



if __name__=="__main__":
    SA = ['negative','neutral', 'positive']
    path=['./SA_pre.csv','./SA_pre-post.csv','./SA_post.csv','./SA_total.csv']

    for j in range(len(path)):
        x_all, y = readCsv(path[j])
        lr = LinearRegression()
        lr.fit(x_all, y)
        print("{}".format(path[j].strip('.csv').split('_')[1]))
        print("系数:",lr.coef_)
        print("偏移量:",lr.intercept_)
        print("*"*20)

    # plt.savefig("情感分析-线性回归.jpg")
    # plt.show()
