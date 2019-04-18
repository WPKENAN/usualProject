import numpy as np
from datetime import datetime
import math
import matplotlib.pyplot as plt
from folium import plugins
import folium
import webbrowser

def dealData():
    path = "D:\github\Data\\AA00212.csv";
    lines=readCsv(path)
    lng_lat_time=output_lng_lat_time(lines);
    speed=np.array(calculateSpeed(lng_lat_time))
    region=[0,60,80,100,120,180];
    counts=countSpeed(speed,region);
    print(region)
    print(counts)

    fig = plt.figure()
    ax1=fig.add_subplot(111)
    ax1.plot(region,counts,color='g')
    ax1.scatter(region,counts,color='r')
    ax1.grid()
    ax1.set_xlabel("km/h")
    ax1.set_ylabel("counts")
    ax1.set_title("Speed interval chart")

    ax2=ax1.twinx();
    ax2.plot(region,[x/len(speed) for x in counts],color='b')
    ax2.set_ylabel("%")
    # plt.show()

    maxSpeed=input("请输入允许的最大速度(km/h):");
    new_lng_lat_time=[];
    new_lines=[]
    for i in range(len(speed)):
        if speed[i]<=float(maxSpeed) and speed[i]>0:
            new_lng_lat_time.append(lng_lat_time[i])
            new_lines.append(lines[i]);

    print("速度<={} 有{}条数据".format(maxSpeed,len(new_lng_lat_time)))
    writeCsv(new_lines,path+"\\..\\new_lines.csv");
    writeCsv(new_lng_lat_time, path + "\\..\\new_lng_lat_time.csv");
    print("保存新的数据到csv");

    return new_lng_lat_time;
    # print(len(speed))
    # print(sum(speed > 1000))
    # plt.plot(speed)
    # plt.show()
    # print(sum(speed>1000))

def drawMap(new_lng_lat_time):
    gui_ji = []
    for item in new_lng_lat_time:
        gui_ji.append([item[1],item[0]])

    m = folium.Map(gui_ji[0], zoom_start=18)
    start_i=0;
    end_i=0;
    count=0;
    color=['red','blue','green']
    for i in range(1,len(gui_ji)):
        end_i = i - 1;
        if cal_dis2(gui_ji[i-1][1],gui_ji[i-1][0],gui_ji[i][1],gui_ji[i][0])>100:
            folium.Marker(gui_ji[start_i], popup='<i>{}号起始点</i>'.format(count),icon=folium.Icon(color='red', icon='info-sign')).add_to(m)
            folium.Marker(gui_ji[end_i], popup='<i>{}号终止点</i>'.format(count),icon=folium.Icon(color='blue', icon='info-sign')).add_to(m)
            route = folium.PolyLine(
                gui_ji[start_i:end_i+1],
                weight=1,
                color=color[count%len(color)],
                opacity=1
            ).add_to(m)
            aircraft = {'font-weight': 'bold', 'font-size': '10'}
            plugins.PolyLineTextPath(
                route,
                '\u2708',
                repeat=True,
                offset=1,
                attributes=aircraft
            ).add_to(m)
            start_i=i;
            count = count + 1;

    m.save("444444.html")
    webbrowser.open("444444.html")

def writeCsv(lines,path):
    outFile=open(path,'w')
    for line in lines:
        for i in range(len(line)-1):
            outFile.write("{},".format(line[i]));
        outFile.write("{}\n".format(line[-1]));

def readCsv(path):
    lines = open(path).readlines();
    lines=lines[1:len(lines)];
    return lines;

def output_lng_lat_time(lines):
    lng_lat_time = [];
    for i in range(len(lines)):
        lines[i]=lines[i].strip('\n').split(',');
        #lng-3,lat-4,time-10

        lines[i][3]=float(lines[i][3]);
        lines[i][4]=float(lines[i][4]);

        method=2;
        if method==1:

            if i == 0:
                lng_lat_time.append([lines[i][3], lines[i][4], strToDatetime(lines[i][10])]);
                # print(lng_lat_time[-1])
                continue
            if [lines[i][3], lines[i][4]]!=lng_lat_time[-1][0:2]:
                lng_lat_time.append([lines[i][3], lines[i][4], strToDatetime(lines[i][10])]);
                continue
            lng_lat_time.append(lng_lat_time[-1])
        if method==2:
            lng_lat_time.append([lines[i][3], lines[i][4], strToDatetime(lines[i][10])]);

        # print(lng_lat_time[-1])



    # print(lng_lat_time[0])
    # print(lng_lat_time[-1])
    return lng_lat_time

def countSpeed(speed,region):
    counts=[]
    for i in region:
        counts.append(sum(speed<=i))
    return  counts


def strToDatetime(timeStr):
    timeStr=timeStr.strip('\n').split(' ');
    timeStr[0]=timeStr[0].split('-');
    timeStr[1]=timeStr[1].split(':');

    year=int(timeStr[0][0]);
    month=int(timeStr[0][1]);
    day=int(timeStr[0][2]);

    hour=int(timeStr[1][0]);
    minute=int(timeStr[1][1]);
    second=int(timeStr[1][2]);

    # print([year,month,day,hour,minute,second])
    return datetime(year,month,day,hour,minute,second)



def cal_dis1(lon1,lat1,lon2,lat2):
    lat1 = (math.pi/180.0)*lat1
    lat2 = (math.pi/180.0)*lat2
    lon1 = (math.pi/180.0)*lon1
    lon2= (math.pi/180.0)*lon2
    #因此AB两点的球面距离为:{arccos[sina*sinx+cosb*cosx*cos(b-y)]}*R  (a,b,x,y)
    #地球半径
    R = 6378.1
    temp=math.sin(lat1)*math.sin(lat2)+\
         math.cos(lat1)*math.cos(lat2)*math.cos(lon2-lon1)
    if temp>1.0:
         temp = 1.0
    d = math.acos(temp)*R
    return d

def cal_dis2(lon1,lat1,lon2,lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r

def calcTime(time1,time2):
    return abs((time2-time1).total_seconds()/60/60);


def calculateSpeed(lng_lat_time):
    speed=[0];
    for i in range(1,len(lng_lat_time)):
        # print(i)
        if cal_dis2(lng_lat_time[i-1][0],lng_lat_time[i-1][1],lng_lat_time[i][0],lng_lat_time[i][1])==0:
            speed.append(0);
        else:
            speed.append(cal_dis2(lng_lat_time[i-1][0],lng_lat_time[i-1][1],lng_lat_time[i][0],lng_lat_time[i][1])/calcTime(lng_lat_time[i-1][2],lng_lat_time[i][2]));
        # print(speed[i])

        # print([cal_dis1(lng_lat_time[i - 1][0], lng_lat_time[i - 1][1], lng_lat_time[i][0], lng_lat_time[i][1]),
        #       cal_dis2(lng_lat_time[i-1][0],lng_lat_time[i-1][1],lng_lat_time[i][0],lng_lat_time[i][1])])

    return  speed;

if __name__=="__main__":
    new_lng_lat_time=dealData();
    drawMap(new_lng_lat_time);