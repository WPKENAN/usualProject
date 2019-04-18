import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
from scipy.spatial import KDTree
import sklearn.cluster as skc  # 密度聚类
import math
import random
from sklearn.cluster import KMeans

# visitlist类用于记录访问列表
# unvisitedlist记录未访问过的点
# visitedlist记录已访问过的点
# unvisitednum记录访问过的点数量
class visitlist:
    def __init__(self, count=0):
        self.unvisitedlist=[i for i in range(count)]
        self.visitedlist=list()
        self.unvisitednum=count

    def visit(self, pointId):
        self.visitedlist.append(pointId)
        self.unvisitedlist.remove(pointId)
        self.unvisitednum -= 1

def  dist(a, b):
    # 计算a,b两个元组的欧几里得距离
    return math.sqrt(np.power(a-b, 2).sum())

def my_dbscanl(dataSet, eps, minPts):
    # numpy.ndarray的 shape属性表示矩阵的行数与列数
    nPoints = dataSet.shape[0]
    # (1)标记所有对象为unvisited
    # 在这里用一个类vPoints进行买现
    vPoints = visitlist(count=nPoints)
    # 初始化簇标记列表C,簇标记为 k
    k = -1
    C = [-1 for i in range(nPoints)]
    while(vPoints.unvisitednum > 0):
        # (3)随机上选择一个unvisited对象p
        p = random.choice(vPoints.unvisitedlist)
        # (4)标记p为visited
        vPoints.visit(p)
        # (5)if p的$\varepsilon$-邻域至少有MinPts个对象
        # N是p的$\varepsilon$-邻域点列表
        N = [i for i in range(nPoints) if dist(dataSet[i], dataSet[p])<= eps]
        if  len(N) >= minPts:
            # (6)创建个新簇C，并把p添加到C
            # 这里的C是一个标记列表，直接对第p个结点进行赋植
            k += 1
            C[p]=k
            # (7)令N为p的ε-邻域中的对象的集合
            # N是p的$\varepsilon$-邻域点集合
            # (8) for N中的每个点p'
            for p1 in N:
                # (9) if p'是unvisited
                if p1 in vPoints.unvisitedlist:
                    # (10)标记p’为visited
                    vPoints.visit(p1)
                    # (11) if p'的$\varepsilon$-邻域至少有MinPts个点，把这些点添加到N
                    # 找出p'的$\varepsilon$-邻域点，并将这些点去重添加到N
                    M=[i for i in range(nPoints) if dist(dataSet[i], \
                        dataSet[p1]) <= eps]
                    if len(M) >= minPts:
                        for i in M:
                            if i not in N:
                                N.append(i)
                    # (12) if p'还不是任何簇的成员，把P'添加到C
                    # C是标记列表，直接把p'分到对应的簇里即可
                    if  C[p1] == -1:
                        C[p1]= k
        # (15)else标记p为噪声
        else:
            C[p]=-1

    # (16)until没有标t己为unvisitedl内对象
    return C

def my_dbscan2(dataSet, eps, minPts):
    # numpy.ndarray的 shape属性表示矩阵的行数与列数
    # 行数即表小所有点的个数
    nPoints = dataSet.shape[0]
    # (1) 标记所有对象为unvisited
    # 在这里用一个类vPoints进行实现
    vPoints = visitlist(count=nPoints)
    # 初始化簇标记列表C，簇标记为 k
    k = -1
    C = [-1 for i in range(nPoints)]
    # 构建KD-Tree，并生成所有距离<=eps的点集合
    kd = KDTree(dataSet)
    while(vPoints.unvisitednum>0):
        # (3) 随机选择一个unvisited对象p
        p = random.choice(vPoints.unvisitedlist)
        # (4) 标t己p为visited
        vPoints.visit(p)
        # (5) if p 的$\varepsilon$-邻域至少有MinPts个对象
        # N是p的$\varepsilon$-邻域点列表
        N = kd.query_ball_point(dataSet[p], eps)
        if len(N) >= minPts:
            # (6) 创建个一个新簇C，并把p添加到C
            # 这里的C是一个标记列表，直接对第p个结点进行赋值
            k += 1
            C[p] = k
            # (7) 令N为p的$\varepsilon$-邻域中的对象的集合
            # N是p的$\varepsilon$-邻域点集合
            # (8) for N中的每个点p'
            for p1 in N:
                # (9) if p'是unvisited
                if p1 in vPoints.unvisitedlist:
                    # (10) 标记p'为visited
                    vPoints.visit(p1)
                    # (11) if p'的$\varepsilon$-邻域至少有MinPts个点，把这些点添加到N
                    # 找出p'的$\varepsilon$-邻域点，并将这些点去重新添加到N
                    M = kd.query_ball_point(dataSet[p1], eps)
                    if len(M) >= minPts:
                        for i in M:
                            if i not in N:
                                N.append(i)
                    # (12) if p'还不是任何簇的成员，把p'添加到c
                    # C是标记列表，直接把p'分到对应的簇里即可
                    if C[p1] == -1:
                        C[p1] = k
                    # (15) else标记p为噪声
                    else:
                        C[p1] = -1

    # (16) until没有标记为unvisited的对象
    return C


def kmeans(data, k=2):
    def _distance(p1, p2):
        """
        Return Eclud distance between two points.
        p1 = np.array([0,0]), p2 = np.array([1,1]) => 1.414
        """
        tmp = np.sum((p1 - p2) ** 2)
        return np.sqrt(tmp)

    def _rand_center(data, k):
        """Generate k center within the range of data set."""
        n = data.shape[1]  # features
        centroids = np.zeros((k, n))  # init with (0,0)....
        for i in range(n):
            dmin, dmax = np.min(data[:, i]), np.max(data[:, i])
            centroids[:, i] = dmin + (dmax - dmin) * np.random.rand(k)
        return centroids

    def _converged(centroids1, centroids2):

        # if centroids not changed, we say 'converged'
        set1 = set([tuple(c) for c in centroids1])
        set2 = set([tuple(c) for c in centroids2])
        return (set1 == set2)

    n = data.shape[0]  # number of entries
    centroids = _rand_center(data, k)
    label = np.zeros(n, dtype=np.int)  # track the nearest centroid
    assement = np.zeros(n)  # for the assement of our model
    converged = False

    while not converged:
        old_centroids = np.copy(centroids)
        for i in range(n):
            # determine the nearest centroid and track it with label
            min_dist, min_index = np.inf, -1
            for j in range(k):
                dist = _distance(data[i], centroids[j])
                if dist < min_dist:
                    min_dist, min_index = dist, j
                    label[i] = j
            assement[i] = _distance(data[i], centroids[label[i]]) ** 2

        # update centroid
        for m in range(k):
            centroids[m] = np.mean(data[label == m], axis=0)
        converged = _converged(old_centroids, centroids)
    return centroids, label, np.sum(assement)

def readTxt(path):
    id_log_lat=[]
    lines=open(path,encoding="utf-16").readlines();
    # print(chardet.detect(lines))
    for i in range(len(lines)):
        lines[i]=lines[i].split('\t');
        if lines[i][0].split('-')[-1].isdigit():
            id_log_lat.append([eval(lines[i][0].split('-')[-1]),eval(lines[i][1]),eval(lines[i][2])])


    print(len(id_log_lat))
    print(id_log_lat)
    return id_log_lat



def main():
    # path="D:\\wp\\微信文件夹\\WeChat Files\\WPKENAN\FileStorage\\File\\2019-04\\daxuechengtxt\\10kV博东线环网柜.txt"
    # readTxt(path)
    textDict={}
    folder="D:\wp\微信文件夹\WeChat Files\\WPKENAN\\FileStorage\File\\2019-04\\daxuechengtxt"
    for file in os.listdir(folder):
        if file[-3:]=='txt':
            path=folder+"\\"+file
            # print(path)
            textDict[file]=np.array(readTxt(path))

    matplotlib.rcParams['font.family'] = 'SimHei'
    allPoints=np.zeros((0,2))
    # count=0
    plt.figure()
    plt.subplot(221)
    for item in textDict:
        # print(textDict[item])
        allPoints=np.concatenate((allPoints,textDict[item][:,1:3]))
        # count=count+textDict[item].shape[0];
        plt.scatter(textDict[item][:,1],textDict[item][:,2],label=item)
    plt.title("初始类别")
    # plt.legend()
    # plt.show()
    # print(count)
    print(allPoints.shape)



    #dbscan
    # plt.subplot(122)
    # X=allPoints
    # C1 = my_dbscan2(X, 0.1, 2)
    # plt.scatter(X[:, 0], X[:, 1], c=C1, marker='.')
    # plt.show()

    #dbscan2
    plt.subplot(222)
    X = allPoints
    db = skc.DBSCAN(eps=0.0009, min_samples=2).fit(X)
    labels = db.labels_
    plt.scatter(X[:, 0], X[:, 1], c=labels, marker='.')
    plt.title("DBSCAN")
    print(len(set(labels)))
    # plt.show()


    #kmeans
    # X = allPoints
    # centroids, label, _=kmeans(X,k=10);
    # plt.scatter(X[:,0],X[:,1],c=label,marker='.')
    # plt.show()


    #kmeans_ski
    # 假如我要构造一个聚类数为的聚类器
    plt.subplot(223)
    X=allPoints
    estimator = KMeans(n_clusters=20)  # 构造聚类器
    estimator.fit(X)  # 聚类
    label_pred = estimator.labels_  # 获取聚类标签
    centroids = estimator.cluster_centers_  # 获取聚类中心
    inertia = estimator.inertia_  # 获取聚类准则的总和

    plt.scatter(X[:, 0], X[:, 1], c=label_pred, marker='.')
    plt.scatter(centroids[:,0],centroids[:,1],marker='o',c="r")
    plt.title("KMEANS")
    plt.savefig("result.png")
    plt.show()

if __name__=="__main__":
    main()
