import pandas as pd
import itertools
import copy


def readCsv(path):
    data=pd.read_excel(path,sheetname=0,header=-1)
    data=data.values
    print(data.shape)
    return data[:,0],data[:,1:]

def dealData(data):
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            # print(type(data[i,j]))
            if type(data[i,j])==str:
                if "分钟" in data[i,j]:
                    data[i, j] = data[i, j].replace('分钟', '')
                    data[i,j]=float(data[i,j])/60
                else:
                    data[i,j]=data[i,j].replace('小时','')
            data[i,j]=float(data[i,j])
    print(data.shape)


def floyd(data):
    MAX=float('inf')
    path = [[MAX] * (data.shape[0]) for i in range(data.shape[0])];
    dis = [[MAX] * (data.shape[0]) for i in range(data.shape[0])];

    # 更改权值为1
    for i in range(data.shape[0]):
        data[i,i] = 0
        for j in range(data.shape[0]):
            dis[i][j]=data[i,j];


    for i in range(data.shape[0]):
        for j in range(data.shape[0]):
            if data[i,j] == MAX:
                path[i][j] = -1;
            else:
                path[i][j] = i;

    for k in range(data.shape[0]):
        for i in range(data.shape[0]):
            for j in range(data.shape[0]):
                if dis[i][j] > dis[i][k] + dis[k][j]:
                    dis[i][j] = dis[i][k] + dis[k][j];
                    path[i][j] = path[k][j];
    # print(dis[0][3])
    # print(path[0][3])
    return dis,path

def printPath(path,start,target):
    pathList=[];

    pathList.append(target)
    while target!=start:
        pathList.append(path[start][target]);
        target=path[start][target];
    pathList.reverse()
    return pathList

def showOnePoint(start,target,name,indexDict,dis,path):
    print("最短距离是:{}".format(dis[indexStart][indexTarget]))

    shortestPath = printPath(paths, indexStart, indexTarget)
    print("最短路径是:",end="")
    for item in shortestPath:
        print(name[item], end='->')
    print('')

def showOnePointList(start,targets,name,indexDict,dis,path):
    minTargetList=copy.deepcopy(targets)
    minDistance=float('inf');
    for item in itertools.permutations(targets,len(targets)):
        distance=dis[start][item[0]];
        for i in range(len(item)-1):
            distance=dis[item[i]][item[i+1]]
        if distance < minDistance:
            minDistance=distance;
            minTargetList=copy.deepcopy(item)


    return minTargetList,minDistance

if __name__=="__main__":
    filepath="data.xlsx"
    name,data=readCsv(filepath)
    dealData(data)

    indexDict = {}
    for i in range(len(name)):
        indexDict[name[i]]=i;

    #floyd算法
    dis,paths=floyd(data)

    #show 一个点到另一个点的最短路径
    start=1;
    target=51
    indexStart = indexDict[start]
    indexTarget = indexDict[target]
    print("{}->{}".format(start, target))
    showOnePoint(indexStart,indexTarget,name,indexDict,dis,paths)

    print('**************************************')
    #show一个点到另一群点的总的最短路径
    start=1;
    targets = [3, 4, 59,48];
    print("{}->{}".format(start,targets))
    indexStart = indexDict[start]
    indexTargets = copy.deepcopy(targets)
    for i in range(len(targets)):
        indexTargets[i]=indexDict[targets[i]]
    # print("在矩阵中的序号:{}->{}".format(indexStart, indexTargets))
    minTargetList, minDistance=showOnePointList(indexStart, indexTargets, name, indexDict, dis, paths)

    TargetList=copy.deepcopy(targets)
    for i in range(len(minTargetList)):
        TargetList[i]=name[minTargetList[i]]
    print("最短距离为:{}   访问顺序是:{}".format(minDistance,TargetList))

    result=[printPath(paths,indexStart,minTargetList[0])]
    for i in range(len(minTargetList)-1):
        result=result[:-1]
        result.extend(printPath(paths,minTargetList[i],minTargetList[i+1]))
    for i in range(len(result)):
        result[i]=name[result[i]]
    print("最短路径是:", end="")
    for item in result:
        print(item, end='->')
    print('')
    print(result)











