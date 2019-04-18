def readCsv(path1,path2):
    file=open(path1,encoding='utf8');
    contents=file.readlines();
    contents=contents[1:len(contents)]
    station={}
    for i in range(len(contents)):
        contents[i]=contents[i].strip('\n').split(',');
        contents[i][1]=int(contents[i][1])
        # print(contents[i])
        station[contents[i][1]]=contents[i][0]
    # print(station)
    file.close()
    #################################################
    MAX = float('inf')
    stationList = station.keys();
    stationMap=[[MAX]*(len(station)+1) for i in range(len(station)+1)]

    file = open(path2, encoding='utf8');
    contents = file.readlines();
    contents = contents[1:len(contents)]
    for i in range(len(contents)):
        contents[i] = contents[i].strip('\n').split(',');
        startStation = int(contents[i][0])
        endStation = int(contents[i][1])
        # print(contents[i])
        stationMap[startStation][endStation]=float(contents[i][2]);
        stationMap[endStation][startStation] = float(contents[i][2]);#无向图，权是excel
    # print(stationMap)
    # print(stationMap[80][16])
    file.close()
    return station,stationMap


def floyd(station,stationMap):
    MAX=float('inf')
    path=[[MAX]*(len(station)+1) for i in range(len(station)+1)];
    dis = [[MAX] * (len(station) + 1) for i in range(len(station) + 1)];

    #更改权值为1
    for i in range(len(station)+1):
        stationMap[i][i]=0
        for j in range(len(station)+1):
            # dis[i][j]=stationMap[i][j];
            if stationMap[i][j]<MAX:
                dis[i][j]=1;


    for i in range(len(station)):
        for j in range(len(station)):
            if stationMap[i][j]==MAX:
                path[i][j]=0;
            else:
                path[i][j]=i;

    for k in range(1,len(station)+1):
        for i in range(1,len(station)+1):
            for j in range(1,len(station)+1):
                if dis[i][j] > dis[i][k]+dis[k][j]:
                    dis[i][j]=dis[i][k]+dis[k][j];
                    path[i][j]=path[k][j];

    outfile=open('result.csv','w')
    outfile.write('stationName,stationId,shortest,path\n');
    for i in range(1,len(station)+1):
        for j in range(1,len(station)+1):
            # print('{}->{},{}->{}'.format(i,j),end=' ')
            outfile.write('{}->{},{}->{},{},'.format(station[i],station[j],i,j,dis[i][j]));
            if dis[i][j]==MAX:
                outfile.write('\n')
                continue
            else:
                pathList = printPath(path, i, j);
                for k in range(len(pathList)):
                    # print('{}'.format(pathList[k]),end=' ')
                    outfile.write('->{}'.format(pathList[k]))
                # print(' ')
                outfile.write('\n')



    outfile.close()

def printPath(path,start,target):
    pathList=[];

    pathList.append(target)
    while target!=start:
        pathList.append(path[start][target]);
        target=path[start][target];
    pathList.reverse()
    return pathList

if __name__=='__main__':
    path1='1.csv'
    path2='2.csv'
    station,stationMap=readCsv(path1,path2);
    floyd(station,stationMap);


