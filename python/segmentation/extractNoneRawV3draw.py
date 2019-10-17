import os
import sys
import shutil


def crop3Ddraw(v3dexe,cropdll,teraflyFolder,apoPath,savaFolder,dimX,dimY,dimZ):
    commandStr = "{} " \
                 "/x {} " \
                 "/f cropTerafly " \
                 "/i  {} {}  {} /p {} {} {}".format(v3dexe,cropdll,teraflyFolder, apoPath, savaFolder,int(dimX),int(dimY),int(dimZ))
    os.system(commandStr)
    print("crop3Ddraw ok")

def crop3Ddraw(teraflyFolder,apoPath,savaFolder,dimX,dimY,dimZ):
    commandStr = "D:/v3d_external/bin/vaa3d_msvc.exe /x D:\\vaa3d_tools\\bin\plugins\\image_geometry\\crop3d_image_series\\cropped3DImageSeries.dll /f cropTerafly " \
                 "/i  {} {}  {} /p {} {} {}".format(teraflyFolder, apoPath, savaFolder,int(dimX),int(dimY),int(dimZ))
    os.system(commandStr)
    print("crop3Ddraw ok")

def extract2apo(path):
    brainDict={}
    fileList=os.listdir(path)
    for file in fileList:
        brain=file.split('_')[0]
        if brain not in brainDict:
            brainDict[brain]=[]
        for v3drawFile in os.listdir(os.path.join(path,file)):
            if ".v3draw" in v3drawFile:
                x,y,z=v3drawFile.strip('.v3draw').split('_')[0],v3drawFile.strip('.v3draw').split('_')[1],v3drawFile.strip('.v3draw').split('_')[2]
                brainDict[brain].append([x,y,z])

    for key in brainDict.keys():
        outfile=open("./"+key+".apo",'w')
        for x,y,z in brainDict[key]:
            outfile.write("0, , ,, {},{},{}, 0.000,0.000,0.000,50.000,0.000,,,,255,255,255\n".format(z,x,y))

    return brainDict
if __name__=="__main__":
    path="C:\\Users\wpkenan\Desktop\Archive"
    extract2apo(path)
