import shutil
import os

if __name__=="__main__":
    folder=".\\images"
    targetFolder=".\\train"
    count=1;
    for subfolder in os.listdir(folder):
        for imgfile in os.listdir(os.path.join(folder,subfolder)):
            print(os.path.join(folder,subfolder,imgfile))
            if not os.path.exists(os.path.join(targetFolder,subfolder)):
                os.mkdir(os.path.join(targetFolder,subfolder))
            shutil.copy(os.path.join(folder,subfolder,imgfile),os.path.join(targetFolder,subfolder,"{}.{}".format(count,imgfile.split('.')[-1])))
            count+=1
