#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 15:01:23 2018

@author: yetta
"""
#print(__doc__)

import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth

# #############################################################################
# Generate sample data
centers = [[1, 1], [-1, -1], [1, -1]]
filepath1 = 'C:/Users\Anzhi\Desktop\github\Data\DEAP\DEAP\EEG_feature.txt'  # 数据文件路径
filepath2 = 'C:/Users\Anzhi\Desktop\github\Data\DEAP\DEAP\\valence_arousal_label.txt'
x = np.loadtxt(filepath1,dtype=float,delimiter='\t')
ytemp = np.loadtxt(filepath2,dtype=float,delimiter='\t')
y ,a= np.split(ytemp,(1,),axis=1)
y = np.squeeze(y)
# #############################################################################
# Compute clustering with MeanShift

# The following bandwidth can be automatically detected using
# bandwidth = estimate_bandwidth(x, quantile=0.1,n_samples=500)

# print(bandwidth)
ms = MeanShift(bandwidth=10, bin_seeding=False)
ms.fit(x)
labels = ms.labels_
labels = np.squeeze(labels)
cluster_centers = ms.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)

print("number of estimated clusters : %d" % n_clusters_)
print(labels)
print(y)

j=0
print(np.shape(x))
print(np.shape(labels))
print(np.shape(y))
'''
for i in range(160):
    if labels[1,i]==(y[1,i]+1):
        j=j+1
        
temp = j/160
print(temp)
'''
# #############################################################################
# Plot result
import matplotlib.pyplot as plt
from itertools import cycle

plt.figure(1)
plt.clf()

colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
print(len(cluster_centers))
for k, col in zip(range(n_clusters_), colors):
    my_members = labels == k
    cluster_center = cluster_centers[k]
    plt.plot(x[my_members, 0], x[my_members, 1], col + '.')
    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=14)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()