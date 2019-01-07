import numpy as np
import os
import shutil
import re
import sys
import time



def crop3D(teraflyFolder,apoPath,v3drawFolder):
    commandStr = "D:/v3d_external/bin/vaa3d_msvc.exe /x D:\\vaa3d_tools\\bin\plugins\\image_geometry\\crop3d_image_series\\cropped3DImageSeries.dll /f cropTerafly " \
                 "/i  {} {}  {} /p 512 512 512".format(teraflyFolder, apoPath, v3drawFolder)
    os.system(commandStr)

def rename3D(apoPath,v3drawFolder):
    apofile = open(apoPath);
    apolines = apofile.readlines();
    apolist = [];
    dict = {}
    for line in apolines:
        z, x, y = line.split(',')[4:7]
        id = line.split(',')[2]
        # print(x,y,z)
        if line[0] == "#":
            continue;
        id = int(id);
        z = float(z);
        y = float(y);
        x = float(x);
        apolist.append([id, x, y, z]);
        dict["{:.3f}_{:.3f}_{:.3f}.v3draw".format(x, y, z)] = id;
    apolist = sorted(apolist, key=lambda x: x[0])
    print(apolist)
    print(dict)
    count = 0;
    for file in os.listdir(v3drawFolder):
        # print(file)
        count = count + 1
        if file in dict:
            if os.path.exists(v3drawFolder + "\\" + "ID({})_{}".format(dict[file], file)):
                os.remove(v3drawFolder + "\\" + "ID({})_{}".format(dict[file], file))
            # print(v3drawFolder + "\\" + file, v3drawFolder + "\\" + "ID({})_{}".format(dict[file], file));
            os.rename(v3drawFolder + "\\" + file, v3drawFolder + "\\" + "ID({})_{}".format(dict[file], file))


def splitTofolders(v3drawFolder,targetFolder):
    if not os.path.exists(targetFolder):
        os.mkdir(targetFolder)
    for file in os.listdir(v3drawFolder):
        if not os.path.exists(targetFolder+"\\"+file.strip(".v3draw")):
            os.mkdir(targetFolder+"\\"+file.strip(".v3draw"))
            shutil.copy(v3drawFolder + "\\" + file, targetFolder+"\\"+file.strip(".v3draw") + "\\" + file)

def createMarker(apoPath,splitFolder,isMul=1):
    file=open(apoPath);
    lines=file.readlines();
    markers=[];
    mulmarker=[];
    for line in lines:
        z,x,y=line.split(',')[4:7]
        # print(x,y,z)
        if line[0]=="#":
            continue;

        id=int(float(line.split(',')[2]))
        z=float(z);
        y=float(y);
        x=float(x);
        markers.append([x,y,z,id])

    # print(markers)
    # print(len(markers))
    for marker in markers:
        # print(marker)
        if not os.path.exists(splitFolder + "\\" + "ID({})_{:.3f}_{:.3f}_{:.3f}".format(marker[-1],marker[0], marker[1], marker[2])):
            continue
        outfile = open(splitFolder + "\\" + "ID({})_{:.3f}_{:.3f}_{:.3f}".format(marker[-1],marker[0], marker[1], marker[2]) + "\\" + "ID({})_{:.3f}_{:.3f}_{:.3f}.v3draw.marker".format(marker[-1],marker[0], marker[1], marker[2]),'w')
        # print(outfile)
        outfile.write("##x,y,z,radius,shape,name,comment, color_r,color_g,color_b\n")
        count=0;
        nearIds=[];
        for tmpMarker in markers:
            if max(abs(tmpMarker[0] - marker[0]), abs(tmpMarker[1] - marker[1]), abs(tmpMarker[2] - marker[2]))==0:
                count = count + 1;
                # print(tmpMarker)
                outfile.write("{:.3f},{:.3f},{:.3f},0, 1, , , 246,63,17\n".format(tmpMarker[0] - marker[0] + 256,
                                                                      tmpMarker[1] - marker[1] + 256,
                                                                      tmpMarker[2] - marker[2] + 256));
                nearIds.append(tmpMarker[3])
                break;
        for tmpMarker in markers:
            # print(max(abs(tmpMarker[0]-256),abs(tmpMarker[1]-256),abs(tmpMarker[2]-256)))
            if max(abs(tmpMarker[0]-marker[0]),abs(tmpMarker[1]-marker[1]),abs(tmpMarker[2]-marker[2])) < 255 and max(abs(tmpMarker[0]-marker[0]),abs(tmpMarker[1]-marker[1]),abs(tmpMarker[2]-marker[2]))!=0:
                count=count+1;
                # print(tmpMarker)
                if isMul:
                    outfile.write("{:.3f},{:.3f},{:.3f},0, 1, , , 246,63,17\n".format(tmpMarker[0]-marker[0]+256,tmpMarker[1]-marker[1]+256,tmpMarker[2]-marker[2]+256));
                # if max(abs(tmpMarker[0]-marker[0]),abs(tmpMarker[1]-marker[1]),abs(tmpMarker[2]-marker[2]))!=0:
                nearIds.append(tmpMarker[3])
        if count>0:
            mulmarker.append([marker,count,nearIds]);
        outfile.close();

    mulmarker=sorted(mulmarker,key=lambda x:x[0][3],reverse=False)
    print("there are {} mulMarkers".format(len(mulmarker)))
    print(mulmarker)

    if os.path.exists(splitFolder+"\\..\\somaBlock.csv"):
        return;

    outfile=open(splitFolder+"\\..\\somaBlock.csv",'w');
    outfile.write("id,count,nearIds\n")
    for item in mulmarker:
        # print("%d,%s,%s"%(item[0][3],item[1],"dasd"))
        outfile.write("%s,%s,"%(item[0][3],item[1]))
        for i in item[2]:
            outfile.write("{} ".format(i))
        outfile.write("\n")

def app2(path):
    print("app2 start:")
    files = os.listdir(path)
    count = 0;
    for file in files:
        # print(file[-6:])
        if file[-6:] == "v3draw":
            count = count + 1;
            print(file)
            commandStr = "D:/v3d_external/bin/vaa3d_msvc.exe " \
                         "/x D:/vaa3d_tools/bin/plugins/neuron_tracing\Vaa3D_Neuron2/vn2.dll " \
                         "/f app2 " \
                         "/i  \"%s\" " \
                         "/p \"%s\" 0 -1" % (path + "/" + file,path + "/" + file+".marker")
            # commandStr="ping www.baidu.com"
            # try:
            #     result = command(commandStr, timeout=60 * 10)
            # except TimeoutError:
            #     print('%s Run command timeout.' % (file))
            # else:
            #     print(result)
            os.system(commandStr)

def app3(path):
    print("app3 start:")
    files = os.listdir(path)
    count = 0;
    for file in files:
        # print(file[-6:])
        if file[-6:] == "v3draw":
            count = count + 1;
            print(file)
            commandStr = "D:/v3d_external/bin/vaa3d_msvc.exe " \
                         "/x D:/vaa3d_tools/bin/plugins/neuron_tracing\Vaa3D_Neuron2/vn2.dll " \
                         "/f app3 " \
                         "/i  \"%s\" " \
                         "/p \"%s\" 0 -1" % (path + "/" + file,path + "/" + file+".marker")
            print(commandStr)
            os.system(commandStr)

def runAutoTrace(splitFolder,algorithm):
    for dir in os.listdir(splitFolder):
        if len(os.listdir(splitFolder+"\\"+dir))<3:
            algorithm(splitFolder+"\\"+dir)

def prunSwcFile(swcPath,outPath):
    swcfile=open(swcPath);
    swclines=swcfile.readlines();
    swc={}
    for line in swclines:
        if line[0]=="#":
            continue
        line=line.strip('\n')
        line=line.split(' ');
        n=int(line[0]);
        type=int(line[1]);
        x=float(line[2]);
        y = float(line[3]);
        z = float(line[4]);
        radius=float(line[5]);
        parent=int(line[6]);
        isIn=1;
        # swc.append([n,type,x,y,z,radius,parent]);
        # if n==1:
        #     isIn=1;
        swc[n]=[n,type,x,y,z,radius,parent,isIn];


    indexAll=list(swc.keys());
    indexAll.sort(reverse=True);
    # print(indexAll)

    for index in indexAll:
        # print(swc[index])
        isIn = swc[index][-1]
        pid = index
        # print(index)
        # print(pid)
        while isIn:
            pid = swc[pid][-2];
            if pid==-1:
                break;
            if pid not in swc:
                break;
        # print("out:{} pid={}".format(index,pid))
        if pid==-1:
            continue;

        isIn = swc[index][-1]
        pid = index;
        while isIn:
            swc[pid][5] = -1
            swc[pid][-1] = 0;
            pid = swc[pid][-2];
            if pid == -1:
                break;
            if pid not in swc:
                break;

    outfile=open(outPath,'w');
    print(swcPath)
    if len(indexAll)==0:
        print("{} is empty")
        return;
    outfile.write("#base index={}-->1\n".format(min(indexAll)))
    outfile.write("##n,type,x,y,z,radius,parent\n");
    indexAll.sort();
    # print(len(indexAll))
    count=0;
    for index in indexAll:
        # print(swc[index])
        if swc[index][5]<0:
            continue
        count=count+1;
        outfile.write("{} {} {} {} {} {} {}\n".format(swc[index][0]-min(indexAll)+1,swc[index][1],swc[index][2],swc[index][3],swc[index][4],swc[index][5],max(-1,swc[index][6]-min(indexAll)+1)))
    print("ID({}) before prun:{} after prun:{} pruned number:{}".format(int(swcPath.split('\\')[-1].split('_')[1]),len(indexAll),count,len(indexAll)-count))

def prunSwcFolder(readFolder,writerFolder):
    print(sys._getframe().f_code.co_name+":")
    if not os.path.exists(writerFolder):
        os.mkdir(writerFolder)
    for i in os.listdir(readFolder):
        prunSwcFile(readFolder+"\\"+i,writerFolder+"\\"+i);

def cutManualSwc(srcManualSwcFolder,tarManualSwcFolder,apoPath):
    print(sys._getframe().f_code.co_name + ":")
    # srcManualSwcFolder="D:\soamdata\\17302\\17302_Whole"
    # tarManualSwcFolder=srcManualSwcFolder+"_Cut"
    if not os.path.exists(tarManualSwcFolder):
        os.mkdir(tarManualSwcFolder);

    markerDict={};
    file = open(apoPath);
    lines = file.readlines();
    for line in lines:
        z, x, y = line.split(',')[4:7]
        # print(x,y,z)
        if line[0] == "#":
            continue;

        id = int(float(line.split(',')[2]))
        z = float(z);
        y = float(y);
        x = float(x);
        # markers.append([x, y, z, id])
        markerDict[id]=[x,y,z];

    # print(markerDict)
    count=0;
    count2=0
    for swc in os.listdir(srcManualSwcFolder):
        if swc[-4:]==".swc" or swc[-5:]==".eswc":
            count=count+1;
            # print(count)
            if (int)(swc.split('_')[1]) not in markerDict:
                continue
            # print(int(swc.split('_')[1]))
            xcenter=markerDict[int(swc.split('_')[1])][0];
            ycenter = markerDict[int(swc.split('_')[1])][1];
            zcenter = markerDict[int(swc.split('_')[1])][2];
            # print(srcManualSwcFolder+"\\"+swc)
            swcfile=open(srcManualSwcFolder+"\\"+swc);
            swclines=swcfile.readlines();
            outfile=open(tarManualSwcFolder+"\\"+swc,'w');

            for line in swclines:
                if line[0]=="#":
                    outfile.write(line);
                    continue;
                line=line.strip('\n');
                line=line.split(' ');
                if abs(float(line[2])-xcenter)<256 and abs(float(line[3])-ycenter)<256 and abs(float(line[4])-zcenter)<256:
                    line[5] = '1.0'
                    line[2] = 256.0 + round((float(line[2]) - xcenter));
                    line[3] = 256.0 + round((float(line[3]) - ycenter));
                    line[4] = 256.0 + round((float(line[4]) - zcenter));
                    outfile.write("{} {} {} {} {} {} {}\n".format(line[0],line[1],line[2],line[3],line[4],line[5],line[6]));

        elif swc[-4:]=="eswc":
            count2=count2+1;

def disBetSwc(manualSwc,autoSwc,resultPath):
    commandStr = "D:/v3d_external/bin/vaa3d_msvc.exe " \
                 "/x D:\\vaa3d_tools\\bin\plugins\\neuron_utilities\\neuron_distance\\neuron_dist.dll " \
                 "/f neuron_distance " \
                 "/i  {} {} " \
                 "/p 2 /o {}".format(manualSwc, autoSwc,resultPath)
    os.system(commandStr)

def disBetSwcFolder(manualFolder,autoFolder,distanceFolder):
    print(sys._getframe().f_code.co_name + ":")
    count=0;
    auto={};
    manual={};
    for root, dirs, files in os.walk(autoFolder):
        for file in files:
            # print(root+"\\"+file);
            if "x254_y254_z254" in file:
                count=count+1;
                auto[int(re.findall("\((.+?)\)",root)[0])]=root+"\\"+file
    print(auto[176])
    # print(j)
    # print(count)
    for root, dirs, files in os.walk(manualFolder):
        for file in files:
            count=count+1;
            manual[int(file.split('_')[1])]=root+"\\"+file
    # print(manual)

    if not os.path.exists(distanceFolder):
        os.mkdir(distanceFolder)

    resultFolder = distanceFolder +"\\"+ manualFolder.split("\\")[-1] + "(To)" + autoFolder.split("\\")[-1];
    # resultFolderReverse=manualFolder + "\\..\\distance\\" + autoFolder.split("\\")[-1] + "(To)" + manualFolder.split("\\")[-1];
    if not os.path.exists(resultFolder):
        os.mkdir(resultFolder)
    # if not os.path.exists(resultFolderReverse):
    #     os.mkdir(resultFolderReverse)
    for i in auto:
        if i in manual:
            print(resultFolder+"\\"+"ID({}).txt".format(i))
            if not os.path.exists(resultFolder+"\\"+"ID({}).txt".format(i)):
                disBetSwc(manual[i],auto[i],resultFolder+"\\"+"ID({}).txt".format(i))

def outputExcel(distanceFolder):
    data = {}
    for i in os.listdir(distanceFolder):
        tmplines = np.zeros((500, 8)) - 1;
        # print(i)
        for j in os.listdir(os.path.join(distanceFolder, i)):
            tmpline = [];
            id = int(re.findall("\((.+?)\)", j)[0])
            # print(id)
            distanceFile = open(os.path.join(distanceFolder, i, j));
            lines = distanceFile.readlines();
            tmpline.append(id)
            for line in lines:
                if line[0] == 'i':
                    continue
                line = line.strip('\n');
                line = line.split('=');
                # print(line)
                # print(line[-1])
                try:
                    line[-1]=float(line[-1]);
                except:
                    # print(line[-1])
                    line[-1]=-1;
                tmpline.append(float(line[-1]));
            # print(np.shape(tmplines))
            tmplines[id, :] = np.array(tmpline);
        # print("***********************************************")
        # for item in tmplines:
        # print(item)
        data[i] = tmplines
        # print(len(data[i]))

    name = list(data.keys());
    name.sort();

    for i in name:
        # print(distanceFolder+i+".csv")
        outfile = open(distanceFolder + "\\..\\" + i + ".csv", 'w');
        # print("{},{},{},{},{},{},{}".format("manual_To_"+i.split('s')[-1],i.split('s')[-1]+"_To_manual","average of bi-directional entire-structure-averages","differen-structure-average ",4,5,6))
        outfile.write("{},{},{},{},{},{},{}\n".
                      format("id", "manual_To_" + i.split('s')[-1], i.split('s')[-1] + "_To_manual",
                             "average of bi-directional entire-structure-averages", "differen-structure-average ", 4, 5))
        for j in data[i]:
            # print(j)
            if j[0]<0:
                continue
            outfile.write("{},{},{},{},{},{},{}\n".
                          format(j[0], j[1], j[2], j[3], j[4], j[5], j[6]))
def mergeExcel(somaBlockCsv,disCsvList):
    somaBlock={};
    file=open(somaBlockCsv);
    lines=file.readlines();
    for i in range(len(lines)):
        line=lines[i].strip('\n');
        line=line.split(',');
        if i==0:
            somaBlock[0] = [];
            for j in range(len(line)):
                somaBlock[0].append(line[j]);
        else:
            somaBlock[int(line[0])] = [];
            for j in range(len(line)):
                somaBlock[int(line[0])].append(line[j]);
    file.close();


    for csvFile in disCsvList:
        file=open(csvFile);
        lines=file.readlines();
        for i in range(len(lines)):

            line = lines[i].strip('\n');
            line = line.split(',');
            print(line)
            if i==0:
                for j in range(len(line)):
                    somaBlock[0].append(line[j]);
            elif int(float(line[0])) in somaBlock:
                for j in range(len(line)):
                    somaBlock[int(float(line[0]))].append(line[j]);
        file.close()

    # print("out2")
    print(somaBlock[10])
    outfile=open(somaBlockCsv+"\\..\\result.csv",'w');
    for i in somaBlock:
        for j in somaBlock[i]:
            outfile.write("{},".format(j));
        outfile.write("\n")
    outfile.close()
    # print("out3")



def main():

    #manual
    teraflyFolder = "E:\mouse18454_teraconvert\RES(26298x35000x11041)"
    # apoPath = "D:\soamdata\\18454\\test.apo"
    apoPath="D:\soamdata\\18454\\soma_list.ano.apo"
    v3drawFolder = "D:\soamdata\\18454\\v3draw"
    srcManualSwcFolder = v3drawFolder + "\\..\\manualRawSwc"

    #auto
    splitFolderApp2=v3drawFolder+"\\..\\splitToApp2"
    splitFolderApp3_1 = v3drawFolder + "\\..\\splitToApp3.1"
    tarManualSwcFolder=v3drawFolder+"\\..\\manualCutSwc"
    tarManualSwcFolder_prun=v3drawFolder+"\\..\\manualPrunedSwc"
    distanceFolder=v3drawFolder+"\\..\\distance";

    #step1 prepare v3draw && split to folders
    # crop3D(teraflyFolder,apoPath,v3drawFolder)
    # rename3D(apoPath,v3drawFolder)
    # splitTofolders(v3drawFolder,splitFolderApp2)
    # splitTofolders(v3drawFolder, splitFolderApp3_1)

    #step2 prepare markers
    # createMarker(apoPath,splitFolderApp2,isMul=0)
    # createMarker(apoPath,splitFolderApp3_1,isMul=1)

    #step3 run app2,app3.1
    # runAutoTrace(splitFolderApp2,app2)
    # runAutoTrace(splitFolderApp3_1,app3)

    #step4 prun manualSwc
    # cutManualSwc(srcManualSwcFolder,tarManualSwcFolder,apoPath);
    # prunSwcFolder(tarManualSwcFolder,tarManualSwcFolder_prun)

    #step5 run distance
    disBetSwcFolder(tarManualSwcFolder_prun,splitFolderApp2,distanceFolder)
    disBetSwcFolder(tarManualSwcFolder_prun,splitFolderApp3_1,distanceFolder)

    #output excel
    outputExcel(distanceFolder)

    #merge excel
    mergeExcel(v3drawFolder+"\\..\\somaBlock.csv",[v3drawFolder+"\\..\\manualPrunedSwc(To)splitToApp2.csv",v3drawFolder+"\\..\\manualPrunedSwc(To)splitToApp3.1.csv"])

if __name__=="__main__":
    # tmpfile = open('D:\soamdata\\18454\\out.txt', 'w+')
    # sys.stdout = tmpfile  # 标准输出重定向至文件
    # print('This message is for file!')

    startTime = time.asctime(time.localtime(time.time()))
    # main();
    endTime=time.asctime( time.localtime(time.time()))
    print("startTime:{}".format(startTime))
    print("endTime:{}".format(endTime))

    # app2("D:\soamdata\\18454\splitToApp2\ID(177)_16677.947_13351.408_5308.884")
    # os.system("explore.exe")
    disBetSwc("D:\soamdata\\18454\manualPrunedSwc\\18454_00164_YJ_SYY_stamp_2019_01_04_11_33.ano.eswc",
              "D:\soamdata\\18454\splitToApp3.1\ID(164)_24079.059_12004.414_5841.724\\ID(164)_24079.059_12004.414_5841.724.v3draw_x254_y254_z254_app2.swc",
              "D:\soamdata\\18454\splitToApp3.1\ID(164)_24079.059_12004.414_5841.724\\distance.txt")