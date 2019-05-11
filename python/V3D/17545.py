import os
import shutil
import sys
import numpy as np
import re

def shiftSwc(inpath,outpath,dx,dy,dz,dindex):
    lines=open(inpath).readlines();
    output=open(outpath,'w');
    for i in range(len(lines)):
        if lines[i][0]=='#':
            output.write(lines[i])
            continue
        lines[i]=lines[i].strip('\n');
        lines[i]=lines[i].split(' ');
        output.write("{} {} {} {} {} {} {}\n".format(eval(lines[i][0])+dindex,lines[i][1],eval(lines[i][2])+dx,eval(lines[i][3])+dy,eval(lines[i][4])+dz,lines[i][5],eval(lines[i][6])+dindex))
        # print(lines[i])
    output.close()

def shift_merge_Swc(swcFiles,outpath,dindex,dx,dy,dz):
    swcs={}
    count=0;
    for file in swcFiles:

        swcs[count]=[]

        lines = open(file).readlines();
        for i in range(len(lines)):
            if lines[i][0] == '#':
                continue
            lines[i] = lines[i].strip('\n');
            lines[i] = lines[i].split(' ');
            swcs[count].append([eval(lines[i][0]) + dindex*count,
                                count+1,
                                eval(lines[i][2]) + dx*count,
                                eval(lines[i][3]) + dy*count,
                                eval(lines[i][4]) + dz*count,
                                lines[i][5],
                                eval(lines[i][6]) + dindex*count])
        count = count + 1;
    # print(swcs[0])
    # print(swcs[1])
    output=open(outpath,'w');
    for key in swcs:
        lines=swcs[key]
        for i in range(len(lines)):
            output.write("{} {} {} {} {} {} {}\n".format(lines[i][0], lines[i][1], lines[i][2],lines[i][3], lines[i][4], lines[i][5],lines[i][6]))


def shift_merge_Swc_folder(inFolders,outFolder):
    count=0;
    for file in os.listdir(inFolders[1]):
        if file[-3:] == 'swc':
            count=count+1;
            # if count>3:
            #     break
            swcFiles=[x+"\\"+file for x in inFolders];
            if os.path.exists(swcFiles[0]) and os.path.exists(swcFiles[1]) and os.path.exists(swcFiles[-1]):
                print(swcFiles)
                shift_merge_Swc(swcFiles,outFolder+"\\"+file,99999999,2000,0,0)


# shift_merge
def renameSwc1(infolder,outfolder):
    for file in os.listdir(infolder):
        if file[-3:] == 'swc':
            shutil.copy(infolder+"\\"+file,outfolder+"\\"+file.split('_')[0]+".swc")

def renameSwc2(infolder,outfolder):
    for file in os.listdir(infolder):
        if file[-3:] == 'swc':
            shutil.copy(infolder+"\\"+file,outfolder+"\\"+str(int((file.split('.')[0]).split('_')[1]))+".swc")


def scaleSwc(inpath,outpath,scale):
    file = open(inpath)
    lines = file.readlines();
    file.close()

    output = open(outpath, 'w');
    for i in range(len(lines)):
        if lines[i][0] == '#':
            output.write(lines[i])
            continue
        lines[i] = lines[i].strip('\n');
        lines[i] = lines[i].split(' ');
        output.write("{} {} {} {} {} {} {}\n".format(eval(lines[i][0]), lines[i][1], eval(lines[i][2])*scale,
                                                     eval(lines[i][3])*scale, eval(lines[i][4])*scale, lines[i][5],
                                                     eval(lines[i][6])))
        # print(lines[i])
    output.close()

def scaleFolder(infolder,outfolder,scale):
    for file in os.listdir(infolder):
        if file[-3:] == 'swc':
            scaleSwc(infolder+"\\"+file,outfolder+"\\"+file,scale)

def disBetSwc(manualSwc,autoSwc,resultPath):
    commandStr = "D:/v3d_external/bin/vaa3d_msvc.exe " \
                 "/x D:\\vaa3d_tools\\bin\plugins\\neuron_utilities\\neuron_distance\\neuron_dist.dll " \
                 "/f neuron_distance " \
                 "/i  {} {} " \
                 "/p 2 /o {}".format(manualSwc, autoSwc,resultPath)
    os.system(commandStr)

def disBetSwcFolder(manualFolder,autoFolder,distanceFolder):
    count=0;
    for file in os.listdir(manualFolder):
        if file[-3:] == 'swc':

            if os.path.exists(autoFolder+"\\"+file):
                count = count + 1
                disBetSwc(manualFolder+"\\"+file,autoFolder+"\\"+file,distanceFolder+"\\"+file.split('.')[0]+".txt")
                # if count>2:
                #     break


def outputExcel(distanceFolder):
    data = {}
    tmplines=[]
    # print(i)
    for j in os.listdir(distanceFolder):

        tmpline = [];
        distanceFile = open(distanceFolder+"\\"+j);
        lines = distanceFile.readlines();
        id=0;
        onlyOne=1
        for line in lines:
            if line[0] == 'i':
                id=line.strip('\n').split('\\')[-1].split('.')[0];
                if onlyOne:
                    tmpline.append(int(id));
                    onlyOne=0;
                continue
            line = line.strip('\n');
            line = line.split('=');
            try:
                line[-1]=float(line[-1]);
            except:
                # print(line[-1])
                line[-1]=-1;
            tmpline.append(float(line[-1]));
            # print(tmpline)
        tmplines.append(tmpline)

    data[0]= tmplines


    # print(distanceFolder+i+".csv")
    outfile = open(distanceFolder + "\\..\\" + distanceFolder.split("\\")[-1] + ".csv", 'w');
    # print("{},{},{},{},{},{},{}".format("manual_To_"+i.split('s')[-1],i.split('s')[-1]+"_To_manual","average of bi-directional entire-structure-averages","differen-structure-average ",4,5,6))
    outfile.write("{},{},{},{},{},{},{}\n".
                  format("id", "manual_To_" + distanceFolder.split('\\')[-1], distanceFolder.split('\\')[-1] + "_To_manual",
                         "average of bi-directional entire-structure-averages", "differen-structure-average ", 4, 5))
    for j in data[0]:
        # print(j)
        if j[0]<0:
            continue
        outfile.write("{},{},{},{},{},{},{},{}\n".
                      format(j[0], j[1], j[2], j[3], j[4], j[5], j[6],j[7]))

def main():

    brain=17545

    app2Folder = "D:\soamdata\\ultratracer\\{}\\app2".format(brain)
    app3Folder = "D:\soamdata\\ultratracer\\{}\\app3".format(brain)
    manualFolder = "D:\soamdata\\ultratracer\\{}\\manual".format(brain)
    mergeFolder = "D:\soamdata\\ultratracer\\{}\\merge_swc".format(brain)
    app3_distance = "D:\soamdata\\ultratracer\\{}\\app3_distance".format(brain)
    app2_distance = "D:\soamdata\\ultratracer\\{}\\app2_distance".format(brain)

    if not os.path.exists(app2Folder):
        os.mkdir(app2Folder);
    if not os.path.exists(app3Folder):
        os.mkdir(app3Folder);
    if not os.path.exists(manualFolder):
        os.mkdir(manualFolder);
    if not os.path.exists(mergeFolder):
        os.mkdir(mergeFolder);
    if not os.path.exists(app3_distance):
        os.mkdir(app3_distance);
    if not os.path.exists(app2_distance):
        os.mkdir(app2_distance);

    #更改名称
    # renameSwc1("D:\\soamdata\\ultratracer\\{}\\{}_app2\in".format(brain,brain),app2Folder);
    # renameSwc1("D:\\soamdata\\ultratracer\\{}\\{}_app3\in".format(brain,brain),app3Folder);
    # renameSwc2("D:\soamdata\\ultratracer\\{}\\{}_manual".format(brain,brain),manualFolder);

    #scale同一尺度


    # scaleFolder(app2Folder,app2Folder,2);
    # scaleFolder(app3Folder,app3Folder,2)

    #mergeSwc

    # shift_merge_Swc(["D:\soamdata\\ultratracer\\17302\\app2\\1.swc","D:\soamdata\\ultratracer\\17302\\app2\\1.swc","D:\soamdata\\ultratracer\\17302\\app2\\1.swc"],
    #                 "D:\soamdata\\ultratracer\\17302\merge_swc\\1.swc",99999, 1000, 0, 0)
    shift_merge_Swc_folder([app3Folder,app2Folder],mergeFolder)

    #distance
    # disBetSwcFolder(manualFolder, app2Folder, app2_distance)
    # disBetSwcFolder(manualFolder,app3Folder,app3_distance)

    #outexcel
    # outputExcel(app2_distance)
    # outputExcel(app3_distance)


if __name__=="__main__":
    # path="D:\\soamdata\\ultratracer\\17302\\17302_app2\individual\\2_8100.000_7804.000_1474.000.v3draw.marker_nc_APP2_GD.swc"
    # shiftSwc(path,path+"\\..\\..\\..\\merge_swc\\"+path.split("\\")[-1]+"_shift.swc",10,10,10,999999);
    main()


