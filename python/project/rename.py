import os
folder="D:\github\\usualProject\python\wordCnn\images\\"

for file in os.listdir(folder):
    path=folder+"\\"+file
    count=0;
    for file in os.listdir(path):
        count = count + 1
        newname=file.split('.')[1]
        print(newname)
        try:
            os.rename(path+"\\"+file,path+"\\"+"my{}.{}".format(count,newname))
        except:
            pass
