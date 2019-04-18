import cv2 as cv
import numpy as np
import queue
import re

road={}
car={}
cross={}
roadPair={}

# DIRECTION={'u':0,'r':1,'p':2,'l':3}

class roadNode:
    def __init__(self,id=0,length=0,speed=0,channel=0,from_=0,to=0,isDouble=0):
        self.id=id;
        self.length=length;
        self.speed=speed;
        self.channel=channel;
        self.from_=from_;
        self.to=to;
        self.isDouble=isDouble;
        self.pD=[-1,-1,-1];#左,直行,右
        self.nD=[-1,-1,-1];

    def display(self):
        print("{} {} {} {} {} {} {}".format(self.id,self.length,self.speed,self.channel,self.from_,self.to,self.isDouble))

class crossNode:
    def __init__(self,id=0,u=0,r=0,p=0,l=0,arr=[-1,-1,-1,-1]):
        self.id=id;
        self.u=u;
        self.r=r;
        self.p=p;
        self.l=l;
        self.arr=arr;

class carNode:
    def __init__(self,id=0,from_=0,to=0,speed=0,startTime=0):
        self.id=id;
        self.from_=from_;
        self.to=to;
        self.speed=speed;
        self.time=startTime;

def readCar(filePath):
    # (id,from,to,speed,planTime)
    carContent=open(filePath).readlines();
    carMatrix = ""
    for i in range(len(carContent)):
        if carContent[i][0]=="#":
            continue
        carMatrix=carMatrix+carContent[i];

    carMatrix=re.findall('\((.*?)\)',carMatrix)

    for i in range(len(carMatrix)):
        carMatrix[i]=carMatrix[i].split(',');
        for j in range(len(carMatrix[i])):
            carMatrix[i][j]=int(carMatrix[i][j]);
    # print(carMatrix)
    return carMatrix

def readRoad(filePath):
    # (id,length,speed,channel,from,to,isDuplex)
    roadContent = open(filePath).readlines();
    roadMatrix = ""
    # print(roadContent)
    for i in range(len(roadContent)):
        if roadContent[i][0] == "#":
            continue
        roadMatrix = roadMatrix + roadContent[i];

    roadMatrix = re.findall('\((.*?)\)', roadMatrix)

    for i in range(len(roadMatrix)):
        roadMatrix[i] = roadMatrix[i].split(',');
        for j in range(len(roadMatrix[i])):
            roadMatrix[i][j] = int(roadMatrix[i][j]);

    # print(roadMatrix)
    # return roadMatrix
    for i in range(len(roadMatrix)):
        roadPair[(roadMatrix[i][4],roadMatrix[i][5])]=roadNode(roadMatrix[i][0], roadMatrix[i][1], roadMatrix[i][2],
                                                               roadMatrix[i][3], roadMatrix[i][4],roadMatrix[i][5],
                                                               roadMatrix[i][6]);
        # if roadMatrix[i][6]==1:
        #     roadPair[(roadMatrix[i][5], roadMatrix[i][4])] = roadNode(roadMatrix[i][0], roadMatrix[i][1],
        #                                                               roadMatrix[i][2], roadMatrix[i][3],
        #                                                               roadMatrix[i][5],
        #                                                               roadMatrix[i][4], roadMatrix[i][6]);

        road[roadMatrix[i][0]]=roadNode(roadMatrix[i][0], roadMatrix[i][1], roadMatrix[i][2],
                                                               roadMatrix[i][3], roadMatrix[i][4],roadMatrix[i][5],
                                                               roadMatrix[i][6]);

    # roadPair[(1,2)].display();
    # for key in roadPair:
        # print(key)
        # roadPair[key].display()


def readCross(filePath):
    # (id,roadId,roadId,roadId,roadId)
    crossContent = open(filePath).readlines();
    crossMatrix = ""
    # print(crossContent)
    for i in range(len(crossContent)):
        if crossContent[i][0] == "#":
            continue
        crossMatrix = crossMatrix + crossContent[i];

    crossMatrix = re.findall('\((.*?)\)', crossMatrix)

    for i in range(len(crossMatrix)):
        crossMatrix[i] = crossMatrix[i].split(',');
        for j in range(len(crossMatrix[i])):
            crossMatrix[i][j] = int(crossMatrix[i][j]);
    # print(crossMatrix)
    # return  crossMatrix

    for i in range(len(crossMatrix)):
        tmp = crossNode(crossMatrix[i][0], crossMatrix[i][1], crossMatrix[i][2], crossMatrix[i][3], crossMatrix[i][4],[crossMatrix[i][1], crossMatrix[i][2], crossMatrix[i][3], crossMatrix[i][4]]);
        cross[crossMatrix[i][0]] = tmp;


def linkRoad():

    for key in cross:
        for i in range(4):
            crossArr=cross[key].arr
            # print(crossArr)
            if crossArr[i]==-1:
                continue
            from_=road[crossArr[i]].from_;
            to=road[crossArr[i]].to;

            if to==key:

                tmpPD=[crossArr[(i+1)%4],crossArr[(i+2)%4],crossArr[(i+3)%4]];
                for j in range(len(tmpPD)):
                    if tmpPD[j]!=-1 and road[tmpPD[j]].isDouble==0 and key!=road[tmpPD[j]].from_:
                        tmpPD[j]=-1;
                road[crossArr[i]].pD=tmpPD;


            elif from_ == key:
                # road[crossArr[i]].nD = [crossArr[(i + 1) % 4], crossArr[(i + 2) % 4], crossArr[(i + 3) % 4]];
                tmpND = [crossArr[(i + 1) % 4], crossArr[(i + 2) % 4], crossArr[(i + 3) % 4]];
                for j in range(len(tmpND)):
                    if tmpND[j] != -1 and road[tmpND[j]].isDouble == 0 and key != road[tmpND[j]].from_:
                        tmpND[j] = -1;
                road[crossArr[i]].nD = tmpND;




    for key in road:
        print("{} {}——>{} 正向: {}  负向: {}".format(road[key].id,road[key].from_,road[key].to,road[key].pD,road[key].nD))

def outGraph():
    pass
    # for key in road:
    #     print("{} {}——>{} 正向: {}  负向: {}".format(road[key].id,road[key].from_,road[key].to,road[key].pD,road[key].nD))
    # notVis=set([]);
    # for key in road:
    #     notVis.add(key);
    #
    # maxX=800;
    # maxY=maxX;
    # canvas = np.zeros((maxX, maxY, 3), dtype="uint8")
    # # 画绿线
    # green = (0, 255, 0)
    # red=(255,0,0);
    #
    #
    #
    # length=50
    # startX=int(maxX/2);
    # startY=int(maxY/2);
    # endX=startX+length;
    # endY=startY;
    #
    # cv.arrowedLine(canvas, (startX, startY), (endX, endY), green, 2)
    # cv.arrowedLine(canvas, (endX, endY), (startX, startY), green, 2)
    # cv.imshow("Canvas", canvas)
    # cv.waitKey(0)
    #
    # cur_roadId = min(road.keys());
    # dirc=0;#0是正向 1是负向
    #
    # bfsQueue =queue.Queue();
    # bfsQueue.put([cur_roadId,0]);
    # while(len(notVis)):
    #     queueTop=bfsQueue.get();
    #     tmpRoad=road[queueTop[0]];
    #
    #     if tmpRoad.isDouble==1:
    #         cv.arrowedLine(canvas, (startX, startY), (endX, endY), green, 2);
    #         cv.arrowedLine(canvas, (endX, endY), (startX, startY), green, 2);
    #
    #
    #     if queueTop[1]==0:
    #         for i in tmpRoad.pD:
    #             if i!=-1:
    #                 return;



    # cv.line(canvas, (startX, startY), (endX, endY), green, 2)
    # cv.imshow("Canvas", canvas)
    # cv.waitKey(0)

    # notVis.remove(minKey);






def main(fileFolder):
    carFilePath=fileFolder+"\\car.txt"
    roadFilePath=fileFolder+"\\road.txt"
    crossFilePath=fileFolder+"\\cross.txt"

    carMatrix=readCar(carFilePath);
    roadMatrix=readRoad(roadFilePath);
    crossMatrix=readCross(crossFilePath);


    linkRoad()
    outGraph()


if __name__ == '__main__':
    main("D:\github\Data\HUAWEI\\2019软挑-初赛-SDK\SDK\SDK_python\CodeCraft-2019\config_wp")
    # a=roadNode(1,2,3,4,5,6,7);
    # print("road")
    # for key in road:
    #     # print(key)
    #     print("{} {} {} {} {} {} {} {} {}".format(road[key].id, road[key].length, road[key].speed, road[key].channel, road[key].from_, road[key].to,
    #                                         road[key].isDouble,road[key].pD,road[key].pD))

