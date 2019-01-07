import os
import sys
import shutil
import numpy as np
import time
#
# def mkdir(folder):
#     commandStr="mkdir {}".format(folder);
#     os.system(commandStr);

def _20181223_():
    path="D:\soamdata\\17302\\v3draw";
    for root,dirs,files in os.walk(path):
        # print(files)
        for file in files:
            pass
            subfile=root+"\\..\\"+file.strip('.v3draw');
            # print(subfile)
            if not os.path.exists(subfile):
                print("mkdir "+subfile)
                os.mkdir(subfile)
                print("copy {} to {}".format(root+"\\"+file,subfile+"\\"+file))
                shutil.copy(root+"\\"+file,subfile+"\\"+file)


def _20181224_():
    commandStr="D:/v3d_external/bin/vaa3d_msvc.exe /x D:\\vaa3d_tools\\bin\plugins\wpkenanPlugin\somaDetection\somaDetection.dll " \
               "/f somadetect /i D:\soamdata\somaDetection\\16232.000_15508.000_3058.000.v3draw /p -1 /o D:\soamdata\somaDetection\\output.v3draw "

    os.system(commandStr)

def _20181228_():
    file=open("D:\soamdata\somaDetection\\raw.txt");
    contents=file.read()
    contents=contents.strip(' \n');
    contents=contents.split(' ')
    # print(contents[134217728])
    print(len(contents))
    # print(contents[:10])
    for i in range(len(contents)):
        contents[i]=int(contents[i]);
    # contents.append(0);
    contents=np.array(contents);
    matrix=np.zeros((512,512,512));
    print("Line: ",sys._getframe().f_lineno)
    for i in range(512):
        for j in range(512):
            for k in range(512):
                matrix[i][j][k]=contents[(i*512*512+j*512+k)]

    print("over")

def _20190102_():
    commandStr = "D:/v3d_external/bin/vaa3d_msvc.exe /x D:\\vaa3d_tools\\bin\plugins\wpkenanPlugin\swcDistance\swcDistance.dll " \
                 "/f function " \
                 "/i " \
                 "D:\soamdata\\17302\\test\ID(1)_16232.000_15508.000_3058.000\\16232.000_15508.000_3058.000.v3draw_x8_y448_z320_app2.swc " \
                 "D:\soamdata\\17302\\test\ID(1)_16232.000_15508.000_3058.000\\16232.000_15508.000_3058.000.v3draw_x222_y354_z144_app2.swc " \
                 "/p -1 " \
                 "/o D:\soamdata\somaDetection\\output.v3draw "
    os.system(commandStr)


def _20190103_():
    commandStr = "D:/v3d_external/bin/vaa3d_msvc.exe " \
                 "/x D:\\vaa3d_tools\\bin\\plugins\\wpkenanPlugin\\Vaa3D_Neuron3\\vn3.dll " \
                 "/f app3 " \
                 "/i D:\\soamdata\\zhouzhi\\x_10580_y_19004_z_1769.v3draw " \
                 "/p D:\\soamdata\\zhouzhi\\x_10580_y_19004_z_1769.v3draw_vn3.marker 0 -1"

    os.system(commandStr)

def _20190107_():
    savedStdout = sys.stdout  # 保存标准输出流
    file=open('D:\soamdata\\18454\\out.txt', 'w+')
    sys.stdout = file  # 标准输出重定向至文件
    print('This message is for file!')
    # sys.stdout = savedStdout

def _20190107_2(apoPath,splitFolder,isMul=1):
    file = open(apoPath);
    lines = file.readlines();
    markers = [];
    mulmarker = [];
    for line in lines:
        z, x, y = line.split(',')[4:7]
        # print(x,y,z)
        if line[0] == "#":
            continue;
        id = int(float(line.split(',')[2]))
        z = float(z);
        y = float(y);
        x = float(x);
        markers.append([x, y, z, id])
    for marker in markers:
        count = 0;
        nearIds = [];
        for tmpMarker in markers:
            if max(abs(tmpMarker[0] - marker[0]), abs(tmpMarker[1] - marker[1]), abs(tmpMarker[2] - marker[2])) == 0:
                count = count + 1;
                nearIds.append(tmpMarker[3])
                break;
        for tmpMarker in markers:
            # print(max(abs(tmpMarker[0]-256),abs(tmpMarker[1]-256),abs(tmpMarker[2]-256)))
            if max(abs(tmpMarker[0] - marker[0]), abs(tmpMarker[1] - marker[1]),
                   abs(tmpMarker[2] - marker[2])) < 310 and max(abs(tmpMarker[0] - marker[0]),
                                                                abs(tmpMarker[1] - marker[1]),
                                                                abs(tmpMarker[2] - marker[2])) != 0:
                count = count + 1;
                nearIds.append(tmpMarker[3])
        if count > 0:
            mulmarker.append([marker, count, nearIds]);

    mulmarker = sorted(mulmarker, key=lambda x: x[0][3], reverse=False)
    print("there are {} mulMarkers".format(len(mulmarker)))
    for item in mulmarker:
        print(item)

def _20190107_3(teraflyFolder, apoPath, v3drawFolder):
    commandStr = "D:/v3d_external/bin/vaa3d_msvc.exe /x D:\\vaa3d_tools\\bin\plugins\\image_geometry\\crop3d_image_series\\cropped3DImageSeries.dll /f cropTerafly " \
                 "/i  {} {}  {} /p 600 600 600".format(teraflyFolder, apoPath, v3drawFolder)
    os.system(commandStr)

if __name__=="__main__":
    # _20181224_()
    # _20181228_()
    # _20190103_();

    # startTime = time.asctime(time.localtime(time.time()))
    # _20190107_();
    # endTime = time.asctime(time.localtime(time.time()))
    # print("startTime:{}".format(startTime))
    # print("endTime:{}".format(endTime))

    # manual
    teraflyFolder = "E:\mouse18454_teraconvert\RES(26298x35000x11041)"
    apoPath = "D:\soamdata\\18454\\test.apo"
    # apoPath = "D:\soamdata\\18454\\soma_list.ano.apo"
    v3drawFolder = "D:\soamdata\\18454\\v3draw"
    srcManualSwcFolder = v3drawFolder + "\\..\\manualRawSwc"

    # auto
    splitFolderApp2 = v3drawFolder + "\\..\\splitToApp2"
    splitFolderApp3_1 = v3drawFolder + "\\..\\splitToApp3.1"
    tarManualSwcFolder = v3drawFolder + "\\..\\manualCutSwc"
    tarManualSwcFolder_prun = v3drawFolder + "\\..\\manualPrunedSwc"
    distanceFolder = v3drawFolder + "\\..\\distance";
    # _20190107_2(apoPath,splitFolderApp2,0)
    _20190107_3(teraflyFolder,apoPath,v3drawFolder)



