import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from sklearn.linear_model import LinearRegression

def readCsv(path):
    df=pd.read_csv(path,header=None);
    #pos neu neg
    data=df.values;

    return data[:,0:3],data[:,-1]



if __name__=="__main__":
    SA = ['negative','neutral', 'positive']
    path=['./SA_pre.csv','./SA_pre-post.csv','./SA_post.csv','./SA_total.csv']

    plt.figure(figsize=(40, 20))
    for j in range(len(path)):
        x_all, y = readCsv(path[j])
        for i in range(len(SA)):
            plt.subplot(4,3,j*3+i+1)
            x=x_all[:,i]/np.sum(x_all,axis=1)
            x=np.reshape(x,(len(x),1))
            lr = LinearRegression()
            lr.fit(x, y)
            xi = np.linspace(np.min(x), np.max(x), 20)
            xi = np.reshape(xi, (len(xi), 1))
            y_pred = lr.predict(xi)
            plt.scatter(x, y)
            plt.plot(xi, y_pred, color='r',label='lineFit')
            plt.grid()
            # print("Revenue vs. pre tweet count {}".format(lr.coef_[0]))
            # plt.title("Revenue vs. pre tweet count {}".format(lr.coef_[0]))
            plt.xlabel("percent")
            plt.ylabel('Revenue')
            plt.title("{}-{} {:.2e}".format(path[j].strip('.csv').split('_')[1],SA[i],lr.coef_[0]))
            plt.legend()
    plt.savefig("情感分析-线性回归.jpg")
    plt.show()
