import scipy.io as scio
import os
import numpy as np
import shutil
import pandas as pd

def pro1(path,targetFolder):
    if not os.path.exists(targetFolder):
        os.mkdir(targetFolder)
    list_dirs = os.walk(path)
    for root, dirs, files in list_dirs:
        for f in files:
            if "导" in root:
                city = root.split('\\')[1]
                if not os.path.exists(os.path.join(targetFolder,city)):
                    os.mkdir(os.path.join(targetFolder,city))
                print(os.path.join(root, f))
                shutil.copy(os.path.join(root, f),os.path.join(targetFolder,city,f))

def csvTonNumpy(path):
    # print(sorted(os.listdir("../raw_data")))
    classNames = sorted(os.listdir(path))
    print(classNames)

    dictName = {}
    for i in range(len(classNames)):
        dictName[classNames[i]] = i
    print(dictName)

    count = 0;
    for classname in classNames:
        folder = os.path.join(path, classname)
        for basename in os.listdir(folder):
            file = os.path.join(folder, basename)
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
            print(count)


    np.save('allX.npy',allX)
    np.save('allY.npy', allY)
    print(allY)
    print(allX.shape)
    print(allY.shape)

def pro2(path,targetFolder):
    years=['2014','2015','2016','2017'];
    list_dirs = os.walk(path)
    for root, dirs, files in list_dirs:
        for f in files:
            if "导" in root:
                city = root.split('\\')[1]
                if not os.path.exists(os.path.join(targetFolder, city)):
                    os.mkdir(os.path.join(targetFolder, city))
                for year in years:
                    if year in root:
                        break;
                if not os.path.exists(os.path.join(targetFolder, city,year)):
                    os.mkdir(os.path.join(targetFolder, city,year))
                print(os.path.join(root, f))
                shutil.copy(os.path.join(root, f), os.path.join(targetFolder, city, year,f))

if __name__=='__main__':
    path="./raw_data"
    #
    # pro1(path,"./data/pro1_data")
    csvTonNumpy("./data/pro1_data")

    # pro2(path, "./data/pro2_data")
    # for folder in os.listdir("./data/pro2_data"):
    #     csvTonNumpy(os.path.join("./data/pro2_data",folder))






