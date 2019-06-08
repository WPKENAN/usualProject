close all
clear all;
clc;
pm=100;                    %概率范围
xm=100;                    %x轴范围
ym=100;                    %y轴范围
line=10;            %连线距离初始值           
sink.x=0.5*xm;             %基站x轴 50
sink.y=0.5*ym;             %基站y轴 50
n=100; 
p=0.08;
for i=1:1:n/2             %随机产生100个点
    S(i).xd=rand(1,1)*xm;
    S(i).yd=rand(1,1)*ym;
    S(i).temp_rand=rand; 
    S(i).type='N';      %进行选举簇头前先将所有节点设为普通节点
    S(i).selected='N';
    S(i).power=300;
end
for i=n/2:1:n             %随机产生100个点
    S(i).xd=xm+rand(1,1)*xm;
    S(i).yd=ym+rand(1,1)*ym;
    S(i).temp_rand=rand; 
    S(i).type='N';      %进行选举簇头前先将所有节点设为普通节点
    S(i).selected='N';
    S(i).power=300;
end

X=zeros(n,2);
for i=1:n
    X(i,:)=[S(i).xd,S(i).yd];
end
figure;
plot(X(:,1),X(:,2),'o');
title 'Randomly Generated Data';

hold on
for i=1:n
    text(X(i,1),X(i,2),num2str(i));
end

