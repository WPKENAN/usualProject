import os
import sys
import shutil

def _20181225_():
    path="D:\github\Data\CT_head\head-ct-hemorrhage\\head_ct"
    labelpath="D:\github\Data\CT_head\head-ct-hemorrhage\\labels.csv"
    labelsfile=open(labelpath).readlines();
    # print(labels)

    labels={}
    for line in labelsfile:
        line=line.strip('\n');
        line=line.split(',');
        print(line)
        if line[0]=="id":
            continue
        labels[int(line[0])]=int(line[1])
    print(labels)


    if not os.path.exists(path+"\\..\\split\\hemorrhage"):
        os.mkdir(path+"\\..\\split\\hemorrhage")
    if not os.path.exists(path+"\\..\\split\\normal"):
        os.mkdir(path+"\\..\\split\\normal")

    for file in os.listdir(path):
        # print(file)
        if labels[int(file.split('.')[0])]:
            shutil.copy(path+"\\"+file,path+"\\..\\split\\hemorrhage"+"\\"+file);
        else:
            shutil.copy(path + "\\" + file, path + "\\..\\split\\normal\\" + "\\" + file);

def _20181225_1_():
    manpath="D:\github\Data\knee\knee\man"
    womanpath="D:\github\Data\knee\knee\woman"
    mancsvpath="D:\github\Data\knee\knee\man.csv";
    womancsvpath="D:\github\Data\knee\knee\woman.csv"

    mancsvfile=open(mancsvpath).readlines();
    womancsvfile=open(womancsvpath).readlines();

    mancsv={};
    womancsv={};

    # print(mancsvfile)
    for line in mancsvfile:
        line=line.strip('\n')
        line=line.split(',')
        # print(line[2:5])
        if line[2]=='':
            line[2]='-1';
        if line[3]=='':
            line[3]='-1';
        if line[4]=='':
            line[4]='-1';
        mancsv[line[0]]=[int(line[2]),int(line[3]),int(line[4])]
        # print(line)
    # print(mancsv)
    for line in womancsvfile:
        line=line.strip('\n')
        line=line.split(',')
        # print(line[2:5])
        if line[2]=='':
            line[2]='-1';
        if line[3]=='':
            line[3]='-1';
        if line[4]=='':
            line[4]='-1';
        womancsv[line[0]]=[int(line[2]),int(line[3]),int(line[4])]

    # print(mancsv)
    # print(womancsv)

    for file in os.listdir(manpath):
        # print(file)
        if file.split('_')[0] in mancsv:
            # print(mancsv[file.split('_')[0]][0])
            for i in range(3):
                if not os.path.exists(manpath + "\\..\\database\\{}\\".format(i)):
                    os.mkdir(manpath + "\\..\\database\\{}\\".format(i))
                if not os.path.exists(manpath+"\\..\\database\\{}\\".format(i)+"{}".format(mancsv[file.split('_')[0]][i])):
                    os.mkdir(manpath+"\\..\\database\\{}\\".format(i)+"{}".format(mancsv[file.split('_')[0]][i]))
                shutil.copy(manpath+"\\"+file,manpath+"\\..\\database\\{}\\".format(i)+"{}".format(mancsv[file.split('_')[0]][i])+"\\"+file)

    for file in os.listdir(womanpath):
        # print(file)
        if file.split('_')[0] in womancsv:
            # print(mancsv[file.split('_')[0]][0])
            for i in range(3):
                if not os.path.exists(manpath + "\\..\\database\\{}\\".format(i)):
                    os.mkdir(manpath + "\\..\\database\\{}\\".format(i))
                if not os.path.exists(manpath+"\\..\\database\\{}\\".format(i)+"{}".format(womancsv[file.split('_')[0]][i])):
                    os.mkdir(manpath+"\\..\\database\\{}\\".format(i)+"{}".format(womancsv[file.split('_')[0]][i]))
                shutil.copy(womanpath+"\\"+file,womanpath+"\\..\\database\\{}\\".format(i)+"{}".format(womancsv[file.split('_')[0]][i])+"\\"+file)

        # pass

def _20181225_2_():
    commandStr="activate py35 & python 2015train.py";
    flag=os.system(commandStr)
    count=0;
    while flag:
        file=open("log1.txt").readlines();

        outfile2 = open("log2.txt", 'a');
        outfile2.write(file[0] + "\n")

        tmp=file[0].split("..\\cache\\");
        print((tmp[0]+tmp[1]).strip('.'))
        print("--------------")
        os.remove((tmp[0]+tmp[1]).strip('.txt'))
        count=count+1
        flag = os.system(commandStr)

        print("------------------------: ",count)





if __name__=="__main__":
    # _20181225_();
    # _20181225_1_()
    _20181225_2_()