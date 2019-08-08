import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.svm import SVR
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from sklearn.svm import SVC

index=np.array([2,3,4,5,6,7,8,9,10,15])-1;
def readTrain(path,header=None):
    df=pd.read_csv(path,header=header);
    data=df.values

    train_y=data[:,-1];
    class_le = LabelEncoder();
    train_y=class_le.fit_transform(train_y);

    train_x = data[:, 0:-1];
    le=[]
    for i in range(len(index)):
        le.append(LabelEncoder())
        train_x[:, index[i]]=le[i].fit_transform(train_x[:,index[i]])

    ohe=OneHotEncoder(categorical_features=index.tolist());
    train_x=ohe.fit_transform(train_x).toarray()

    np.random.seed(10)
    x=[]
    y=[]
    for i in range(1,len(train_y)):
        if np.random.random()<0.11369757599076567 and train_y[i]==0 or train_y[i]==1:
            x.append(train_x[i,:].tolist())
            y.append(train_y[i])



    # print(train_x[25:28,:])

    return le,class_le,ohe,np.array(x),np.array(y)

def pro1(x,y,outX):
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=1)

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

    print("start")
    # 3.使用径向基核函数配置的支持向量机进行回归训练并预测
    rbf_svr = SVR(kernel='rbf')
    rbf_svr.fit(X_train, y_train)
    print("fit over")
    rbf_svr_y_predict = rbf_svr.predict(X_test)

    # 3.径向基核函数配置的SVR
    print('R-squared value of RBF SVR is', rbf_svr.score(X_test, y_test))
    print('the MSE of RBF SVR is',
          mean_squared_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(rbf_svr_y_predict)))
    print('the MAE of RBF SVR is',
          mean_absolute_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(rbf_svr_y_predict)))

    plt.scatter(list(range(len(y_test))), np.round(ss_y.inverse_transform(rbf_svr_y_predict))-0.1, label='Predicted')
    plt.scatter(list(range(len(y_test))), np.round(ss_y.inverse_transform(y_test)), label='Ideal')
    plt.legend()
    plt.title("RBF SVR (R-squared:{:.2f} MSE:{:.2f} MAE:{:.2f})".
              format(rbf_svr.score(X_test, y_test),
                     mean_squared_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(rbf_svr_y_predict)),
                     mean_absolute_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(rbf_svr_y_predict))))

    pre=np.round(np.abs(ss_y.inverse_transform(rbf_svr_y_predict)))
    # print(pre)
    p=0
    for i in range(len(y_test)):  # 循环检测测试数据分类成功的个数
        if pre[i] == np.round(np.abs(ss_y.inverse_transform(y_test)[i])):
            p += 1

    print(p / len(y_test))  # 输出测试集准确率

    print("predict result!!!!!!!!!!")
    outX = ss_X.transform(outX)
    outY=np.round(np.abs(ss_y.inverse_transform(rbf_svr.predict(outX))))
    print(outY.shape)
    predictY = pd.DataFrame(outY)
    predictY.to_csv('Results_1.csv', encoding='utf-8', index=False, header=False)
    plt.show()

def pro2(x,y,outX):
    clf = SVC(kernel='rbf')  # 调参
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=1)
    clf.fit(X_train, y_train)  # 训练
    print(clf.fit(X_train, y_train))  # 输出参数设置
    p = 1  # 正确分类的个数
    print("start cal")
    for i in range(len(y_test)):  # 循环检测测试数据分类成功的个数
        if clf.predict(X_test[i,:].reshape(1, -1)) == y_test[i]:
            p += 1

    print(p / len(y_test))  # 输出测试集准确率

    print("predict result!!!!!!!!!!")
    # outX = ss_X.transform(outX)
    outY = clf.predict(outX)
    print(outY.shape)
    predictY = pd.DataFrame(outY)
    predictY.to_csv('Results_1.csv', encoding='utf-8', index=False, header=False)





def train(train_x,train_y,outX):
    x=train_x;
    y=train_y;
    pro1(x,y,outX)
    # pro2(x,y,outX)


    # print(x.shape)
    # print(y)

if __name__=="__main__":
    trainPath="Train.csv"
    testPath="Test.csv";
    le, class_le, ohe, train_x, train_y=readTrain(trainPath,0)
    # print(train_x[0,:])
    # print(train_x.shape)


    #read outX
    df = pd.read_csv(testPath, header=0);
    data = df.values
    outX = data;
    for i in range(len(index)):
        outX[:, index[i]] = le[i].transform(outX[:, index[i]])

    outX=ohe.transform(outX).toarray()
    # print(outX[25:28,:])

    train(train_x,train_y,outX)
