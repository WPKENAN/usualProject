import numpy as np
import pandas as pd
header = ['userId','itemId','rating','timestamp']
df = pd.read_csv('./data/ml-latest/ratings.csv',
                sep=',',names=header,header=0)
# print(df)
# users_unique=df.userId.unique()
# items_unique=df.itemId.unique()
# n_users = users_unique.shape[0]
# n_items = items_unique.shape[0]
#
# itemId2uniqueId={}
# uniqueId2itemId={}
# count=1
# for i in range(len(df.itemId)):
#     if i%10000==0:
#         print(i)
#     if df.itemId[i] not in itemId2uniqueId:
#         itemId2uniqueId[df.itemId[i]]=count
#         uniqueId2itemId[count]=df.itemId[i]
#         count+=1
#
# #print(df.itemId.unique())
# print('Number of users = ' + str(n_users) + ' | Number of movies = ' + str(n_items))