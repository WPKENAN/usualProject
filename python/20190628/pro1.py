import random
import numpy as np
threshold=0.5
scale=100000;

arr=[]
random.seed(0)
for i in range(scale):
    if random.random()>threshold:
        arr.append(1);
    else:
        arr.append(0)
arr=np.array(arr)
print(np.sum(arr))

random.seed(1)
val=0.0001;

count=0;
for i in range(scale):
    # temp=np.random.normal(0,1,1)
    temp=random.random()
    # temp=np.random.random()
    # temp=np.random.weibull(10,1)
    # print(temp)
    if temp>val and arr[i]==1 or temp<=val and arr[i]==0:
        count+=1;
print(count/scale)





