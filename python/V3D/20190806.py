import os
import sys
import shutil
import numpy as np
color=7
def readSwc(path,flag='root is -1'):
    with open(path) as file:
        lines=file.readlines()
    swc = {}
    for i in range(len(lines)):
        lines[i]=lines[i].strip('\n')
        if lines[i][0]=='#':
            continue
        lines[i]=lines[i].split(' ')
        # print(lines[i])
        swc[int(lines[i][0])]=[int(lines[i][1]),float(lines[i][2]),float(lines[i][3]),float(lines[i][4]),float(lines[i][5]),int(lines[i][6])]
    return swc

def dfsFindPath(swc,curPoint=[94.602, 2.039, 90.800]):
    minDis=9999999999
    for key in swc:
        tmp=np.sum((np.array([swc[key][1],swc[key][2],swc[key][3]])-np.array([curPoint[0],curPoint[1],curPoint[2]]))**2)
        if tmp < minDis:
            curId=key
            minDis=tmp
            # print(curId,tmp)

    while(curId in swc.keys()):
        swc[curId][0]=color
        curId=swc[curId][-1];



    return  swc

def writeSwc(outPath,swc):
    with open(outPath,'w') as file:
        for key in swc:
            if not swc[key][0]==color:
                continue
            file.write("{} ".format(key))
            for i in range(len(swc[key])-1):
                file.write("{} ".format(swc[key][i]))
            file.write("{}\n".format(swc[key][-1]))

def writeMarker(outPath,leaves):
    with open(outPath,'w') as file:
        for leaf in leaves:
            file.write("{}, {}, {}, 0, 1, , , 255,0,0\n".format(leaf[0],leaf[1],leaf[2]))



def resetPathColor():
    pass

def findLeafNode(swc):
    leaves=[]
    # find head
    for key in swc:
        if swc[key][-1] not in swc:
            # print(swc[key][2],swc[key][3],swc[key][4])
            leaves.append([swc[key][1],swc[key][2],swc[key][3]])


    #find leaf
    noChildren=list(swc.keys())
    for key in swc:
        if swc[key][-1] in noChildren:
            noChildren.remove(swc[key][-1])
    for key in noChildren:
        leaves.append([swc[key][1],swc[key][2],swc[key][3]])

    # print(leaves)
    return leaves
    # return leaves
def readFolder(folderPath,targetFolder):
    subStrList=[]
    for file in os.listdir(folderPath):
        if "_manual.swc" in file:
            subStrList.append(file.strip("_manual.swc"))

    for subStr in subStrList:
        print(subStr)
        initSwc = readSwc(os.path.join(folderPath,subStr+".v3draw_ini.swc"))
        manualSwc = readSwc(os.path.join(folderPath, subStr + "_manual.swc"))
        leaves = findLeafNode(manualSwc)
        for curPoint in leaves:
            initSwc=dfsFindPath(initSwc,curPoint)
        writeSwc(os.path.join(targetPath,subStr+"Rset.swc"),initSwc)
        writeMarker(os.path.join(targetPath,subStr+"leaves.marker"),leaves)
if __name__=="__main__":

    folderPath="C:\\Users\wpkenan\Desktop\cmy_marker_threshold1"
    # targetPath=folderPath+"/../result"
    targetPath=folderPath
    # if os.path.exists(targetPath):
    #     shutil.rmtree(targetPath)
    # os.mkdir(targetPath)
    readFolder(folderPath,targetPath)
    # path='test.swc'
    # swc=readSwc(path)
    # swc=dfsFindPath(swc)
    # writeSwc("result.swc",swc)
    # leaves=findLeafNode(swc)

