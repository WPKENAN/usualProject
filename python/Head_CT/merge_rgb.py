import re
import pandas as pd
import os
import shutil
import cv2 as cv
import copy
import numpy as np

def getDict(excel):
    m, n = excel.shape
    data={}
    for i in range(m):
        nums=excel[i,1].split('_')
        key=str(excel[i,0])+"-";
        for num in nums:
            key+=str(int(num))+"_"
        key=key.strip('_')
        data[key]=excel[i,-1]

    # print(data)
    return data

def read(path):
    print(path)
    img=cv.imread(path,cv.IMREAD_GRAYSCALE)
    img=cv.resize(img,(512,512))
    return copy.deepcopy(img)


def merge(imgs):
    result=imgs[0]
    for i in range(1,len(imgs)):
        result=np.dstack((result,imgs[i]))

    return result


def toImage(dic,imagePath,clas):
    keys=list(dic.keys())
    for i in range(1,len(keys)-1):
        key=keys[i]

        folder=key.split('-')[0]
        file=key.split('-')[1]

        # print(key)
        if not (os.path.exists(os.path.join(imagePath,folder,file+".jpg")) or os.path.exists(os.path.join(imagePath,folder,file+".jpg"))):
            print(os.path.join(imagePath,folder,file+".jpg"))
            continue
        if not (os.path.exists(os.path.join(imagePath,keys[i - 1].split('-')[0],keys[i - 1].split('-')[1]+".jpg"))
                or os.path.exists(os.path.join(imagePath,keys[i - 1].split('-')[0],keys[i - 1].split('-')[1]+".jpg"))):
            print(os.path.join(imagePath,folder,file+".jpg"))
            continue

        if not (os.path.exists(os.path.join(imagePath,keys[i + 1].split('-')[0],keys[i + 1].split('-')[1]+".jpg"))
                or os.path.exists(os.path.join(imagePath,keys[i + 1].split('-')[0],keys[i + 1].split('-')[1]+".jpg"))):
            print(os.path.join(imagePath,folder,file+".jpg"))
            continue

        if keys[i - 1].split('-')[0] == folder and keys[i + 1].split('-')[0] == folder:
            if os.path.exists(os.path.join(imagePath, folder, file + ".jpg")):
                img1 = read(os.path.join(imagePath, folder, file + ".jpg"))
            else:
                pass
                img1 = read(os.path.join(imagePath, folder, file + ".gif"))

            if os.path.exists(os.path.join(imagePath,keys[i - 1].split('-')[0],keys[i - 1].split('-')[1]+".jpg")):
                img2 = read(os.path.join(imagePath,keys[i - 1].split('-')[0],keys[i - 1].split('-')[1]+ ".jpg"))
            else:
                pass
                img2 = read(os.path.join(imagePath,keys[i - 1].split('-')[0],keys[i - 1].split('-')[1]+ ".gif"))

            if os.path.exists(os.path.join(imagePath,keys[i +1].split('-')[0],keys[i + 1].split('-')[1]+ ".jpg")):
                img3 = read(os.path.join(imagePath,keys[i + 1].split('-')[0],keys[i + 1].split('-')[1]+ ".jpg"))
            else:
                pass
                img3 = read(os.path.join(imagePath,keys[i + 1].split('-')[0],keys[i + 1].split('-')[1]+ ".gif"))

            result = merge([img1, img2, img3])

            if dic[keys[i]] + dic[keys[i-1]] +dic[keys[i+1]] >= 2:
                cv.imwrite(os.path.join("./image/{}/{}.jpg".format(clas,key)),result)
            else:
                cv.imwrite(os.path.join("./image/normal/{}.jpg".format(key)), result)

if __name__=="__main__":
    addexcelpath="./data/add.xlsx"
    subexcelpath="./data/sub.xlsx"
    addimagepath="./data/add"
    subimagepath="./data/sub"

    addexcel=pd.read_excel(addexcelpath).values[:,1:4];
    subexcel=pd.read_excel(subexcelpath).values[:,1:4]

    print(addexcel.shape)
    add=getDict(addexcel)
    sub=getDict(subexcel)

    # print(list(add.keys()))
    # keys=list(add.keys())
    print(sub.keys())
    toImage(add, subimagepath,'add')

    toImage(sub,addimagepath,'sub')















