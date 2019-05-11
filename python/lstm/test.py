import numpy
import matplotlib.pyplot as plt
from pandas import read_csv
import math

cityframe=read_csv('C:\\Users\Anzhi\Documents\Tencent Files\\3272346474\FileRecv\\month_rate.csv', usecols=[1], engine='python', skipfooter=0)
dataframe = read_csv('C:\\Users\Anzhi\Documents\Tencent Files\\3272346474\FileRecv\\month_rate.csv', usecols=[5], engine='python', skipfooter=0)
# dataframe = read_csv('D:\github\\usualProject\python\lstm\\test.csv', usecols=[1], engine='python', skipfooter=3)

city=input("please in put FZDBM: ");
city=city.upper();
citys=cityframe.values;
datasets = dataframe.values
# 将整型变为float
datasets = datasets.astype('float32')


dataset=numpy.zeros((sum(citys==city)[0],1))
print("总共找到 {} 个历史数据".format(sum(citys==city)[0]))
count=0;
for i in range(len(citys)):
    if citys[i]==city:
        dataset[count]=datasets[i]
        count=count+1;




