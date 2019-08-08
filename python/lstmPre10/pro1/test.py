# coding:UTF-8
'''
Created on 2015年5月12日
@author: zhaozhiyong
'''

import scipy.io as scio

dataFile = './data/9.mat'
data = scio.loadmat(dataFile)
print(data.keys())
keys=[]
for key in data.keys():
    keys.append(key)

print(keys)
