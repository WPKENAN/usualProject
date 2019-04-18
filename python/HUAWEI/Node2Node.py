import queue
import re
import copy

class quadTree:
    def __init__(self,id=0,neighbours=[-1,-1,-1,-1]):
        self.id=id;
        self.neighbours=neighbours;#n e s,w

road = {}
car = {}
cross = {}
crossPair = {}
crossQuadTree={}
carFilePath = ""
roadFilePath = ""
crossFilePath = ""
answerFilePath="1"


# DIRECTION={'u':0,'r':1,'p':2,'l':3}

class roadNode:
    def __init__(self, id=-1, length=-1, speed=-1, channel=-1, from_=-1, to=-1, isDouble=0):
        self.id = id;
        self.length = length;
        self.speed = speed;
        self.channel = channel;
        self.from_ = from_;
        self.to = to;
        self.isDouble = isDouble;
        self.pD = [-1, -1, -1];  # 左,直行,右
        self.nD = [-1, -1, -1];

    def display(self):
        print("{} {} {} {} {} {} {}".format(self.id, self.length, self.speed, self.channel, self.from_, self.to,
                                            self.isDouble))


class crossNode:
    def __init__(self, id=-1, arr=[-1, -1, -1, -1],arrDirection=[-1,-1,-1,-1],neighbours=[-1,-1,-1,-1]):
        self.id = id;
        self.arr = arr;
        self.arrDirection =arrDirection;
        self.neighbours=neighbours;


class carNode:
    def __init__(self, id=-1, from_=-1, to=-1, speed=-1, startTime=-1,path=[]):
        self.id = id;
        self.from_ = from_;
        self.to = to;
        self.speed = speed;
        self.startTime = startTime;
        self.path=path;




def readCar(filePath):
    # (id,from,to,speed,planTime)
    carContent = open(filePath).readlines();
    carMatrix = ""
    for i in range(len(carContent)):
        if carContent[i][0] == "#":
            continue
        carMatrix = carMatrix + carContent[i];

    carMatrix = re.findall('\((.*?)\)', carMatrix)

    for i in range(len(carMatrix)):
        carMatrix[i] = carMatrix[i].split(',');
        for j in range(len(carMatrix[i])):
            carMatrix[i][j] = int(carMatrix[i][j]);
    # print(carMatrix)

    for i in range(len(carMatrix)):
        tmp = carNode(carMatrix[i][0],carMatrix[i][1], carMatrix[i][2], carMatrix[i][3], carMatrix[i][4]);
        car[carMatrix[i][0]] = tmp;
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
        crossPair[(roadMatrix[i][4], roadMatrix[i][5])] = roadNode(roadMatrix[i][0], roadMatrix[i][1], roadMatrix[i][2],
                                                                  roadMatrix[i][3], roadMatrix[i][4], roadMatrix[i][5],
                                                                  roadMatrix[i][6]);
        if roadMatrix[i][6]==1:
            crossPair[(roadMatrix[i][5], roadMatrix[i][4])] = roadNode(roadMatrix[i][0], roadMatrix[i][1],
                                                                      roadMatrix[i][2], roadMatrix[i][3],
                                                                      roadMatrix[i][5],
                                                                      roadMatrix[i][4], roadMatrix[i][6]);

        road[roadMatrix[i][0]] = roadNode(roadMatrix[i][0], roadMatrix[i][1], roadMatrix[i][2],
                                          roadMatrix[i][3], roadMatrix[i][4], roadMatrix[i][5],
                                          roadMatrix[i][6]);

    # crossPair[(1,2)].display();
    # for key in crossPair:
    # print(key)
    # crossPair[key].display()


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
        tmp = crossNode(crossMatrix[i][0],
                        [crossMatrix[i][1], crossMatrix[i][2], crossMatrix[i][3], crossMatrix[i][4]]);
        cross[crossMatrix[i][0]] = tmp;


def linkRoad():

    #规定第一个直行是正北
    for key in cross:
        crossQuadTree[key]=quadTree(id=key);
        # notVis.add(key);

    tmpDir = 0;
    isVis = set();
    tmpQueue = queue.Queue();
    tmpQueue.put([1,cross[1].arr[0],0]);

    while not tmpQueue.empty():

        curNode = tmpQueue.get();
        tmpId=curNode[0];
        tmpDir=curNode[2];

        tmpCross=copy.deepcopy(cross[tmpId]);
        tmpTargetId=tmpId;
        tmpIndex=tmpCross.arr.index(curNode[1]);

        for i in range(4):

            if tmpCross.arr[(i+tmpIndex)%4]==-1:
                continue
            tmpCross.arrDirection[(i+tmpIndex)%4]=(tmpDir+i)%4;

            if road[tmpCross.arr[(i+tmpIndex)%4]].from_==tmpId:
                tmpTargetId=road[tmpCross.arr[(i+tmpIndex)%4]].to;
            else:
                tmpTargetId=road[tmpCross.arr[(i+tmpIndex)%4]].from_;

            if (tmpId,tmpTargetId) in crossPair:
                tmpCross.neighbours[(tmpDir+i)%4] = tmpTargetId;
            # else:
            #     print(tmpId,tmpTargetId)

            if tmpTargetId not in isVis:
                tmpQueue.put([tmpTargetId,tmpCross.arr[(i+tmpIndex)%4],(tmpDir+i+2)%4]);
                isVis.add(tmpTargetId)

        cross[tmpId]=tmpCross


    # for key in cross:
    #     print("{} {} {} {}".format(cross[key].id,cross[key].arr,cross[key].arrDirection,cross[key].neighbours));



def main(fileFolder):
    carFilePath = fileFolder + "\\car.txt"
    roadFilePath = fileFolder + "\\road.txt"
    crossFilePath = fileFolder + "\\cross.txt"
    # print(answerFilePath)
    global  answerFilePath
    answerFilePath=fileFolder+"\\answer.txt"

    # print(answerFilePath)
    carMatrix = readCar(carFilePath);
    roadMatrix = readRoad(roadFilePath);
    crossMatrix = readCross(crossFilePath);

    linkRoad();
    floyd();

def floyd():

    MAX=float('inf')
    crossList=cross.keys();
    floydMap = [[MAX]*(len(crossList)+1) for i in range(len(crossList)+1)];
    path=[[MAX]*(len(crossList)+1) for i in range(len(crossList)+1)];
    dis = [[MAX] * (len(crossList) + 1) for i in range(len(crossList) + 1)];

    for i in crossList:
        floydMap[i][i]=0;
        dis[i][i]=0;
        for j in cross[i].neighbours:
            if j == -1:
                continue
            floydMap[i][j]=crossPair[(i,j)].length/crossPair[(i,j)].speed;
            dis[i][j]=floydMap[i][j];

    for i in crossList:
        for j in crossList:
            if floydMap[i][j]==MAX:
                path[i][j]=0;
            else:
                path[i][j]=i;

    # for i in range(1,len(floydMap)):
    #     for j in range(1,len(floydMap)):
    #         print("{:.0f} ".format(path[i][j]),end='')
    #
    #     print('')

    for k in range(1,len(floydMap)):
        for i in range(1,len(floydMap)):
            for j in range(1,len(floydMap)):
                if dis[i][j] > dis[i][k]+dis[k][j]:
                    dis[i][j]=dis[i][k]+dis[k][j];
                    path[i][j]=path[k][j];

    # for i in range(1,len(floydMap)):
    #     for j in range(1,len(floydMap)):
    #         print("{:.1f} ".format(dis[i][j]),end='')
    #
    #     print('')

    # for i in range(1,len(floydMap)):
    #     for j in range(1,len(floydMap)):
    #         print("{:.0f} ".format(path[i][j]),end='')
    #
    #     print('')
    # print(floydMap)

    # for i in range(1,len(floydMap)):
    #     print(floydMap[i])


    # for key in cross:
    #     print("{} {} {} {}".format(cross[key].id,cross[key].arr,cross[key].arrDirection,cross[key].neighbours));

    # for i in range(1,len(floydMap)):
    #     for j in range(1,len(floydMap)):
    #         print("{}-->{} {}".format(i,j,printPath(path,i,j)))

    outfile=open(answerFilePath,'w');

    for key in car:
        # print(key)
        tmpCar=copy.deepcopy(car[key]);

        tmpFrom_=tmpCar.from_;
        tmpTo=tmpCar.to;

        # print(tmpFrom_)
        # print(tmpTo)
        # print(printPath(path,tmpFrom_,tmpTo))
        tmpCar.path=printPath(path,tmpFrom_,tmpTo);
        car[key]=copy.deepcopy(tmpCar);

        # print("{},{}".format(tmpCar.id,tmpCar.startTime),end='');
        # for i in range(len(tmpCar.path)-1):
        #     print(",{}".format(crossPair[(tmpCar.path[i],tmpCar.path[i+1])].id),end='');
        # print("")

        outfile.write("({},{}".format(tmpCar.id,tmpCar.startTime));
        for i in range(len(tmpCar.path)-1):
            outfile.write(",{}".format(crossPair[(tmpCar.path[i],tmpCar.path[i+1])].id));
        outfile.write(")\n")
        del tmpCar


def printPath(path,start,target):
    pathList=[];

    pathList.append(target)
    while target!=start:
        pathList.append(path[start][target]);
        target=path[start][target];
    pathList.reverse()
    return pathList



def dijkstra():
    pass

if __name__ == '__main__':
    main("D:\github\Data\HUAWEI\\2019软挑-初赛-SDK\SDK\SDK_python\CodeCraft-2019\config_wp")
    # a=roadNode(1,2,3,4,5,6,7);
    # print("road")
    # for key in road:
    #     # print(key)
    #     print("{} {} {} {} {} {} {} {} {}".format(road[key].id, road[key].length, road[key].speed, road[key].channel, road[key].from_, road[key].to,
    #                                         road[key].isDouble,road[key].pD,road[key].pD))

