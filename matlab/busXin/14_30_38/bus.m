clc
clear
%初始化,车上人数
peopleOnBus=0;
peopleOnBus_maxNum=38;
stationNum=14;%站台数量
stationDis=3;%km
startTime=datenum(2019,04,04,06,00,00);
oneSeconds=datenum(2019,04,04,06,00,01)-datenum(2019,04,04,06,00,00);

getOff=zeros(stationNum,1);
getOn=zeros(stationNum,1);
people=zeros(stationNum,1);%15次关闭车门之后人数
speed=zeros(stationNum,1);
time=zeros(stationNum,1);;

for i=1:stationNum
    if i==1
        getOff(i)=0;
    elseif i==stationNum
        getOff(i)=peopleOnBus;
    else
        getOff(i)=getOffBus(0,peopleOnBus);
    end
    peopleOnBus=peopleOnBus-getOff(i);
    
    if i==stationNum  
        getOn(i)=0;
    else
        getOn(i)=getOnBus(0,peopleOnBus_maxNum-peopleOnBus);
    end
    peopleOnBus=peopleOnBus+getOn(i);
    people(i)=peopleOnBus;
    
    if i==1
        time(i)=0;
        speed(i)=30;
    else
        %time(i)=time(i-1)+getTime(5*60,10*60);%单位是秒
        %speed(i)=stationDis/(time(i)-time(i-1))*60*60;%单位km/h
        
        speed(i)=30;
        time(i)=stationDis/(speed(i)/60/60)+time(i-1);
    end
end

time;
timeStr=string(time);
for i =1:stationNum
    timeStr(i)=datestr(time(i)*oneSeconds+startTime,'HH:MM:SS');
end

figure
hold on
grid()
plot(getOn)
plot(getOff)
plot(people)
ylabel('人数')
xlabel('站台编号')
legend('getOn','getOff','peopleOnBus')

disp('[getOff,getOn,people,timeStr,speed]')
[getOff,getOn,people,timeStr,speed]


