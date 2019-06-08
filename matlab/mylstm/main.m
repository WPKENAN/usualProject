clc
clear
path='C:\Users\Anzhi\Desktop\data.xlsx'
exceldata=xlsread(path);
exceldata=exceldata(:,2:15);
noNan=exceldata(1:95,:)-min(exceldata(1:95,:)')'+0.001;%前95行数据是完整的
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%train%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%对每一行进行归一化，算出每一年的相对的分，有利于后面的预测
normalization=noNan./sum(noNan')';
%figure
%subplot(121)
%plot(noNan(:,1))
%subplot(122)
%plot(normalization(:,1)));
%data=[noNan(:,5)]';
%data=reshape(normalization',1,95*14);
cba=['A','B','C','D','E','F','G','H','I','J','K','L','M','N'];
nets=struct();
pre=zeros(7,14);
for i=1:14
    data = [normalization(:,i)]';
    [nets.(cba(i)),x]=train(data,cba(i),7);
    pre(:,i)=x;
end
analyzeNetwork(nets.(cba(1)));
%Update
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%sort%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
disp('1-14(A-T)球队预测得分')
pre(7,:)
[B,I]=sort(pre(7,:),'descend');
disp('得分排名，从第一名到第14名')
B
disp('球队排名,输出编号，从第一名到第14名编号如下')
I