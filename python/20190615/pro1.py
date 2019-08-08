import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.cluster import Birch
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
import copy
from sklearn.metrics import classification_report


pingjia=["艺术馆评价",
         "艺术俱乐部评价",
         "饮品档次评价",
         "餐馆评价",
         "博物馆评价",
         "度假村评价",
         "公园评价",
         "海滩评价",
         "影剧院评价",
         "宗教机构评价"
         ]
X = None
Y = None
def readCsv(path):
    data=pd.read_csv(path)
    # print(data.values[:,1:].shape)
    return data.values[:,1:];
def myKmeans(data):
    print("*******************************Kmeans************************")
    X=data
    print(X.shape)
    tests = list(range(2,10))
    print(tests)
    scores=[]
    for t in tests:
        kmeans_model = KMeans(n_clusters=t).fit(X)
        score=metrics.silhouette_score(X,kmeans_model.labels_,metric='euclidean')
        print('K = %s, 轮廓系数 = %.03f'%(t,score))
        scores.append(score)
    plt.plot(tests,scores,"-*")
    plt.xlabel('Number of Clusters')
    plt.ylabel('Silhouette Coefficient Score')
    plt.title("Kmeans")
    plt.show()
    print(scores)
    max_index=sorted(range(len(scores)), key=lambda k: scores[k],reverse=1)
    max_k=tests[max_index[0]]
    print("轮廓系数最大的k={}".format(max_k))

def myBirch(data):
    print("*******************************Birch************************")
    X = data
    #效果不好
    # pca = PCA(3)
    # projected = pca.fit_transform(X)
    # X=projected

    print(X.shape)
    tests = list(range(2, X.shape[1]))
    print(tests)
    scores = []
    for t in tests:
        birch_model = Birch(n_clusters=t,threshold = 1).fit(X)
        score = metrics.silhouette_score(X, birch_model.labels_, metric='euclidean')
        print('K = %s, 轮廓系数 = %.03f' % (t, score))
        scores.append(score)
    plt.plot(tests, scores, "-*")
    plt.xlabel('Number of Clusters')
    plt.ylabel('Silhouette Coefficient Score')
    plt.title("Birch")
    plt.show()
    print(scores)
    max_index = sorted(range(len(scores)), key=lambda k: scores[k], reverse=1)
    max_k = tests[max_index[0]]
    print("轮廓系数最大的k={}".format(max_k))

def myPca(data):
    global Y
    X=data
    pca = PCA().fit(X)
    plt.plot(np.cumsum(pca.explained_variance_ratio_))
    plt.xlabel('number of components')
    plt.ylabel('cumulative explained variance');
    plt.title('PCA=3')
    plt.grid()
    plt.show()


    # 从10维空间降维到二维空间，进行可视化
    # from sklearn.datasets import load_digits

    pca = PCA(3)
    projected = pca.fit_transform(X)

    # 画出每个点的前3个主成份
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    birch_model = Birch(n_clusters=2, threshold=1).fit(X)
    ax.scatter(projected[:, 0], projected[:, 1],projected[:, 2],c=birch_model.labels_)
    ax.set_xlabel('component 1')
    ax.set_ylabel('component 2')
    ax.set_zlabel('component 3')
    plt.title("BIRCH k=2")
    # plt.colorbar();
    plt.show()

    # 画出每个点的前3个主成份
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    kmeans_model = KMeans(n_clusters=2).fit(X)
    ax.scatter(projected[:, 0], projected[:, 1], projected[:, 2], c=kmeans_model.labels_)
    ax.set_xlabel('component 1')
    ax.set_ylabel('component 2')
    ax.set_zlabel('component 3')
    plt.title("KMEANS k=2")
    # plt.colorbar();
    plt.show()
    Y = copy.deepcopy(kmeans_model.labels_)


def pro1(data):
    # pro1
    myKmeans(data)
    myBirch(data)
    myPca(data)

def pro2(data):

    X=data
    kmeans_model = KMeans(n_clusters=2).fit(X)
    print("Center of the cluster1:")
    print(kmeans_model.cluster_centers_[0 ,:])
    print("Center of the cluster2:")
    print(kmeans_model.cluster_centers_[1 ,:])

    #第1类每种特征的平均分
    scores=np.mean(X[kmeans_model.labels_==0,:],axis=0)
    print(scores)
    print("第1类每种特征的平均分-偏好排序,从高到低")
    print(sorted(range(len(scores)), key=lambda k: scores[k], reverse=1))
    temp = []
    for i in sorted(range(len(scores)), key=lambda k: scores[k], reverse=1):
        temp.append(pingjia[i])
    print(temp)

    # 第2类每种特征的平均分
    scores = np.mean(X[kmeans_model.labels_ == 1, :], axis=0)
    print(scores)
    print("第1类每种特征的平均分-偏好排序,从高到低")
    print(sorted(range(len(scores)), key=lambda k: scores[k], reverse=1))
    temp=[]
    for i in sorted(range(len(scores)), key=lambda k: scores[k], reverse=1):
        temp.append(pingjia[i])
    print(temp)


def pro3(data):
    thre=int(data.shape[0]*0.8)
    # print(Y)
    print("Train cases={},Test cases={}".format(thre,data.shape[0]-thre))
    train_X=data[0:thre,:];
    train_Y=Y[0:thre]

    test_X=data[thre:,:]
    test_Y = Y[thre:]


    #bayes
    print("class by bayes")
    clf = GaussianNB()
    clf.fit(train_X, train_Y);
    print("Predict result by bayes")
    y_pred=clf.predict(test_X);
    y_true=test_Y
    print(classification_report(y_true, y_pred))

    #Knn
    print("Class by knn")
    knn = KNeighborsClassifier()
    knn.fit(train_X, train_Y);
    print("Predict result by bayes")
    y_pred = knn.predict(test_X);
    y_true = test_Y
    print(classification_report(y_true, y_pred))


if __name__=="__main__":
    path="data.csv"
    data=readCsv(path)

    #problem1
    print("********************pro1*******************")
    pro1(data)

    #problem2
    print("********************pro2*******************")
    pro2(data)

    #problem3
    print("********************pro3*******************")
    pro3(data)

