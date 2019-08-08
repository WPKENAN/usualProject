import re
import pandas as pd
import os
import shutil

def remove_chinese(string):
    # string = 'abc测试123..._<>《》！*(^)$%~!@#$…&%￥—+=、。，；‘’“”：·`中文'
    rule = re.compile(r"[^a-zA-Z0-9.\-_]")
    line = rule.sub('', string)
    # print(line)
    line=line.replace('-',"_")
    line=line.replace('____','_')

    print(string,line)
    if '.jpg' in line:
        line=line.split('.')[0]
        nums=line.split('_')
        line=''
        for num in nums:
            line+=str(int(num))+"_"
        line=line.strip('_')+'.jpg'
    if '.gif' in line:
        line=line.split('.')[0]
        nums=line.split('_')
        line=''
        for num in nums:
            line+=str(int(num))+"_"
        line=line.strip('_')+'.gif'

    return line

def readxlsx(path,target):
    df=pd.read_excel(path);
    data=df.values[:,:]
    print(data)
    m,n=data.shape

    result=[]
    for j in range(n):
        for i in range(m):
            # print(type(data[i,j])==type("da"))
            if type(data[i,j])==type("a") and '-' in data[i,j]:
                result.append([data[i,j-1],remove_chinese(data[i,j]),1 if data[i,j+1]==1 else 0])

    print(len(result))
    result=pd.DataFrame(result)
    print(result.shape)
    # print(df.shape)
    result.to_excel(target)
def readimage(path,target):
    pass
if __name__=="__main__":
    path="./raw_data/add.xlsx"
    target="./data/add.xlsx"
    readxlsx(path,target)
    #
    path = "./raw_data/sub.xlsx"
    target = "./data/sub.xlsx"
    readxlsx(path, target)

    path="./raw_data/add"
    target="./data/add"
    if os.path.exists(target):
        shutil.rmtree(target)
    os.mkdir(target)

    for folder in os.listdir(path):
        if os.path.exists(os.path.join(target,folder)):
            shutil(os.path.join(target,folder))
        os.mkdir(os.path.join(target,folder))
        for file in os.listdir(os.path.join(path,folder)):
            shutil.copy(os.path.join(path,folder,file),os.path.join(target,folder,remove_chinese(file)))

    path = "./raw_data/sub"
    target = "./data/sub"
    if os.path.exists(target):
        shutil.rmtree(target)
    os.mkdir(target)

    for folder in os.listdir(path):
        if os.path.exists(os.path.join(target, folder)):
            shutil(os.path.join(target, folder))
        os.mkdir(os.path.join(target, folder))
        for file in os.listdir(os.path.join(path, folder)):
            shutil.copy(os.path.join(path, folder, file), os.path.join(target, folder, remove_chinese(file)))