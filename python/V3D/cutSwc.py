import os
import sys
def prunSwcFile(swcPath,outPath):
    swcfile=open(swcPath);
    swclines=swcfile.readlines();
    swc={}
    for line in swclines:
        if line[0]=="#":
            continue
        line=line.strip('\n')
        line=line.split(' ');
        n=int(line[0]);
        type=int(line[1]);
        x=float(line[2]);
        y = float(line[3]);
        z = float(line[4]);
        radius=float(line[5]);
        parent=int(line[6]);
        isIn=1;
        # swc.append([n,type,x,y,z,radius,parent]);
        # if n==1:
        #     isIn=1;
        swc[n]=[n,type,x,y,z,radius,parent,isIn];


    indexAll=list(swc.keys());
    indexAll.sort(reverse=True);
    # print(indexAll)

    for index in indexAll:
        # print(swc[index])
        isIn = swc[index][-1]
        pid = index
        # print(index)
        # print(pid)
        while isIn:
            pid = swc[pid][-2];
            if pid==-1:
                break;
            if pid not in swc:
                break;
        # print("out:{} pid={}".format(index,pid))
        if pid==-1:
            continue;

        isIn = swc[index][-1]
        pid = index;
        while isIn:
            swc[pid][5] = -1
            swc[pid][-1] = 0;
            pid = swc[pid][-2];
            if pid == -1:
                break;
            if pid not in swc:
                break;

    outfile=open(outPath,'w');
    print(swcPath)
    if len(indexAll)==0:
        print("{} is empty")
        return;
    outfile.write("#base index={}-->1\n".format(min(indexAll)))
    outfile.write("##n,type,x,y,z,radius,parent\n");
    indexAll.sort();
    # print(len(indexAll))
    count=0;
    for index in indexAll:
        # print(swc[index])
        if swc[index][5]<0:
            continue
        count=count+1;
        outfile.write("{} {} {} {} {} {} {}\n".format(swc[index][0]-min(indexAll)+1,swc[index][1],swc[index][2],swc[index][3],swc[index][4],swc[index][5],max(-1,swc[index][6]-min(indexAll)+1)))
    print("ID({}) before prun:{} after prun:{} pruned number:{}".format(swcPath,len(indexAll),count,len(indexAll)-count))

def prunSwcFolder(readFolder,writerFolder):
    print(sys._getframe().f_code.co_name+":")
    if not os.path.exists(writerFolder):
        os.mkdir(writerFolder)
    for i in os.listdir(readFolder):
        prunSwcFile(readFolder+"\\"+i,writerFolder+"\\"+i);

def cutManualSwc(srcManualSwcFolder,tarManualSwcFolder,apoPath,x_scale,y_scale,z_scale):
    print(sys._getframe().f_code.co_name + ":")
    # srcManualSwcFolder="D:\soamdata\\17302\\17302_Whole"
    # tarManualSwcFolder=srcManualSwcFolder+"_Cut"
    if not os.path.exists(tarManualSwcFolder):
        os.mkdir(tarManualSwcFolder);

    markerDict={};
    file = open(apoPath);
    lines = file.readlines();
    for line in lines:
        z, x, y = line.split(',')[4:7]
        # print(x,y,z)
        if line[0] == "#":
            continue;

        id = int(float(line.split(',')[2]))
        z = float(z);
        y = float(y);
        x = float(x);
        # markers.append([x, y, z, id])
        markerDict[id]=[x,y,z];

    # print(markerDict)
    count=0;
    count2=0
    for swc in os.listdir(srcManualSwcFolder):
        if swc[-4:]==".swc" or swc[-5:]==".eswc":
            count=count+1;
            print(swc.split('_')[-1])
            try:
                if (int)(swc.split('_')[-1].split('.')[0]) not in markerDict:
                    continue
            # print(int(swc.split('_')[1]))

                # print(swc.split('_')[-1].split('.')[0])
                # if not swc.split('_')[-1].split('.')[0].isdigit():
                #     continue
                xcenter=markerDict[int(swc.split('_')[-1].split('.')[0])][0];
                ycenter = markerDict[int(swc.split('_')[-1].split('.')[0])][1];
                zcenter = markerDict[int(swc.split('_')[-1].split('.')[0])][2];

            except:
                continue

            # print(srcManualSwcFolder+"\\"+swc)
            swcfile=open(srcManualSwcFolder+"\\"+swc);
            swclines=swcfile.readlines();
            outfile=open(tarManualSwcFolder+"\\"+swc,'w');


            for line in swclines:

                if line[0]=="#":
                    outfile.write(line);
                    continue;
                line=line.strip('\n');
                line=line.split(' ');

                if abs(float(line[2])-xcenter)<x_scale and abs(float(line[3])-ycenter)<y_scale and abs(float(line[4])-zcenter)<z_scale:
                    line[5] = '1.0'
                    line[2] = x_scale + round((float(line[2]) - xcenter));
                    line[3] = y_scale + round((float(line[3]) - ycenter));
                    line[4] = z_scale + round((float(line[4]) - zcenter));
                    # print(xcenter, ycenter, zcenter)
                    # print(line[2],line[3],line[4],line[5],line[6])
                    outfile.write("{} {} {} {} {} {} {}\n".format(line[0],line[1],line[2],line[3],line[4],line[5],line[6]));
            # sada
        elif swc[-4:]=="eswc":
            count2=count2+1;

if __name__=="__main__":
    srcManualSwcFolder="C:\\Users\\Anzhi\\Desktop\\17302_Whole"
    tarManualSwcFolder=srcManualSwcFolder+"\\..\\cut"
    tarManualSwcFolder_prun=srcManualSwcFolder+"\\..\\prun"
    apoPath = "D:\soamdata\\17302\\17302.apo"
    cutManualSwc(srcManualSwcFolder,tarManualSwcFolder,apoPath,512,512,128);
    prunSwcFolder(tarManualSwcFolder,tarManualSwcFolder_prun)