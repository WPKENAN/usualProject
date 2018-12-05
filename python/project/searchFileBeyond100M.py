import os.path
import fnmatch
import glob
import os


def recursiveSearchFiles(dirPath, partFileInfo):
    fileList = []
    # print(os.path.join('\\', dirPath, '*'))
    pathList = glob.glob(os.path.join('\\', dirPath, '*'))  # windows path

    # print 'pathList = '
    # print pathList
    # print([partFileInfo])
    for mPath in pathList:
        # print([partFileInfo,mPath])
        # print mPath
        if fnmatch.fnmatch(mPath, partFileInfo):
            fileList.append(mPath)  # 符合条件条件加到列表
        elif os.path.isdir(mPath):
            # print mPath
            fileList += recursiveSearchFiles(mPath, partFileInfo)  # 将返回的符合文件列表追加到上层
        else:
            pass
    return fileList


def gci(filepath,allFile):
#遍历filepath下所有文件，包括子目录
    files = os.listdir(filepath)
    for fi in files:
        fi_d = os.path.join(filepath,fi)
        if os.path.isdir(fi_d):
            # print(os.path.join(filepath, fi_d))
            gci(fi_d,allFile)
        else:
            # print(os.path.join(filepath,fi_d))#递归遍历/root目录下所有文件
            allFile.append(os.path.join(filepath,fi_d))

# def test():
#     allFile.append(10)
#     print(allFile)

if __name__=='__main__':
    allFile=[]
    # test()
    gci("D:\\github",allFile);
    print("文件总数:%d"%(len(allFile)));
    # paths = recursiveSearchFiles("D:\github\Data", "*.*")  # windows path
    paths=sorted(allFile,key=lambda x:os.path.getsize(x),reverse=True)

    for path in paths:
        print("%s    %sMB"%(path, round(os.path.getsize(path)/1024/1024)))
        if os.path.getsize(path)/1024/1024 < 95:
            break;
