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

def loadData(path,header,i):
    data=processingData.readXlsx(path,header);
    # print(data.shape)
    xindex=[]
    for j in range(data.shape[1]):
        if j==i:
            continue
        else:
            xindex.append(j)


    x,y=data[:,xindex],data[:,i]
    # print(x,y)
    # print(y)
    print(xindex)
    return x,y;

    # return X_train, X_test, y_train, y_test

def performance_metric(y_true,y_predict):
    '''计算实际值与预测值的R2分数'''
    score = r2_score(y_true,y_predict)
    return score


def train(path,header,pre_index):
    x,y=loadData(path,header,pre_index);
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

    # 3.使用径向基核函数配置的支持向量机进行回归训练并预测
    rbf_svr = SVR(kernel='rbf')
    rbf_svr.fit(X_train, y_train)
    rbf_svr_y_predict = rbf_svr.predict(X_test)

    return rbf_svr,rbf_svr_y_predict,ss_y,X_test,y_test


if __name__=="__main__":
    path="data.xlsx"
    # loadData(path,0)
    from pylab import mpl

    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    names = ["热源温度K", "环境温度K", "冷凝水温度", "蒸发温度", "蒸发压力", "冷凝温度", "冷凝压力", "工质泵等熵效率", "膨胀机等熵效率", "过热度"];
    for i in range(10):
        if i%5==0:
            plt.figure()
        rbf_svr, rbf_svr_y_predict, ss_y, X_test, y_test=train(path,0,i)
        plt.subplot(3, 2, i%5+1)
        plt.plot(list(range(len(y_test))), ss_y.inverse_transform(rbf_svr_y_predict), label='Predicted')
        plt.plot(list(range(len(y_test))), ss_y.inverse_transform(y_test), label='Ideal')
        plt.legend()
        plt.title("{} RBF-SVR (R-squared:{:.2f} MSE:{:.2f} MAE:{:.2f})".
                  format(names[i],rbf_svr.score(X_test, y_test),
                         mean_squared_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(rbf_svr_y_predict)),
                         mean_absolute_error(ss_y.inverse_transform(y_test),
                                             ss_y.inverse_transform(rbf_svr_y_predict))))
    plt.show()

