clc
clear
userpath('D:\github\usualProject\matlab\busXin')
%初始化,车上人数
peopleOnBus=0;
peopleOnBus_maxNum=40;
stationNum=15;%站台数量
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
        speed(i)=45;
    else
        %time(i)=time(i-1)+getTime(5*60,10*60);%单位是秒
        %speed(i)=stationDis/(time(i)-time(i-1))*60*60;%单位km/h
        
        speed(i)=45;
        time(i)=stationDis/(speed(i)/60/60)+time(i-1);
    end
end

time;
timeStr=string(time);
for i =1:stationNum
    timeStr(i)=datestr(time(i)*oneSeconds+startTime,'HH:MM:SS');
end


%初始化,车上人数
peopleOnBus=round(people(end-1)*0.6+rand*40);
H1=peopleOnBus;
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



%初始化,车上人数
peopleOnBus=round(people(end-1)*0.6+rand*40);
H2=peopleOnBus;
peopleOnBus_maxNum=40;
stationNum=29;%站台数量
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
        speed(i)=80;
    else
        %time(i)=time(i-1)+getTime(5*60,10*60);%单位是秒
        %speed(i)=stationDis/(time(i)-time(i-1))*60*60;%单位km/h
        
        speed(i)=80;
        time(i)=stationDis/(speed(i)/60/60)+time(i-1);
    end
end

time;
timeStr=string(time);
for i =1:stationNum
    timeStr(i)=datestr(time(i)*oneSeconds+startTime,'HH:MM:SS');
end



T=25
figure
title('First transfer')
if H1<T
    plot([0,2],[H1,H1],'g','LineWidth',30)
else
    plot([0,2],[H1,H1],'r','LineWidth',30)
end
figure
title('Second transfer')
if H2<T
    plot([0,2],[H2,H2],'g','LineWidth',30)
else
    plot([0,2],[H2,H2],'r','LineWidth',30)
end





