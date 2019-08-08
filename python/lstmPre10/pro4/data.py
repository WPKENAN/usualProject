import scipy.io as scio
import os
import numpy as np
import shutil
import pandas as pd
# import tqdm
# def pro1(path,targetFolder):
#     list_dirs = os.walk(path)
#     for root, dirs, files in list_dirs:
#         for f in files:
#             if "导" in root:
#                 city = root.split('\\')[1]
#                 if not os.path.exists(os.path.join(targetFolder,city)):
#                     os.mkdir(os.path.join(targetFolder,city))
#                 print(os.path.join(root, f))
#                 shutil.copy(os.path.join(root, f),os.path.join(targetFolder,city,f))

def csvTonNumpy(path):
    classNames = sorted(os.listdir(path))

    dictName = {}
    for i in range(len(classNames)):
        dictName[classNames[i]] = i
    print(dictName)

    count = 0;
    # n=6
    for classname in classNames:
        print(classname)
        folder = os.path.join(path, classname)
        for basename in os.listdir(folder):
            file = os.path.join(folder, basename)
            print(file)
            data = pd.read_csv(file, header=-1).values[:, 1]
            x = np.reshape(data, (1, len(data)))
            y = np.zeros((x.shape[0], 1)) + dictName[classname]
            # print(file)
            # print(data.shape)
            if count == 0:
                allX = x;
                allY = y;
            else:
                allX = np.vstack((allX, x))
                allY = np.vstack((allY, y))
            count += 1
            print(count/8827)


    np.save(path+'/../allX.npy',allX)
    np.save(path+'/../allY.npy', allY)
    # print(allY)
    print(allX.shape)
    print(allY.shape)

# def pro2(path,targetFolder):
#     years=['2014','2015','2016','2017'];
#     list_dirs = os.walk(path)
#     for root, dirs, files in list_dirs:
#         for f in files:
#             if "导" in root:
#                 city = root.split('\\')[1]
#                 if not os.path.exists(os.path.join(targetFolder, city)):
#                     os.mkdir(os.path.join(targetFolder, city))
#                 for year in years:
#                     if year in root:
#                         break;
#                 if not os.path.exists(os.path.join(targetFolder, city,year)):
#                     os.mkdir(os.path.join(targetFolder, city,year))
#                 print(os.path.join(root, f))
#                 shutil.copy(os.path.join(root, f), os.path.join(targetFolder, city, year,f))

def mergeFolder(path1,path2,target):
    if os.path.exists(target):
        shutil.rmtree(target)
    os.mkdir(target)

    for city in os.listdir(path1):
        if os.path.exists(os.path.join(target,city)):
            shutil.rmtree((os.path.join(target,city)))
        os.mkdir(os.path.join(target,city))
    for city in os.listdir(path2):
        if os.path.exists(os.path.join(target,city)):
            shutil.rmtree((os.path.join(target,city)))
        os.mkdir(os.path.join(target,city))

    count=0;
    for city in os.listdir(path1):
        for file in os.listdir(os.path.join(path1,city)):
            if '-1 .' in file:
                shutil.copy(os.path.join(path1,city,file),os.path.join(target,city,file))

    for city in os.listdir(path2):
        for file in os.listdir(os.path.join(path2,city)):
            shutil.copy(os.path.join(path2,city,file),os.path.join(target,city,file))

def outTxt(path):

    classNames = sorted(os.listdir(path))

    dictName = {}
    for i in range(len(classNames)):
        dictName[classNames[i]] = i
    print(dictName)

    count = 0;
    # n=6
    files=[]
    for classname in classNames:
        print(classname)
        folder = os.path.join(path, classname)
        for basename in os.listdir(folder):
            file = os.path.join(folder, basename)
            files.append(os.path.join(classname,basename))
    files=np.array(files)
    import random
    random.seed(0)
    index = list(range(len(files)));
    random.shuffle(index)
    files=files[index]
    val = 0.79
    x_train = files[0:int(len(files) * val)]
    x_test = files[int(len(files) * val):]

    trainFolder=path+"/../train"
    testFolder=path+"/../test"
    if os.path.exists(trainFolder):
        shutil.rmtree(trainFolder)
    os.mkdir(trainFolder)
    if os.path.exists(testFolder):
        shutil.rmtree(testFolder)
    os.mkdir(testFolder)

    for i in x_train:
        classname=i.split('\\')
        print(classname)
        file=open(trainFolder+"/"+classname[0]+".txt","a+")
        file.write(classname[1]+"\n")
        file.close()

    for i in x_test:
        classname=i.split('\\')
        print(classname)
        file=open(testFolder+"/"+classname[0]+".txt","a+")
        file.write(classname[1]+"\n")
        file.close()


if __name__=='__main__':
    # path1="D:\github\Data\烟草红外\\20190715"
    # path2="D:\github\Data\烟草红外\\20190716"
    # target="D:\github\Data\烟草红外\\data"
    # mergeFolder(path1,path2,target)
    target="D:\github\Data\烟草红外\一阶导数数据"
    #csvTonNumpy(target)
    outTxt(target)

    #
    # # pro1(path,"./data/pro1_data")
    # csvTonNumpy("./data/pro1_data")

    # pro2(path, "./data/pro2_data")
    # for folder in os.listdir("./data/pro2_data"):
    #     csvTonNumpy(os.path.join("./data/pro2_data",folder))






