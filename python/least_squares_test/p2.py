from sklearn.datasets.samples_generator import make_blobs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
#%matplotlib inline

from sklearn.cluster import KMeans


def readcsv(path):
    contents=pd.read_csv(path)
    xy=contents.values
    x=xy[:,0:2]
    y=xy[:,2]
    return x,y



if __name__=="__main__":
    path="./data.csv"
    x,y=readcsv(path)

    plt.scatter(x[:, 0], x[:, 1], marker='o')
    plt.show()

    y_pred = KMeans(n_clusters=4, random_state=9).fit_predict(x)
    plt.scatter(x[:, 0], x[:, 1], c=y_pred)
    plt.show()

