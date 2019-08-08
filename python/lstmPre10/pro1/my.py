import os
import shutil
import random

def split(path,train,test):
    if os.path.exists(train):
        shutil.rmtree(train)
    os.mkdir(train)
    if os.path.exists(test):
        shutil.rmtree(test)
    os.mkdir(test)

    counts=[108,466,368,451,230,455,86,392,488,166,46,185,349]
    cnt=0
    for i in os.listdir(path):
        nums=0
        listfiles=os.listdir(os.path.join(path,i))
        random.shuffle(listfiles)
        random.shuffle(listfiles)
        random.shuffle(listfiles)
        for j in listfiles:
            if not os.path.exists(os.path.join(train,i)):
                os.mkdir(os.path.join(train,i))
            if not os.path.exists(os.path.join(test,i)):
                os.mkdir(os.path.join(test,i))
            if nums<counts[cnt]:
                shutil.copy(os.path.join(path,i,j),os.path.join(train,i,j))
                nums+=1
            else:
                shutil.copy(os.path.join(path,i,j),os.path.join(test, i, j))
                # nums+=1
        cnt+=1


if __name__=="__main__":
    path="../data/pro1_data"
    # print(os.listdir(path))
    split(path,"../train","../test")