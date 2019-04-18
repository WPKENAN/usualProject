% Filename:VideoRead
clc;
clear;
filepath=mfilename('fullpath');
i=findstr(filepath,'\');
filepath=filepath(1:i(end));
obj = VideoReader(strcat(filepath,'T01.avi'));

disp('Totla frames:')
numFrames = obj.NumberOfFrames% ֡������
frame_num=5;%ʹ��֡��
 
 for k = 1 : min(frame_num,numFrames)% ��ȡ����
     frame = read(obj,k);
     %imshow(frame);%��ʾ֡
     imwrite(frame,strcat(filepath,num2str(k),'bmpfile.bmp'),'bmp');% ����֡
 end
 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 
 I=imread(strcat(filepath,'1bmpfile.bmp'));               % �����һ֡��Ϊ����֡
if length(size(I))==3
  I=rgb2gray(I);
end
fr_bw = I; 
[height,width] = size(fr_bw);           %��ÿ֡ͼ���С
fg = zeros(height, width);              %����ǰ���ͱ�������
bg_bw = zeros(height, width);


C = 3;                                  % ����˹ģ�͵ĸ���(ͨ��Ϊ3-5)
M = 3;                                  % ��������ģ�͸���
D = 2.5;                                % ƫ����ֵ
alpha = 0.01;                           % ѧϰ��
thresh = 0.25;                          % ǰ����ֵ
sd_init = 15;                            % ��ʼ����׼��
w = zeros(height,width,C);              % ��ʼ��Ȩ�ؾ���
mean = zeros(height,width,C);           % ���ؾ�ֵ
sd = zeros(height,width,C);             % ���ر�׼��
u_diff = zeros(height,width,C);         % ������ĳ����˹ģ�;�ֵ�ľ��Ծ���
p = alpha/(1/C);                        % ��ʼ��p�������������¾�ֵ�ͱ�׼��
rank = zeros(1,C);                      %������˹�ֲ������ȼ���w/sd)




pixel_depth = 8;                        % ÿ������8bit�ֱ���
pixel_range = 2^pixel_depth -1;         % ����ֵ��Χ[0,255]

for i=1:height
    for j=1:width
        for k=1:C
            mean(i,j,k) = rand*pixel_range;     %��ʼ����k����˹�ֲ��ľ�ֵ
            w(i,j,k) = 1/C;                     % ��ʼ����k����˹�ֲ���Ȩ��
            sd(i,j,k) = sd_init;                % ��ʼ����k����˹�ֲ��ı�׼��
            
        end
    end
end


for n = 1:frame_num
    frame=strcat(filepath,num2str(n),'bmpfile.bmp');
    I1=imread(frame);  % ���ζ����֡ͼ��
    if length(size(I1))==3
        I1=rgb2gray(I1);
    end
    fr_bw =I1;
    
    % �������������m����˹ģ�;�ֵ�ľ��Ծ���
    for m=1:C
        u_diff(:,:,m) = abs(double(fr_bw) - double(mean(:,:,m)));
    end
     
    % ���¸�˹ģ�͵Ĳ���
    for i=1:height
        for j=1:width
            
            match = 0;                                       %ƥ����;
            for k=1:C                       
                if (abs(u_diff(i,j,k)) <= D*sd(i,j,k))       % �������k����˹ģ��ƥ��
                    
                    match = 1;                               %��ƥ������Ϊ1
                    
                    % ����Ȩ�ء���ֵ����׼�p
                    w(i,j,k) = (1-alpha)*w(i,j,k) + alpha;
                    p = alpha/w(i,j,k);                  
                    mean(i,j,k) = (1-p)*mean(i,j,k) + p*double(fr_bw(i,j));
                    sd(i,j,k) =   sqrt((1-p)*(sd(i,j,k)^2) + p*((double(fr_bw(i,j)) - mean(i,j,k)))^2);
                else                                         % �������k����˹ģ�Ͳ�ƥ��
                    w(i,j,k) = (1-alpha)*w(i,j,k);           %��΢����Ȩ��
                    
                end
            end
            
                  
            bg_bw(i,j)=0;
            for k=1:C
                bg_bw(i,j) = bg_bw(i,j)+ mean(i,j,k)*w(i,j,k);
            end
            
            % ����ֵ����һ��˹ģ�Ͷ���ƥ�䣬�򴴽��µ�ģ��
            if (match == 0)
                [min_w, min_w_index] = min(w(i,j,:));      %Ѱ����СȨ��
                mean(i,j,min_w_index) = double(fr_bw(i,j));%��ʼ����ֵΪ��ǰ�۲����صľ�ֵ
                sd(i,j,min_w_index) = sd_init;             %��ʼ����׼��Ϊ6
                end

            rank = w(i,j,:)./sd(i,j,:);                    % ����ģ�����ȼ�
            rank_ind = [1:1:C];%���ȼ�����
           
            
            % ����ǰ��

            
            fg(i,j) = 0;
            while ((match == 0)&&(k<=M))

           
                    if (abs(u_diff(i,j,rank_ind(k))) <= D*sd(i,j,rank_ind(k)))% �������k����˹ģ��ƥ��
                        fg(i,j) = 0; %������Ϊ��������Ϊ��ɫ
           
                    else
                        fg(i,j) = 255;    %����Ϊǰ������Ϊ��ɫ 
                    end
                    
         
                k = k+1;
            end
        end
    end
    
    figure(1)
    subplot(1,3,1),imshow(fr_bw);               %��ʾ���һ֡ͼ��
    subplot(1,3,2),imshow(uint8(bg_bw))         %��ʾ����
    subplot(1,3,3),imshow(uint8(fg))            %��ʾǰ��
    FG= uint8(fg);
    imwrite(FG,'FG.bmp','bmp');
end



