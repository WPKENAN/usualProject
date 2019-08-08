import sklearn
from sklearn.model_selection import train_test_split
import processingData
from sklearn.metrics import r2_score
# import visuals as vs
from sklearn.svm import SVR
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler


def loadData(path,header):
    data=processingData.readXlsx(path,header);
    # print(data.shape)
    x,y=data[:,0:-1],data[:,-1]
    # print(x,y)
    return x,y;

    # return X_train, X_test, y_train, y_test

def performance_metric(y_true,y_predict):
    '''计算实际值与预测值的R2分数'''
    score = r2_score(y_true,y_predict)
    return score


def train(path,header):
    x,y=loadData(path,header);
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

    # 分析回归目标值的差异
    print('The max target value is ', np.max(y))
    print('The min target value is ', np.min(y))
    print('The average target value is ', np.mean(y))

    # 第三步：训练数据和测试数据标准化处理
    # 分别初始化对特征值和目标值的标准化器
    ss_X = StandardScaler()
    ss_y = StandardScaler()
    # 训练数据都是数值型，所以要标准化处理
    X_train = ss_X.fit_transform(X_train)
    X_test = ss_X.transform(X_test)
    # 目标数据（房价预测值）也是数值型，所以也要标准化处理
    # 说明一下：fit_transform与transform都要求操作2D数据，而此时的y_train与y_test都是1D的，因此需要调用reshape(-1,1)，例如：[1,2,3]变成[[1],[2],[3]]
    y_train = ss_y.fit_transform(y_train.reshape(-1, 1))
    y_test = ss_y.transform(y_test.reshape(-1, 1))

    # 1.使用线性核函数配置的支持向量机进行回归训练并预测
    linear_svr = SVR(kernel='linear')
    linear_svr.fit(X_train, y_train)
    linear_svr_y_predict = linear_svr.predict(X_test)
    # 2.使用多项式核函数配置的支持向量机进行回归训练并预测
    poly_svr = SVR(kernel='poly')
    poly_svr.fit(X_train, y_train)
    poly_svr_y_predict = poly_svr.predict(X_test)
    # 3.使用径向基核函数配置的支持向量机进行回归训练并预测
    rbf_svr = SVR(kernel='rbf')
    rbf_svr.fit(X_train, y_train)
    rbf_svr_y_predict = rbf_svr.predict(X_test)

    # 第五步：对三种核函数配置下的支持向量机回归模型在相同测试集下进行性能评估
    # 使用R-squared(越大越好)、MSE（越小越好）、MAE（越小越好）指标评估
    #参考链接https://www.jianshu.com/p/9ee85fdad150


    # 1.线性核函数配置的SVR
    print('R-squared value of linear SVR is', linear_svr.score(X_test, y_test))
    print('the MSE of linear SVR is',
          mean_squared_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(linear_svr_y_predict)))
    print('the MAE of linear SVR is',
          mean_absolute_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(linear_svr_y_predict)))
    plt.subplot(2, 2, 1)
    plt.plot(list(range(len(y_test))), ss_y.inverse_transform(linear_svr_y_predict), label='Predicted')
    plt.plot(list(range(len(y_test))), ss_y.inverse_transform(y_test), label='Ideal')
    plt.legend()
    plt.title("linear SVR (R-squared:{:.2f} MSE:{:.2f} MAE:{:.2f})".
              format(linear_svr.score(X_test, y_test),
                     mean_squared_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(linear_svr_y_predict)),
                     mean_absolute_error(ss_y.inverse_transform(y_test),ss_y.inverse_transform(linear_svr_y_predict))))


    # 2.多项式核函数配置的SVR
    print('R-squared value of Poly SVR is', poly_svr.score(X_test, y_test))
    print('the MSE of Poly SVR is',
          mean_squared_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(poly_svr_y_predict)))
    print('the MAE of Poly SVR is',
          mean_absolute_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(poly_svr_y_predict)))

    plt.subplot(2, 2, 2)
    plt.plot(list(range(len(y_test))), ss_y.inverse_transform(poly_svr_y_predict), label='Predicted')
    plt.plot(list(range(len(y_test))), ss_y.inverse_transform(y_test), label='Ideal')
    plt.legend()
    plt.title("Poly SVR (R-squared:{:.2f} MSE:{:.2f} MAE:{:.2f})".
              format(poly_svr.score(X_test, y_test),
                     mean_squared_error(ss_y.inverse_transform(y_test),ss_y.inverse_transform(poly_svr_y_predict)),
                     mean_absolute_error(ss_y.inverse_transform(y_test),ss_y.inverse_transform(poly_svr_y_predict))))

    # 3.径向基核函数配置的SVR
    print('R-squared value of RBF SVR is', rbf_svr.score(X_test, y_test))
    print('the MSE of RBF SVR is',
          mean_squared_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(rbf_svr_y_predict)))
    print('the MAE of RBF SVR is',
          mean_absolute_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(rbf_svr_y_predict)))

    plt.subplot(2,2,3)
    plt.plot(list(range(len(y_test))),ss_y.inverse_transform(rbf_svr_y_predict),label='Predicted')
    plt.plot(list(range(len(y_test))), ss_y.inverse_transform(y_test),label='Ideal')
    plt.legend()
    plt.title("RBF SVR (R-squared:{:.2f} MSE:{:.2f} MAE:{:.2f})".
              format(rbf_svr.score(X_test, y_test),
                     mean_squared_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(rbf_svr_y_predict)),
                     mean_absolute_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(rbf_svr_y_predict))))
    plt.show()

if __name__=="__main__":
    path="data.xlsx"
    # loadData(path,0)
    train(path,0)