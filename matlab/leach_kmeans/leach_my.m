num11=0;
num12=0;
flag=1;
while(flag)
for r=1:1:10
  figure(r);
    for i=1:1:n             %随机产生100个点
    S(i).temp_rand=rand; 
    end
  for i=1:1:n 
      if  S(i).selected=='N'
    %if  S(i).type=='N' %只对普通节点进行选举，即已经当选簇头的节点不进行再选举
       if ( S(i).temp_rand<=(p/(1-p*mod(r,round(1/p)))))
           S(i).type='C';      %节点类型为蔟头
           S(i).selected='O';
           plot(S(i).xd,S(i).yd,'*');
           text(S(i).xd,S(i).yd,num2str(i));
           num11=num11+1;
       else    S(i).type='N';      %节点类型为普通 
                  plot(S(i).xd,S(i).yd,'o'); 
                  text(S(i).xd,S(i).yd,num2str(i));
                  num12=num12+1;
       end
      end
    if S(i).type=='C'
        plot(S(i).xd,S(i).yd,'*');     %蔟头节点以*标记
        text(S(i).xd,S(i).yd,num2str(i));

    else
        plot(S(i).xd,S(i).yd,'o');      %普通节点以o标记
        text(S(i).xd,S(i).yd,num2str(i));
    end
    hold on;

  end
%判断最近的簇头结点，如何去判断，采用距离矩阵
yy=zeros(n);
for a=1:1:n
    if S(a).type=='N'
        for b=1:1:n
          if S(b).type=='C'
          length(a,b)=sqrt((S(a).xd-S(b).xd)^2+(S(a).yd-S(b).yd)^2); %簇头与每个普通节点的距离
          else
          length(a,b)=10000;    
          end
        end
        [val,b]=min(length(a,:));
        plot([S(b).xd;S(a).xd],[S(b).yd;S(a).yd])  %将节点与簇头连起来，即加入簇头集合
        yy(a,b)=1;
        hold on 
    else
     length(a,:)=10000;   
     end
end
for i=1:1:n 
if S(i).type=='C'
    number=sum(yy(:,i))
    S(i).power=S(i).power-(2+11*number);
    else
    S(i).power=S(i).power-22;
end
end

for i=1:1:n 
   S(i).type='N';
end
end
for i=1:1:n 
    if (S(i).power)<0
        text(S(i).xd,S(i).yd,num2str(i));   
        flag=0;
    end
    
end
if flag==0
    break
    end 
end