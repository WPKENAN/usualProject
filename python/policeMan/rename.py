import os
folder="D:\github\\usualProject\matlab\\acc90\simple_classes"

for file1 in os.listdir(folder):
    path=folder+"\\"+file1
    count=0;

    for file in os.listdir(path):
        count = count + 1
        newname=file.split('.')[-1]
        print(newname)
        try:
            os.rename(path+"\\"+file,path+"\\"+"{}my{}.{}".format(file1,count,newname))
        except:
            pass
