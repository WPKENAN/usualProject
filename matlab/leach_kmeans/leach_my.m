num11=0;
num12=0;
flag=1;
while(flag)
for r=1:1:10
  figure(r);
    for i=1:1:n             %�������100����
    S(i).temp_rand=rand; 
    end
  for i=1:1:n 
      if  S(i).selected=='N'
    %if  S(i).type=='N' %ֻ����ͨ�ڵ����ѡ�٣����Ѿ���ѡ��ͷ�Ľڵ㲻������ѡ��
       if ( S(i).temp_rand<=(p/(1-p*mod(r,round(1/p)))))
           S(i).type='C';      %�ڵ�����Ϊ��ͷ
           S(i).selected='O';
           plot(S(i).xd,S(i).yd,'*');
           text(S(i).xd,S(i).yd,num2str(i));
           num11=num11+1;
       else    S(i).type='N';      %�ڵ�����Ϊ��ͨ 
                  plot(S(i).xd,S(i).yd,'o'); 
                  text(S(i).xd,S(i).yd,num2str(i));
                  num12=num12+1;
       end
      end
    if S(i).type=='C'
        plot(S(i).xd,S(i).yd,'*');     %��ͷ�ڵ���*���
        text(S(i).xd,S(i).yd,num2str(i));

    else
        plot(S(i).xd,S(i).yd,'o');      %��ͨ�ڵ���o���
        text(S(i).xd,S(i).yd,num2str(i));
    end
    hold on;

  end
%�ж�����Ĵ�ͷ��㣬���ȥ�жϣ����þ������
yy=zeros(n);
for a=1:1:n
    if S(a).type=='N'
        for b=1:1:n
          if S(b).type=='C'
          length(a,b)=sqrt((S(a).xd-S(b).xd)^2+(S(a).yd-S(b).yd)^2); %��ͷ��ÿ����ͨ�ڵ�ľ���
          else
          length(a,b)=10000;    
          end
        end
        [val,b]=min(length(a,:));
        plot([S(b).xd;S(a).xd],[S(b).yd;S(a).yd])  %���ڵ����ͷ���������������ͷ����
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