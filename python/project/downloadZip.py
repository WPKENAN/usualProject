import urllib
import requests
from urllib import request
import os
file=open("D:\github\Data\CT_head\CQ500\\cq500_files.txt")
readlist=file.readlines();
for i in range(len(readlist)):
    readlist[i]=readlist[i].strip('\n')


def fun(blocknum,blocksize,totalsize):
    """
    blocknum:当前的块编号
    blocksize:每次传输的块大小
    totalsize:网页文件总大小
    """
    percent = blocknum*blocksize/totalsize
    if percent > 1.0:
        percent = 1.0
    percent = percent*100
    print("download : %.2f%%" %(percent))

for url in readlist:
    print(url)
    filename=os.path.basename(url);
    path = "D:\\github\\Data\\CT_head\\CQ500\\%s" % (filename);
    if not os.path.exists(path):
        request.urlretrieve(url, path, fun)

