
import numpy as np
import pandas as pd

from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn import svm
from sklearn.model_selection import train_test_split
def main():
    pass

def process(data):
    for i in range(len(data)):
        # print(data[i,1],type(data[i,1]))
        if type(data[i,1]) == type('a'):
            data[i,1]=float(data[i,1].replace(',',''))

def read():
    data = np.zeros((31, 12))
    df = pd.read_excel("./data/Phosporus磷.xlsx", header=3)
    Phosporus = df.values[:-1, [0, 2]]
    process(Phosporus)
    data[:, 0] = Phosporus[:, 1]

    df = pd.read_excel("./data/Petroleum石油排放.xlsx", header=3)
    Petroleum = df.values[:-1, [0, 2]]
    process(Petroleum)
    data[:, 1] = Petroleum[:, 1]

    df = pd.read_excel("./data/Arsenic砷.xls", header=3)
    Arsenic = df.values[:-1, [0, 2]]
    process(Arsenic)
    data[:, 2] = Arsenic[:, 1]

    df = pd.read_excel("./data/chromium铬.xls", header=3)
    chromium = df.values[:-1, [0, 2]]
    process(chromium)
    data[:, 3] = chromium[:, 1]

    df = pd.read_excel("./data/plumbum铅.xls", header=3)
    plumbum = df.values[:-1, [0, 2]]
    process(plumbum)
    data[:, 4] = plumbum[:, 1]

    df = pd.read_excel("./data/Mercury汞.xls", header=3)
    Mercury = df.values[:-1, [0, 2]]
    process(Mercury)
    data[:, 5] = Mercury[:, 1]

    df = pd.read_excel("./data/COD.xls", header=3)
    COD = df.values[:-1, [0, 2]]
    process(COD)
    data[:, 6] = COD[:, 1]

    df = pd.read_excel("./data/Ammonia nitrogen氨氮.xlsx", header=3)
    AN = df.values[:-1, [0, 2]]
    process(AN)
    data[:, 7] = AN[:, 1]

    df = pd.read_excel("./data/人均国民收入10年带total.xlsx", header=3)
    income = df.values[:-3, [0, 2]]
    process(income)
    data[:, 8] = income[:, 1]

    df = pd.read_excel("./data/Animal husbandary畜牧业总产值（亿元）.xlsx", header=3)
    Ah = df.values[:-3, [0, 2]]
    process(Ah)
    data[:, 9] = Ah[:, 1]

    df = pd.read_excel("./data/Total waste water releaseAnnualbyProvince- 20 yrs(1).xlsx", header=3)
    wastewater = df.values[:-3, [0, 2]]
    process(wastewater)
    data[:, 10] = wastewater[:, 1]

    df = pd.read_excel("./data/农业总产值（亿元）.xlsx", header=3)
    print(df)
    al = df.values[:-1, [0, 2]]
    process(al)
    data[:, 11] = al[:, 1]


    mean_= np.mean(data,axis=0)
    std_= np.std(data, ddof=1,axis=0)

    mean_ = 0
    std_ = 1

    data = (data - mean_) / std_

    x = data[:, 0:-1]
    y = data[:, -1]

    return x,y,mean_,std_


if __name__=="__main__":
    listLable=['Phosporus','Petroleum','Arsenic','chromium','plumbum','Mercury','COD','AN','income','Ah','agriculture','wastewater']
    from sklearn.linear_model import LinearRegression
    x,y,mean_,std_=read()
    from sklearn.metrics import mean_absolute_error,mean_squared_error
    plt.figure(figsize=(100, 50))
    for i in range(11):
        plt.subplot(3,4,i+1)
        xi=x[:,i]
        xi = np.reshape(xi, (len(x), 1))
        lr = LinearRegression()
        lr.fit(xi, y)
        y_pred = lr.predict(xi)
        plt.scatter(xi,y,color='b',label='true')
        plt.plot(xi,y_pred,color='r',label='LinearRegression')
        plt.title("{}-{} LinearRegression msrm={:.2}".format(listLable[i],listLable[-1],np.sqrt(mean_squared_error(y,y_pred))),fontsize=30)
        plt.xlabel(listLable[i],fontsize=30)
        plt.ylabel(listLable[-1]+"/(ton)",fontsize=30)
        plt.legend()
    plt.savefig('pro2.jpg',bbox_inches = 'tight')
