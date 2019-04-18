import numpy as np
import random
import math
import matplotlib.pyplot as plt
## kmeans algorithm
# data generation


def euler_distance(point1: list, point2: list) -> float:
    """
    计算两点之间的欧拉距离，支持多维
    """
    distance = 0.0
    for a, b in zip(point1, point2):
        distance += math.pow(a - b, 2)
    return math.sqrt(distance)

def get_closest_dist(point, centroids):
    min_dist = math.inf  # 初始设为无穷大
    for i, centroid in enumerate(centroids):
        dist = euler_distance(centroid, point)
        if dist < min_dist:
            min_dist = dist
    return min_dist

def kpp_centers(data_set: list, k: int) -> list:
    """
    从数据集中返回 k 个对象可作为质心
    """
    cluster_centers = []
    cluster_centers.append(random.choice(data_set))
    d = [0 for _ in range(len(data_set))]
    for _ in range(1, k):
        total = 0.0
        for i, point in enumerate(data_set):
            d[i] = get_closest_dist(point, cluster_centers) # 与最近一个聚类中心的距离
            total += d[i]
        total *= random.random()
        for i, di in enumerate(d): # 轮盘法选出下一个聚类中心；
            total -= di
            if total > 0:
                continue
            cluster_centers.append(data_set[i])
            break
    return cluster_centers

def ourkmean(x,k,mu):
    n,p = x.shape
    #step 1 calculate id
    dist0 = np.zeros((n,k))
    for t in range(20):
       for j in range(k):
          dist0[:,j] = np.sum((x - mu[:,j])**2,axis = 1) #加入axis=1以后就是将矩阵的每一行向量相加
       idx = np.argmin(dist0,axis = 1)
       #step 2 calculate mean
       for j in range(k):
          mu[:,j] = np.mean(x[idx==j,:])
    return idx


if __name__=="__main__":
    n = 100
    x1 = np.random.randn(n, 2)
    x2 = np.random.randn(n, 2) + [2, 2]
    x = np.vstack((x1, x2))
    # plt.hold(1)
    plt.figure()
    plt.plot(x1[:, 0], x1[:, 1], 'ro')  # 100个红点
    plt.plot(x2[:, 0], x2[:, 1], 'bo')  # 100个蓝点
    # mu is a p*k matrix


    # mu = np.array([[-1,0.2],[0.5,0.5],[1.5,1.5]]).T
    k = 3
    tmp_list=kpp_centers(x,k);
    mu=np.zeros(np.shape(tmp_list)).T
    for i in range(np.shape(tmp_list)[1]):
        for j in range(np.shape(tmp_list)[0]):
            mu[i][j]=tmp_list[j][i]
    print("centers:\n {}".format(mu))
    idx = ourkmean(x,k,mu)

    # print(kpp_centers(x,3))
    plt.figure()
    #plt.hold(1)
    plt.plot(x[idx==0,0],x[idx==0,1],'ro')
    plt.plot(x[idx==1,0],x[idx==1,1],'bo')
    plt.plot(x[idx==2,0],x[idx==2,1],'ko')
    plt.show()
