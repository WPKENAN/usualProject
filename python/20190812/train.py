import pandas as pd
import sklearn
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
if __name__=="__main__":
    df=pd.read_csv("./analysis.csv",header=1)
    true=df.values[:20,16:19]
    false=df.values[:20,34:37]


    data=np.zeros((len(true)+len(false),4))

    print(data.shape)
    for i in range(len(true)):
        data[i,0:3]=true[i]
        data[i,3]=1
    for i in range(len(false)):
        data[i+len(true),0:3]=false[i]
        data[i+len(true),3]=0
    print(data)

    from sklearn import svm
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    # clf = svm.SVC()
    x=data[:,0:3]
    y=data[:,3]
    #

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    t=1;
    f=1;
    for i in range(len(x)):
        if y[i]==0:
            if f:
                f=0
                ax.scatter(x[i,0]/x[i,1],x[i,1]/x[i,2],x[i,2]/x[i,0],color='b',label="false")
            else:
                ax.scatter(x[i,0]/x[i,1],x[i,1]/x[i,2],x[i,2]/x[i,0], color='b')
        else:
            if t:
                t=0
                ax.scatter(x[i,0]/x[i,1],x[i,1]/x[i,2],x[i,2]/x[i,0], color='r', label="true")
            else:
                ax.scatter(x[i,0]/x[i,1],x[i,1]/x[i,2],x[i,2]/x[i,0], color='r')
    ax.set_xlabel('sigma1/sigma2',fontsize=20)  # 坐标轴
    ax.set_ylabel('sigma2/sigma3',fontsize=20)
    ax.set_zlabel('sigma3/sigma1',fontsize=20)
    plt.legend(fontsize=20)
    # plt.show()

    np.random.seed(0)
    index=list(range(len(x)))
    np.random.shuffle(index)

    x=x[index][:]
    y=y[index][:]

    for i in range(len(x)):
        x[i,:]=np.array([x[i,0]/x[i,1],x[i,1]/x[i,2],x[i,2]/x[i,0]])
    print(x)
    # x=x[:,0]


    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, train_size=0.6)
    # clf.fit(x, y)

    clf = svm.SVC(kernel='rbf')
    clf.fit(x_train, y_train.ravel())

    print(clf.score(x_train, y_train))  # 精度
    print('训练集准确率：', accuracy_score(y_train, clf.predict(x_train)))
    print(clf.score(x_test, y_test))
    print('测试集准确率：', accuracy_score(y_test, clf.predict(x_test)))


    # print(true)

    # print(type(true))