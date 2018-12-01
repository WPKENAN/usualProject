%% Touching somata segmentation based on the raybursting sampling algorithm

clc;
clear;
%% diary file to saving the runtime
diary(strcat('Logs\log',date,'.txt'))
diary on
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%set the parent directory for results
segmentResultsPath='SegmentResults';
if exist('SegmentResults','dir')~=7
    mkdir('SegmentResults');
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% parameter settings
imgName='43';% name of file 
datasetPath='Data\';
imgPath=strcat(datasetPath,imgName,'.tif');
mkdir(segmentResultsPath,imgName);
imgResultPath=strcat(imgName,'\',datasetPath); 
%parameters for image preprocessing
sigma=[3,4]; 
volSegmentThreshold=200;
%parameters for soma localization
jitterHeight=1; 
%parameters for soma segmentation
samplingRays=258; 
resultFilteringThreshold=4200; 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% initialize the algorithm 
img=ImageLoad(imgPath);
tic;
imgSize=size(img);
toc; 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% preprocessing image for foreground extraction
tic;
[imgBin]=ImageBin(img,sigma,volSegmentThreshold);
toc;
% save the binaryzation result
imgBinPath=strcat(segmentResultsPath,'\',imgName,'\',imgName,'Bin.tif');
ImageSave(imgBin,imgBinPath);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% soma localization
tic;
[imgDist,candidateSomaLocations]=SomaLocate(imgBin,jitterHeight);
disp('localizationRuntime:')
toc;

% save the results
imgDistPath=strcat(segmentResultsPath,'\',imgName,'\',imgName,'Dist.tif');
imgCandSomaLocPath=strcat(segmentResultsPath,'\',imgName,'\',imgName,'CandSomaLoc.tif');
ImageSave(uint8(imgDist),imgDistPath);
ImageSave(uint8(candidateSomaLocations),imgCandSomaLocPath);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% soma segmentation 
% detecting soma boundary by improved raybursting sampling algorithm 
disp('segmentRuntime:')
tic;
[somaLocations,somaSegmentResult]=SomaSegment(candidateSomaLocations,samplingRays,imgDist,imgSize,resultFilteringThreshold);
toc;
% save the result
somaSegmentPath=strcat(segmentResultsPath,'\',imgName,'\',imgName,'j',num2str(jitterHeight),'r',num2str(samplingRays),'Th',num2str(resultFilteringThreshold),'Seg.tif');
ImageSave(uint8(somaSegmentResult),somaSegmentPath);
somaLocationPath=strcat(segmentResultsPath,'\',imgName,'\',imgName,'j',num2str(jitterHeight),'r',num2str(samplingRays),'Th',num2str(resultFilteringThreshold),'Loc.swc');
WriteSwc(somaLocations,somaLocationPath);
%%
diary off;

