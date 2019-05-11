import math
import re
import os
import copy

def calAngle(x1,y1,x2,y2):
    try:
        return math.acos((x1*x2+y1*y2)/math.sqrt(x1*x1+y1*y1)/math.sqrt(x2*x2+y2*y2))
    except:
        return 0
def calLength(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2+(y2-y1)**2)
def isConvex(graph):
    angle=0;
    for i in range(len(graph)):
        # print(calAngle(graph[(i+1)%len(graph)][0]-graph[i][0],graph[(i+1)%len(graph)][1]-graph[i][1],
        #                      graph[(i+2)%len(graph)][0]-graph[(i+1)%len(graph)][0],graph[(i+2)%len(graph)][1]-graph[(i+1)%len(graph)][1])/math.pi*180)
        angle=angle+calAngle(graph[(i+1)%len(graph)][0]-graph[i][0],graph[(i+1)%len(graph)][1]-graph[i][1],
                             graph[(i+2)%len(graph)][0]-graph[(i+1)%len(graph)][0],graph[(i+2)%len(graph)][1]-graph[(i+1)%len(graph)][1])
    if abs(angle-2*math.pi)<1e-5:
        return True
    else:
        return False

def available_coloured_pieces(file):
    file=file.read()
    graphs=re.findall("path d=\"(.+?)\"", file);

    for i in range(len(graphs)):
        graphs[i]=graphs[i].split(' ')
        graph=[]
        points=[]
        for j in range(len(graphs[i])):
            if  not graphs[i][j].isdigit():
                continue
            points.append(eval(graphs[i][j]));
            if len(points)==2:
                # if not (len(graph)!=0 and points==graph[-1]):
                graph.append(points)
                points=[]
        # while graph[-1]==graph[0]:
        #     graph=graph[:-1]
        graphs[i]=graph
    # print(graphs)
    return graphs

def are_valid(graphs):
    for graph in graphs:
        if not isConvex(graph):
            return False
    return True

def are_identical_sets_of_coloured_pieces(graphs1,graphs2):
    # print(graphs2[0])
    if len(graphs1)!=len(graphs2):
        return False

    isVis=set()
    for i in range(len(graphs1)):
        for j in range(len(graphs2)):
            if j not in isVis:
                if isEqual(copy.deepcopy(graphs1[i]),copy.deepcopy(graphs2[j])):
                    isVis.add(j);
                    continue
            # print(isEqual(copy.deepcopy(graphs1[i]),copy.deepcopy(graphs2[j])))
            # print(graphs1[i])
            # print(graphs2[j])
            # print("**********************")

    if len(isVis)==len(graphs1):
        return True
    # print(len(isVis))
    return False

def isEqual(graph1,graph2):
    length_angle1=[]
    length_angle2=[]
    for i in range(len(graph1)):
        angle=calAngle(graph1[(i+1)%len(graph1)][0]-graph1[i][0],graph1[(i+1)%len(graph1)][1]-graph1[i][1],
                             graph1[(i+2)%len(graph1)][0]-graph1[(i+1)%len(graph1)][0],graph1[(i+2)%len(graph1)][1]-graph1[(i+1)%len(graph1)][1])
        length_=calLength(graph1[i][0],graph1[i][1],graph1[(i+1)%len(graph1)][0],graph1[(i+1)%len(graph1)][1]);
        length_angle1.append([length_,angle])

    for i in range(len(graph2)):
        angle=calAngle(graph2[(i+1)%len(graph2)][0]-graph2[i][0],graph2[(i+1)%len(graph2)][1]-graph2[i][1],
                             graph2[(i+2)%len(graph2)][0]-graph2[(i+1)%len(graph2)][0],graph2[(i+2)%len(graph2)][1]-graph2[(i+1)%len(graph2)][1])
        length_=calLength(graph2[i][0],graph2[i][1],graph2[(i+1)%len(graph2)][0],graph2[(i+1)%len(graph2)][1]);
        length_angle2.append([length_,angle])

    # print(length_angle1)
    # print(length_angle2)
    for i in range(len(length_angle1)):
        tmp=[]
        for j in range(len(length_angle1)):
            tmp.append(length_angle1[(i+j)%len(length_angle1)])
        if tmp==length_angle2:
            return True

    length_angle3=copy.deepcopy(length_angle2)
    for i in range(len(length_angle2)):
        length_angle3[i][0]=length_angle2[(i+1)%len(length_angle2)][0]


    for i in range(len(length_angle1)):
        tmp=[]
        for j in range(len(length_angle1)):
            tmp.append(length_angle1[(i+j)%len(length_angle1)])
        if tmp==length_angle3:
            return True

    return False


if __name__=="__main__":
    folder="C:\\Users\Anzhi\Documents\Tencent Files\\3272346474\\FileRecv\Assignment_2"
    file="pieces_A.xml"
    file1="shape_A_1.xml"
    content=open(folder+"\\"+file)
    coloured_pieces=available_coloured_pieces(content)
    content.close()
    content1 = open(folder + "\\" + file1)
    coloured_pieces1 = available_coloured_pieces(content1)
    content1.close()
    print(are_valid(coloured_pieces))
    print(are_identical_sets_of_coloured_pieces(coloured_pieces,coloured_pieces1))

