# import time
# N = 1000+3
# for i in range(N):
#     print("进度:{0}%".format((i + 1) * 100 / N), end="\r")
#     time.sleep(0.01)
#
# import pickle
# import tensorflow as tf
#
# datalist_file=""
# def Open(name, mode='r'):
#     """
#     because, in my environment, sometimes gfile.Open is very slow when target file is localpath(not gs://),
#     so, use normal open if the target path is localpath.
#     """
#     if len(name) >= 5 and name[:5] == 'gs://':
#         # return tf.gfile.Open(name, mode)
#     else:
#         return open(name, mode)
#
# with Open(datalist_file, 'rb') as f:
#     datalist = pickle.load(f)
#     for i in datalist:
#         print(i)

# file=open("D:\wp\BaiduNetdiskDownload\homework\\data.txt");
# contents=file.readlines();
#
# for i in range(len(contents)):
#     str=("D:\wp\BaiduNetdiskDownload\homework\\new\\%d.txt")%(i)
#     tmp=open(str,"w");
#     tmp.write(contents[i])
#     tmp.close();
#     if i>1000:
#         break
# file.close()
path="E:\\18.txt"
file=open(path);
contents=file.readlines();
output=open("E:\\cmy.txt",'w');

for i in len(contents):
    contents[i]=contents[i].strip('\n');
