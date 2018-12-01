function [somaLocations,somaSegmentResultImg] = SomaSegment( candidateSomaLocations,samplingRays, imgDist,imgSize, resultFilteringThreshold)
% this function segment the somata 
% two main step is :
% (1) soma boundary detect through raybursting sampling algorithm 
% (2) ellipsoid fitting method to generate the segmentation result  
% inputs:
% samplingrays is number of sampling rays
% imgDist is distance map of original image stacks

% Rp-size of image patch 
Rp=50;
[imgDist,~]=ImageBorderFill(imgDist,imgSize,Rp);
[candidateSomaLocations,imgSize]=ImageBorderFill(candidateSomaLocations,imgSize,Rp);

% initialization the parameters 
candidateSomaNum=numel(candidateSomaLocations);
somaSegmentResults=cell(candidateSomaNum,1);

%load sampling kernel
load('vertexunit3d_18_66_258.mat')
if samplingRays==18
    vertexunit=vertexunit3d_18;
elseif samplingRays==66
    vertexunit=vertexunit3d_66;
elseif samplingRays==258
    vertexunit=vertexunit3d_258;
else
    disp('the number sampling rays is not set correctly!')
end

% variables that save results 
somaLocations=[];
somaSegmentResultImg=logical(zeros(imgSize(1,1),imgSize(1,2),imgSize(1,3)));

somaCounts=0;
somaId=0;

somaBoundary=zeros(samplingRays,30);% allow one ray samples 30 steps at most.Generally, soma radius is less than 20 pixels

for i=1:candidateSomaNum
    if candidateSomaLocations(i)==1 %find soma locations  
        [somaX,somaY,somaZ]=ind2sub(imgSize,i);
        % soma surface sampling
        [samplingResult]=RayBurstSampling(imgDist,somaX,somaY,somaZ,vertexunit);
        somaCounts=somaCounts+1;
        % ellipsoid fitting method for one soma 
        somaSegmentResults{somaCounts}=NSEDFEllipsoid(samplingResult(:,1),samplingResult(:,2),samplingResult(:,3));
        aa=somaSegmentResults{somaCounts};
        [yy,xx,zz]=meshgrid(somaY-Rp:somaY+Rp,somaX-Rp:somaX+Rp,somaZ-Rp:somaZ+Rp);
        nhood=aa(1)*(aa(1)*xx.^2 + aa(2)*yy.^2 + aa(3)*zz.^2 ...
             + aa(4)*xx.*yy + aa(5)*xx.*zz + aa(6)*yy.*zz ...
             + aa(7)*xx + aa(8)*yy + aa(9)*zz + aa(10)*ones(2*Rp+1,2*Rp+1,2*Rp+1))<=0;
        nhoodSize=length(find(nhood)>0);
        if nhoodSize>resultFilteringThreshold
            somaId=somaId+1;
            somaSegmentResultImg(somaX-Rp:somaX+Rp,somaY-Rp:somaY+Rp,somaZ-Rp:somaZ+Rp)=somaSegmentResultImg(somaX-Rp:somaX+Rp,somaY-Rp:somaY+Rp,somaZ-Rp:somaZ+Rp)+nhood; 
            somaLocations(somaId,:)=[somaX,somaY,somaZ]-Rp;
        end
        candidateSomaLocations(somaX-Rp:somaX+Rp,somaY-Rp:somaY+Rp,somaZ-Rp:somaZ+Rp)=candidateSomaLocations(somaX-Rp:somaX+Rp,somaY-Rp:somaY+Rp,somaZ-Rp:somaZ+Rp).*~nhood;
    end                
end
somaSegmentResultImg=somaSegmentResultImg(1+Rp:imgSize(1,1)-Rp,1+Rp:imgSize(1,2)-Rp,1+Rp:imgSize(1,3)-Rp);
end

