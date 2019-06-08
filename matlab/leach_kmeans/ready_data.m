close all
clear all;
clc;
pm=100;                    %���ʷ�Χ
xm=100;                    %x�᷶Χ
ym=100;                    %y�᷶Χ
line=10;            %���߾����ʼֵ           
sink.x=0.5*xm;             %��վx�� 50
sink.y=0.5*ym;             %��վy�� 50
n=100; 
p=0.08;
for i=1:1:n/2             %�������100����
    S(i).xd=rand(1,1)*xm;
    S(i).yd=rand(1,1)*ym;
    S(i).temp_rand=rand; 
    S(i).type='N';      %����ѡ�ٴ�ͷǰ�Ƚ����нڵ���Ϊ��ͨ�ڵ�
    S(i).selected='N';
    S(i).power=300;
end
for i=n/2:1:n             %�������100����
    S(i).xd=xm+rand(1,1)*xm;
    S(i).yd=ym+rand(1,1)*ym;
    S(i).temp_rand=rand; 
    S(i).type='N';      %����ѡ�ٴ�ͷǰ�Ƚ����нڵ���Ϊ��ͨ�ڵ�
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

