import os
folder=".\\data"

count=0;
for file in os.listdir(folder):
    count = count + 1
    newname=file.split('.')[-1]
    # print(newname)
    try:
        os.rename(folder+"\\"+file,folder+"\\"+"{}.{}".format(count,newname))
    except:
        pass
