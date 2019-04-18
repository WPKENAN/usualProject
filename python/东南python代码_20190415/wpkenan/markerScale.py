import shutil
import os
def createMarker(apoPath,scale,X,Y,Z,allMarkerFolder,MulMarkerFolder,isMul=1,is_absolute=1):
    if os.path.exists(allMarkerFolder):
        shutil.rmtree(allMarkerFolder)
    os.mkdir(allMarkerFolder)

    if os.path.exists(MulMarkerFolder):
        shutil.rmtree(MulMarkerFolder)
    os.mkdir(MulMarkerFolder)

    file=open(apoPath);
    lines=file.readlines();
    markers=[];
    mulmarker=[];
    for line in lines:
        z,x,y=line.split(',')[4:7]
        # print(x,y,z)
        if line[0]=="#":
            continue;

        id=int(float(line.split(',')[2]))
        z=float(z)*scale;
        y=float(y)*scale;
        x=float(x)*scale;
        markers.append([x,y,z,id])

    # print(markers)
    # print(len(markers))
    for marker in markers:
        # print(marker)
        # if not os.path.exists(splitFolder + "\\" + "ID({})_{:.3f}_{:.3f}_{:.3f}".format(marker[-1],marker[0], marker[1], marker[2])):
        #     continue
        outfile = open(allMarkerFolder + "\\"+"{}_{:.3f}_{:.3f}_{:.3f}.v3draw.marker".format(marker[-1],marker[0], marker[1], marker[2]),'w')
        # print(outfile)
        outfile.write("##x,y,z,radius,shape,name,comment, color_r,color_g,color_b\n")
        count=0;
        nearIds=[];
        for tmpMarker in markers:
            if max(abs(tmpMarker[0] - marker[0]), abs(tmpMarker[1] - marker[1]), abs(tmpMarker[2] - marker[2]))==0:
                count = count + 1;
                # print(tmpMarker)
                outfile.write("{:.3f},{:.3f},{:.3f},0, 1, , , 246,63,17\n".format(tmpMarker[0],tmpMarker[1],tmpMarker[2]));
                nearIds.append(tmpMarker[3])
                break;
        for tmpMarker in markers:
            # print(max(abs(tmpMarker[0]-block_size),abs(tmpMarker[1]-block_size),abs(tmpMarker[2]-block_size)))
            if abs(tmpMarker[0]-marker[0])<X/2 and abs(tmpMarker[1]-marker[1])<Y/2 and abs(tmpMarker[2]-marker[2]) < Z/2 and max(abs(tmpMarker[0]-marker[0]),abs(tmpMarker[1]-marker[1]),abs(tmpMarker[2]-marker[2]))!=0:
                count=count+1;
                # print(tmpMarker)
                if isMul:
                    outfile.write("{:.3f},{:.3f},{:.3f},0, 1, , , 246,63,17\n".format(tmpMarker[0],tmpMarker[1],tmpMarker[2]));
                # if max(abs(tmpMarker[0]-marker[0]),abs(tmpMarker[1]-marker[1]),abs(tmpMarker[2]-marker[2]))!=0:
                nearIds.append(tmpMarker[3])
        outfile.close()
        if count>1:
            mulmarker.append([marker,count,nearIds]);
            shutil.copy(allMarkerFolder + "\\"+"{}_{:.3f}_{:.3f}_{:.3f}.v3draw.marker".format(marker[-1],marker[0], marker[1], marker[2]),
                        MulMarkerFolder + "\\")
        outfile.close();


    mulmarker=sorted(mulmarker,key=lambda x:x[0][3],reverse=False)
    print("there are {} mulMarkers".format(len(mulmarker)))
    # print(mulmarker)



    outfile=open(allMarkerFolder+"\\..\\somaBlock.csv",'w');
    outfile.write("id,count,nearIds\n")
    for item in mulmarker:
        # print("%d,%s,%s"%(item[0][3],item[1],"dasd"))
        outfile.write("%s,%s,"%(item[0][3],item[1]))
        for i in item[2]:
            outfile.write("{} ".format(i))
        outfile.write("\n")


def scaleApo(apo,scale):
    pass


if __name__=="__main__":
    apopath="C:\\Users\\admin\Desktop\somalist\\18465\\18465.apo"
    tail=apopath.split('\\')[-1].split('.')[0];
    allMarkerFolder=apopath+"\\..\\{}_allMarkerFolder".format(tail)
    MulMarkerFolder=apopath+"\\..\\{}_MulMarkerFolder".format(tail)

    createMarker(apopath,1,512,512,128,allMarkerFolder,MulMarkerFolder,isMul=1)

