import os
import sys
import shutil
import numpy as np
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
               "/f somadetect /i D:\soamdata\\6\most\\test\\18454-1.v3draw /p -1 /o D:\soamdata\\6\most\\test\\18454-2.v3draw "

    os.system(commandStr)
if __name__=="__main__":
    _20181224_()


    # os.system("dir ..")
#




