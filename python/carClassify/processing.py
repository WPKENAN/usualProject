import os
import scipy.io as scio
import numpy as np
import shutil



if __name__=="__main__":

    imgFile="D:\\github\\Data\\BITVehicle_Dataset"
    target="D:\\github\\Data\\carClassify"
    data = scio.loadmat("D:\\github\\Data\\BITVehicle_Dataset\\VehicleInfo.mat")
    # print(data['VehicleInfo'][8][0][3])


    labels={}
    for i in range(len(data['VehicleInfo'])):
        # print(data['VehicleInfo'][i]['name'][0][0])
        if data['VehicleInfo'][i]['nVehicles'][0][0][0]>1:
            print(imgFile + "\\" + data['VehicleInfo'][i]['name'][0][0])
            print(data['VehicleInfo'][i]['nVehicles'][0][0][0])
        else:
            label=data['VehicleInfo'][i]['vehicles'][0]['category'][0][0][0].upper()
            if label not in labels:
                labels[label]=[0,[]];
            else:
                labels[label][0]=labels[label][0]+1;
                labels[label][1].append(data['VehicleInfo'][i]['name'][0][0])


    i=0
    for key in labels.keys():
        if os.path.exists(target+"\\"+key):
            shutil.rmtree(target+"\\"+key)
        os.mkdir(target+"\\"+key)

        for item in labels[key][1]:
            shutil.copy(imgFile + "\\" + item,target + "\\" + key+"\\"+item)
            i+=1
            print(i)

    # print(data['VehicleInfo'][8]['vehicles'][0])





