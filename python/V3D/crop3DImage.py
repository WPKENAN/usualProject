import numpy as np
import os
import shutil
import re
import sys
#D:/v3d_external/bin/vaa3d_msvc.exe /x D:\vaa3d_tools\bin\plugins\image_geometry\crop3d_image_series\cropped3DImageSeries.dll /f app3 /i  D:\soamdata\6\most\test\18454-1.v3draw /p "" 0 -1


def crop3D(teraflyFolder,apoPath,saveFolder):
    commandStr="D:/v3d_external/bin/vaa3d_msvc.exe /x D:\\vaa3d_tools\\bin\plugins\\image_geometry\\crop3d_image_series\\cropped3DImageSeries.dll /f cropTerafly " \
        "/i  {} {}  {} /p 512 512 512".format(teraflyFolder,apoPath,saveFolder)
    os.system(commandStr)

def splitTofolders(path):
    for root, dirs, files in os.walk(path):
        # print(files)
        for file in files:
            pass
            subfile = root + "\\..\\splitTofolders\\" + file.strip('.v3draw');
            # print(subfile)
            if not os.path.exists(subfile):
                print("mkdir " + subfile)
                os.mkdir(subfile)
                print("copy {} to {}".format(root + "\\" + file, subfile + "\\" + file))
                shutil.copy(root + "\\" + file, subfile + "\\" + file)

def createMarker(apoPath,splitFolder):
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
        # print(splitFolder + "\\" + "{}00_{}00_{}00".format(x, y, z))
        # print(splitFolder + "\\14658.000_40500.000_2648.000")
        # print(os.path.exists(splitFolder + "\\" + "{}00_{}00_{}00".format(x, y, z)))

    # print(markers)
    # print(len(markers))
    for marker in markers:
        # print(marker)
        outfile = open(splitFolder + "\\" + "ID({})_{}00_{}00_{}00".format(marker[-1],marker[0], marker[1], marker[2]) + "\\" + "{}00_{}00_{}00.v3draw.marker".format(marker[0], marker[1], marker[2]),'w')
        # print(outfile)
        outfile.write("##x,y,z,radius,shape,name,comment, color_r,color_g,color_b\n")
        count=0;
        nearIds=[];
        for tmpMarker in markers:
            # print(max(abs(tmpMarker[0]-256),abs(tmpMarker[1]-256),abs(tmpMarker[2]-256)))
            if max(abs(tmpMarker[0]-marker[0]),abs(tmpMarker[1]-marker[1]),abs(tmpMarker[2]-marker[2])) < 255:
                count=count+1;
                # print(tmpMarker)
                outfile.write("{},{},{},0, 1, , , 246,63,17\n".format(tmpMarker[0]-marker[0]+256,tmpMarker[1]-marker[1]+256,tmpMarker[2]-marker[2]+256));
                # if max(abs(tmpMarker[0]-marker[0]),abs(tmpMarker[1]-marker[1]),abs(tmpMarker[2]-marker[2]))!=0:
                nearIds.append(tmpMarker[3])

        if count>0:
            mulmarker.append([marker,count,nearIds]);
    outfile.close();
    mulmarker=sorted(mulmarker,key=lambda x:x[0][3],reverse=False)
    print("there are {} mulMarkers".format(len(mulmarker)))

    outfile=open("D:\soamdata\\17302\\somaBlock.csv",'w');
    for item in mulmarker:
        # print("%d,%s,%s"%(item[0][3],item[1],"dasd"))
        outfile.write("%s,%s,"%(item[0][3],item[1]))
        for i in item[2]:
            outfile.write("{} ".format(i))
        outfile.write("\n")


def cutManualSwc(srcManualSwcFolder,tarManualSwcFolder,apoPath):
    srcManualSwcFolder="D:\soamdata\\17302\\17302_Whole"
    tarManualSwcFolder=srcManualSwcFolder+"_Cut"
    if not os.path.exists(tarManualSwcFolder):
        os.mkdir(tarManualSwcFolder);
    count=0;
    count2=0
    for swc in os.listdir(srcManualSwcFolder):
        if swc[-4:]==".swc":
            count=count+1;
            print(count)
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
                if line[0]=='1':
                    xcenter=float(line[2]);
                    ycenter=float(line[3]);
                    zcenter=float(line[4]);
                    line[5]='3.0'
                    line[2] = 256 + (float(line[2])-xcenter);
                    line[3] = 256 + (float(line[3])-ycenter);
                    line[4] = 256 + (float(line[4])-zcenter);
                    outfile.write("{} {} {} {} {} {} {}\n".format(line[0],line[1],line[2],line[3],line[4],line[5],line[6]));
                    # print(xcenter,ycenter,zcenter)
                    continue;

                if abs(float(line[2])-xcenter)<256 and abs(float(line[3])-ycenter)<256 and abs(float(line[4])-zcenter)<256:
                    line[5] = '1.0'
                    line[2] = 256.0 + round((float(line[2]) - xcenter));
                    line[3] = 256.0 + round((float(line[3]) - ycenter));
                    line[4] = 256.0 + round((float(line[4]) - zcenter));
                    outfile.write("{} {} {} {} {} {} {}\n".format(line[0],line[1],line[2],line[3],line[4],line[5],line[6]));



        elif swc[-4:]=="eswc":
            count2=count2+1;




def changeFolderName(apoPath,splitFolder):
    apofile = open(apoPath);
    apolines = apofile.readlines();
    apolist = [];
    dict={}
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
        dict["{}00_{}00_{}00".format(x,y,z)]=id;
    apolist = sorted(apolist, key=lambda x: x[0])
    print(apolist)

    # print(dict["17090.000_19332.000_4804.000"])


    # print('a' in dict)
    # splitFolder="D:\soamdata\\17302\\test"
    count=0;
    for file in os.listdir(splitFolder):
        print(file)
        count=count+1
        if file in dict:
            os.rename(splitFolder+"\\"+file,splitFolder+"\\"+"ID({})_{}".format(dict[file],file))




def disBetSwc(manualSwc,autoSwc,resultPath):
    commandStr = "D:/v3d_external/bin/vaa3d_msvc.exe " \
                 "/x D:\\vaa3d_tools\\bin\plugins\\neuron_utilities\\neuron_distance\\neuron_dist.dll " \
                 "/f neuron_distance " \
                 "/i  {} {} " \
                 "/p 2 /o {}".format(manualSwc, autoSwc,resultPath)
    os.system(commandStr)

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
            # break;



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
            # commandStr="ping www.baidu.com"
            # try:
            #     result = command(commandStr, timeout=60 * 10)
            # except TimeoutError:
            #     print('%s Run command timeout.' % (file))
            # else:
            #     print(result)

            os.system(commandStr)
            # break;

def changeMarkerToOne(splitFolder):
    for i in os.listdir(splitFolder):
        # print(i)
        for j in os.listdir(splitFolder+"\\"+i):
            # print(j)
            if j.split('.')[-1]=="v3draw":
                # print(j)
                outfile=open(splitFolder+"\\"+i+"\\"+j+".marker",'w');
                outfile.write("##x,y,z,radius,shape,name,comment, color_r,color_g,color_b\n");
                outfile.write("256.0,256.0,256.0,0, 1, , , 246,63,17\n")

def sortMarker(splitFolder):
    for i in os.listdir(splitFolder):
        # print(i)
        for j in os.listdir(splitFolder+"\\"+i):
            # print(j)
            if j.split('.')[-1]=="v3draw":
                # print(j)
                # outfile=open(splitFolder+"\\"+i+"\\"+j+".marker",'w');
                # outfile.write("##x,y,z,radius,shape,name,comment, color_r,color_g,color_b\n");
                # outfile.write("256.0,256.0,256.0,0, 1, , , 246,63,17\n")

                markerfile=open(splitFolder+"\\"+i+"\\"+j+".marker");
                markerlines=markerfile.readlines();
                markers=[]
                for line in markerlines:
                    if line[0]=="#":
                        continue
                    line=line.strip('\n');
                    line=line.split(',');
                    x = float(line[0])
                    y = float(line[1])
                    z = float(line[2])
                    markers.append([x,y,z])
                markerfile.close();

                markers=sorted(markers,key=lambda x:max(abs(x[0]-256),abs(x[1]-256),abs(x[2]-256)))
                # print(markers)
                outfile=open(splitFolder+"\\"+i+"\\"+j+".marker",'w');
                outfile.write("##x,y,z,radius,shape,name,comment, color_r,color_g,color_b\n");
                for i in markers:
                    outfile.write("{},{},{},0, 1, , , 246,63,17\n".format(i[0],i[1],i[2]))
                    # print("{},{},{},0, 1, , , 246,63,17".format(i[0],i[1],i[2]))
                # print("\n")
                outfile.close()

def main():
    teraflyFolder="E:\mouseID_321237-17302\RES(54600x34412x9847)"
    apoPath="D:\soamdata\\17302\\somas.ano.apo"
    saveFolder="D:\soamdata\\17302\\v3draw"
    splitFolder=saveFolder+"\\..\\splitTofolders3.1";

    #step1
    # crop3D(teraflyFolder,apoPath,saveFolder);

    #step2
    #splitTofolders(saveFolder);

    #step3
    # createMarker(apoPath,splitFolder)

    #step4
    # count=0;
    # for root, dirs, files in os.walk(splitFolder):
    #     # print(dirs)
    #     count=count+1;
    #     if count < 85:
    #         continue;
    #     print(root)
    #     app3(root)

    # app2
    print("----------app2-------------only one marker")
    count=0;
    for root, dirs, files in os.walk(saveFolder+"\\..\\splitTofolders2.1"):
        # print(dirs)
        count=count+1;
        # print("-----------------{}----------------".format(count))
        # print(root)
        if count < 74:
            continue;
        # print(root)
        # app2(root)

    # app2.2
    print("----------app2-------------mul markers")
    count = 0;
    for root, dirs, files in os.walk(saveFolder + "\\..\\splitTofolders2.2"):
        # print(dirs)
        print("-----------------{}----------------".format(count))
        count = count + 1;
        if count < 74:
            continue;
        print(root)
        app2(root)
    # cutManualSwc('','',apoPath)

    # changeFolderName(apoPath,splitFolder)
    # changeMarkerToOne(splitFolder)
    # sortMarker(splitFolder)

def disBetSwcFolder(manualFolder,autoFolder,resultFolder):

    count=0;
    auto={};
    manual={};
    for root, dirs, files in os.walk(autoFolder):
        for file in files:
            # print(root+"\\"+file);
            if "x254_y254_z254" in file:
                count=count+1;
                auto[re.findall("\((.+?)\)",root)[0]]=root+"\\"+file
    print(auto)
    # print(j)
    # print(count)
    for root, dirs, files in os.walk(manualFolder):
        for file in files:
            count=count+1;
            manual["{}".format(int(file.split('_')[2][0:3]))]=root+"\\"+file
    print(manual)

    resultFolder = manualFolder + "\\..\\distance\\" + manualFolder.split("\\")[-1] + "(To)" + autoFolder.split("\\")[-1];
    # resultFolderReverse=manualFolder + "\\..\\distance\\" + autoFolder.split("\\")[-1] + "(To)" + manualFolder.split("\\")[-1];
    if not os.path.exists(resultFolder):
        os.mkdir(resultFolder)
    # if not os.path.exists(resultFolderReverse):
    #     os.mkdir(resultFolderReverse)
    for i in auto:
        print(i)
        if i in manual:
            disBetSwc(manual[i],auto[i],resultFolder+"\\"+"ID({}).txt".format(i))
            # disBetSwc(auto[i],manual[i],resultFolderReverse+"\\"+"ID({}).txt".format(i))

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
    print(indexAll)

    for index in indexAll:
        # print(swc[index])

        isIn=swc[index][-1]
        pid = swc[index][0];
        while isIn:
            if swc[pid][-2] not in swc:
                break;
            if pid==1:
                break;
            # print(pid)
            isIn = swc[pid][-1];
            pid = swc[pid][-2];


        print("out:{} pid={}".format(index,pid))

        if pid==1:
            continue;
        isIn = swc[index][-1]
        pid = swc[index][0];
        while isIn:
            if swc[pid][-2] not in swc:
                break;
            if pid==1:
                break;
            # print(pid)
            swc[pid][-1] = 0;
            swc[pid][5] = -1;
            pid = swc[pid][-2];



    outfile=open(outPath,'w');
    outfile.write("##n,type,x,y,z,radius,parent\n");
    indexAll.sort();
    for index in indexAll:
        # print(swc[index])
        if swc[index][5]<0:
            continue
        outfile.write("{} {} {} {} {} {} {}\n".format(swc[index][0],swc[index][1],swc[index][2],swc[index][3],swc[index][4],swc[index][5],swc[index][6]))

def prunSwcFolder(readFolder,writerFolder):
    for i in os.listdir(readFolder):
        prunSwcFile(readFolder+"\\"+i,writerFolder+"\\"+i);





def main():
    teraflyFolder="E:\mouseID_321237-17302\RES(54600x34412x9847)"
    apoPath="D:\soamdata\\17302\\somas.ano.apo"
    saveFolder="D:\soamdata\\17302\\v3draw"
    splitFolder=saveFolder+"\\..\\splitTofolders3.1";

    #step1
    # crop3D(teraflyFolder,apoPath,saveFolder);

    #step2
    #splitTofolders(saveFolder);

    #step3
    createMarker(apoPath,splitFolder)

    #step4
    # count=0;
    # for root, dirs, files in os.walk(splitFolder):
    #     # print(dirs)
    #     count=count+1;
    #     if count < 85:
    #         continue;
    #     print(root)
    #     app3(root)

    # app2
    # print("----------app2-------------only one marker")
    # count=0;
    # for root, dirs, files in os.walk(saveFolder+"\\..\\splitTofolders2.1"):
    #     # print(dirs)
    #     count=count+1;
    #     # print("-----------------{}----------------".format(count))
    #     # print(root)
    #     if count < 74:
    #         continue;
        # print(root)
        # app2(root)

    # app2.2
    # print("----------app2-------------mul markers")
    # count = 0;
    # for root, dirs, files in os.walk(saveFolder + "\\..\\splitTofolders2.2"):
    #     # print(dirs)
    #     print("-----------------{}----------------".format(count))
    #     count = count + 1;
    #     if count < 74:
    #         continue;
    #     print(root)
    #     app2(root)
    # cutManualSwc('','',apoPath)

    # changeFolderName(apoPath,splitFolder)
    # changeMarkerToOne(splitFolder)
    # sortMarker(splitFolder)

if __name__=="__main__":
    main();

    # disBetSwc('D:\soamdata\\17302\splitTofolders3.1\ID(1)_16232.000_15508.000_3058.000\\16232.000_15508.000_3058.000.v3draw_x222_y354_z144_app2.swc',
    #           'D:\soamdata\\17302\splitTofolders3.1\ID(1)_16232.000_15508.000_3058.000\\16232.000_15508.000_3058.000.v3draw_x254_y254_z254_app2.swc');


    # prunSwcFile("D:\soamdata\\17302\\test\\17302_CPU_001.processed.swc","D:\soamdata\\17302\\17302_Whole_Cut_Prun\\17302_CPU_001.processed.swc")
    # prunSwcFolder("D:\soamdata\\17302\\17302_Whole_Cut","D:\soamdata\\17302\\17302_Whole_Cut_Prun")
    # disBetSwcFolder("D:\soamdata\\17302\\17302_Whole_Cut_Prun","D:\soamdata\\17302\splitTofolders2.1",'')
    # disBetSwcFolder("D:\soamdata\\17302\\17302_Whole_Cut_Prun", "D:\soamdata\\17302\splitTofolders2.2", '')
    # disBetSwcFolder("D:\soamdata\\17302\\17302_Whole_Cut_Prun", "D:\soamdata\\17302\splitTofolders3.1", '')
    # disBetSwcFolder("D:\soamdata\\17302\\17302_Whole_Cut_Prun", "D:\soamdata\\17302\splitTofolders3.2", '')

