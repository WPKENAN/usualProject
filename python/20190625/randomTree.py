import sklearn
from sklearn.model_selection import train_test_split
import processingData
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
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

    # # 分别初始化对特征值和目标值的标准化器
    # ss_X = StandardScaler()
    # ss_y = StandardScaler()
    # # 训练数据都是数值型，所以要标准化处理
    # X_train = ss_X.fit_transform(X_train)
    # X_test = ss_X.transform(X_test)
    # # 目标数据（房价预测值）也是数值型，所以也要标准化处理
    # # 说明一下：fit_transform与transform都要求操作2D数据，而此时的y_train与y_test都是1D的，因此需要调用reshape(-1,1)，例如：[1,2,3]变成[[1],[2],[3]]
    # y_train = ss_y.fit_transform(y_train.reshape(-1, 1))
    # y_test = ss_y.transform(y_test.reshape(-1, 1))

    '''三、创建模型和训练'''
    # 创建随机森林模型
    n_estimators=10
    my_model = RandomForestRegressor(n_estimators = n_estimators,random_state =1)
    # 把要训练的数据丢进去，进行模型训练
    my_model.fit(X_train, y_train)

    '''四、用测试集预测房价'''
    predicted_prices = my_model.predict(X_test)
    print(predicted_prices)

    #
    plt.subplot(2, 2, 1)
    plt.plot(list(range(len(y_test))), predicted_prices, label='Predicted')
    plt.plot(list(range(len(y_test))), y_test, label='Ideal')
    plt.legend()
    plt.title("RandomForestRegressor n_estimators={} (R-squared:{:.2f} MSE:{:.2f} MAE:{:.2f})".
              format(n_estimators,my_model.score(X_test, y_test),
                     mean_squared_error(y_test, predicted_prices),
                     mean_absolute_error(y_test,predicted_prices)))

    # 创建随机森林模型
    n_estimators = 20
    my_model = RandomForestRegressor(n_estimators=n_estimators, random_state=1)
    # 把要训练的数据丢进去，进行模型训练
    my_model.fit(X_train, y_train)
    predicted_prices = my_model.predict(X_test)
    # print(predicted_prices)

    plt.subplot(2, 2, 2)
    plt.plot(list(range(len(y_test))), predicted_prices, label='Predicted')
    plt.plot(list(range(len(y_test))), y_test, label='Ideal')
    plt.legend()
    plt.title("RandomForestRegressor n_estimators={} (R-squared:{:.2f} MSE:{:.2f} MAE:{:.2f})".
              format(n_estimators, my_model.score(X_test, y_test),
                     mean_squared_error(y_test, predicted_prices),
                     mean_absolute_error(y_test, predicted_prices)))

    # 创建随机森林模型
    n_estimators = 40
    my_model = RandomForestRegressor(n_estimators=n_estimators, random_state=1)
    # 把要训练的数据丢进去，进行模型训练
    my_model.fit(X_train, y_train)
    predicted_prices = my_model.predict(X_test)
    # print(predicted_prices)

    plt.subplot(2, 2, 3)
    plt.plot(list(range(len(y_test))), predicted_prices, label='Predicted')
    plt.plot(list(range(len(y_test))), y_test, label='Ideal')
    plt.legend()
    plt.title("RandomForestRegressor n_estimators={} (R-squared:{:.2f} MSE:{:.2f} MAE:{:.2f})".
              format(n_estimators, my_model.score(X_test, y_test),
                     mean_squared_error(y_test, predicted_prices),
                     mean_absolute_error(y_test, predicted_prices)))

    # 创建随机森林模型
    n_estimators = 100
    my_model = RandomForestRegressor(n_estimators=n_estimators, random_state=1)
    # 把要训练的数据丢进去，进行模型训练
    my_model.fit(X_train, y_train)
    predicted_prices = my_model.predict(X_test)
    # print(predicted_prices)
    plt.subplot(2, 2, 4)
    plt.plot(list(range(len(y_test))), predicted_prices, label='Predicted')
    plt.plot(list(range(len(y_test))), y_test, label='Ideal')
    plt.legend()
    plt.title("RandomForestRegressor n_estimators={} (R-squared:{:.2f} MSE:{:.2f} MAE:{:.2f})".
              format(n_estimators, my_model.score(X_test, y_test),
                     mean_squared_error(y_test, predicted_prices),
                     mean_absolute_error(y_test, predicted_prices)))


    Rsquared=[]
    MSE=[]
    MAE=[]
    index=list(range(1,300,10))
    print(index)
    for i in index:
        n_estimators = i
        my_model = RandomForestRegressor(n_estimators=n_estimators, random_state=1)
        # 把要训练的数据丢进去，进行模型训练
        my_model.fit(X_train, y_train)
        predicted_prices = my_model.predict(X_test)

        Rsquared.append(my_model.score(X_test, y_test))
        MSE.append(mean_squared_error(y_test, predicted_prices))
        MAE.append(mean_absolute_error(y_test, predicted_prices))

    plt.figure()
    plt.plot(index, Rsquared, label='Rsquared')
    plt.plot(index, MSE, label='MSE')
    plt.plot(index, MAE, label='MAE')
    plt.xlabel("n_estimators")
    plt.legend()

    plt.show()





if __name__=="__main__":
    path="data.xlsx"
    # loadData(path,0)
    train(path,0)