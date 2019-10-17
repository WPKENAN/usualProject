import numpy as np
import pandas as pd
import sys
from mpl_toolkits.mplot3d import Axes3D
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.datasets import fetch_california_housing
from sklearn.metrics import mean_squared_error,mean_absolute_error

from pykrige.rk import RegressionKriging
from pykrige.compat import train_test_split
import matplotlib.pyplot as plt
svr_model = SVR(C=0.1)
rf_model = RandomForestRegressor(n_estimators=100)
lr_model = LinearRegression(normalize=True, copy_X=True, fit_intercept=False)

models = [svr_model, rf_model, lr_model]

def readCsv(path):
    df=pd.read_csv(path,header=None)
    print(df)
    data=df.values

    xp = data[:, 0:-1]
    p = xp[:,:-2]
    x = xp[:, -2:]
    target = data[:, -1]


    # target=np.reshape(target,(len(target),1))

    print(p.shape, x.shape, target.shape)

    return p,x,target

if __name__=="__main__":
    path='./6.csv'
    p,x,target=readCsv(path)
    p_train, p_test, x_train, x_test, target_train, target_test = train_test_split(p, x, target, test_size=0.05, random_state=42)

    for m in models:
        print('=' * 40)
        print('regression model:', m.__class__.__name__)
        m_rk = RegressionKriging(regression_model=m, n_closest_points=5)
        m_rk.fit(p_train, x_train, target_train)
        # print('Regression Score: ', m_rk.regression_model.score(p_test, target_test))
        # print('RK score: ', m_rk.score(p_test, x_test, target_test))

        pred=m_rk.predict(p_test, x_test)
        print("RMSE ",np.sqrt(mean_squared_error(pred,target_test)))
        print("MAE ",mean_absolute_error(pred,target_test))
        print("相对预测误差百分比: {}%".format(np.mean(np.abs(pred-target_test)/target_test)*100))
        print("最大预测误差百分比: {}%".format(np.max(np.abs(pred-target_test)/target_test)*100))


        ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
        ax.scatter(x[:,0],x[:,1],m_rk.predict(p, x),color='red',label='pred')
        ax.set_zlabel('target')  # 坐标轴
        ax.set_ylabel('x2')
        ax.set_xlabel('x1')

        ax.scatter(x[:, 0], x[:, 1], target, color='blue',label='real')
        ax.set_zlabel('target')  # 坐标轴
        ax.set_ylabel('x2')
        ax.set_xlabel('x1')
        plt.legend()
        plt.title("{}-RegressionKriging".format(m.__class__.__name__))
        plt.show()

