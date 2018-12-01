function [sampledResult]= RayBurstSampling(imgDist,somaX,somaY,somaZ,vertexunit)
% improved ray burst sampling algorithm based on distance transform
% inputs: 
%   imgDist- distance map 
%   vertexunit- samping core 
%   soma centroid coordinate- somaX, somaY, somaZ
% outputs:
%   samplingResult- all points sampled by ray burst sampling algorithm for soma centroid [somaX,somaY,somaZ] 
%   raysDist- save distance value of sampled points 

%% initialization
[rayNum,dimension]=size(vertexunit);
sampledResult=zeros(rayNum,3);
% save the distance value for sampled rays
raysDist=cell(rayNum,1);

if(dimension~=3||numel(size(imgDist))~=3)
        disp('Wrong dimension.');
        return
end

% check the candidate soma centroid is in foreground or not
isFg=CheckFg(somaX,somaY,somaZ,imgDist);
if(~isFg)
    disp('Wrong origin.')
    return
end

% sampledRays save every sampled points of one ray in all directions
% sampledRays :[1,:] save all sampled points (outer boundary),[2,:] save inner sampled points ID in array sampleRays[1,:] (inner boundary)
sampledRays=cell(rayNum,2);
raysdt=zeros(rayNum,1000);
innerBoundary=1;

%% soma surface sampling 
for directionID=1:rayNum
    %   [(x,y,z)*Ni   v*Ni]
    %disp(num2str(i));
    [sampledRays{directionID,1},sampledRays{directionID,2}]=SingleSampling(somaX,somaY,somaZ,vertexunit(directionID,:),imgDist,directionID);
    raysDist{directionID}=sampledRays{directionID,2};
    temp=sampledRays{directionID,2}(end);
    if(innerBoundary<temp)
        innerBoundary=temp;
    end
    %singleRayDist=[];
% end for
end

%%  process the touching somata and single somata by boundary 

% just save all points and use outer sampled boundary for ellipsoid fitting 
for rayID=1:rayNum
    sampledResult(rayID,:)=sampledRays{rayID,1}(end,:);
end

%end function 
end

%% other functions called by main function 
% SingleSampling- Sampling for one direction from soma centroid   
% CheckForeground- check soma centroid is in foreground or not 
% CheckImgBoundary- check soma centroid is in image range or not 
function [sampledCoord ,sampledDistValue] = SingleSampling(x0,y0,z0,rayDirection,imgDist,rayID)
%    
%     [xyz,v]=
%     (x,y,z)*Ni   v*Ni
    % initialization 
    rays=zeros(1,1000);
    sampledID=1;
    xDirection=rayDirection(1);
    yDirection=rayDirection(2);
    zDirection=rayDirection(3);
    
    intialDist=imgDist(ceil(x0),ceil(y0),ceil(z0));
    %singleRaysDist(1,1)=intialDist;
    resetNum=1;
    rayLength=0;
    % flag for distance increase 
    distIncFlag=0;
 
    sampledDistValue=[];
    sampledCoord=[];
    iterationID=1;
    sampledDistValue(iterationID)=intialDist;
    sampledCoord(iterationID,1:3)=[x0,y0,z0];

    %% soma surface sampling iteratively
    while true
        % compute the coord for next sampled point
        % start from soma centroid [x0,y0,z0]
        % generate [i j k] to correct 
        if(xDirection<0)
            j=ceil(x0-1);
        else 
            j=floor(x0+1);
        end
        if(yDirection<0)
            i=ceil(y0-1);
        else 
            i=floor(y0+1);
        end
        if(zDirection<0)
            k=ceil(z0-1);
        else 
            k=floor(z0+1);
        end
        
        % compute the step 
        tx=(j-x0)/xDirection;
        ty=(i-y0)/yDirection;
        tz=(k-z0)/zDirection;
        t=min(abs([tx,ty,tz]));
        
        % generate the final coordinate for one step 
        %  
        xCurrent=x0+xDirection*t;
        yCurrent=y0+yDirection*t;
        zCurrent=z0+zDirection*t;
        
       %% boundary judgement
       % 1 check the current sampled point is beyond the image boundary or not  
       % exitFlag- flag for exiting the sampling proceedure or not  
        isFg = CheckFg(xCurrent,yCurrent,zCurrent,imgDist);
        if(~isFg>0)
            % current sampled point lie in background, exit the sampled proceedure
            exitFlag=1;
            break;
        else
            % current sampled point could lie in foreground, continue the samples proceedure 
            % currentDist- distance value for current sampled point 
            currentDist=imgDist(ceil(xCurrent),ceil(yCurrent),ceil(zCurrent));
            if(currentDist==0)
                exitFlag=1;
            else
                if(currentDist>intialDist)
                    exitFlag=1;
                else
                    exitFlag=0;
                    rayLength=rayLength+1;
                end
            end
        end
        % save the result and refresh flags
        if(exitFlag==0)
            % iteration continues
            % save results
            iterationID=iterationID+1;
            sampledCoord(iterationID,1:3)=[xCurrent,yCurrent,zCurrent];
            %  sampledDistValue(iterationID)=currentDist;
            %  refresh the initial point
            x0=xCurrent;
            y0=yCurrent;
            z0=zCurrent;
            if(currentDist<=intialDist)
                sampledID=sampledID+1;
                %rays(1,iterationID)=currentDist;
                intialDist=currentDist;
            end
            if distIncFlag==1;
                distIncFlag=0;
            end
        else
            % distance increasing
            % jump the one pixel witdth gap 
            if rayLength >0 && rayLength<imgDist(ceil(x0),ceil(y0),ceil(z0))                                   
                % sampling once more 
                if resetNum==1
                    intialDist=currentDist;
                    distIncFlag=1;
                    tmpCoord=sampledCoord;
                end
                if resetNum==0 && distIncFlag==1;
                    resetNum=1;
                    distIncFlag=0;
                    sampledCoord=tmpCoord;
                    break;    
                end 
            else
                break;
            end  
%         break;
        end
       %% not used this process
        % one more sampling
        if distIncFlag==1
            resetNum=resetNum-1;
        else
            resetNum=1;
        end
    end
end

% check the candidate soma centroid is in foreground or not
function isFg = CheckFg(x,y,z,imgDist)
isBeyond = CheckImgBorder(x,y,z,imgDist);
if isBeyond>0
    % this point is not in image 
    isFg=0;
    return
else
    % check the distance value is zero or not 
    value=imgDist(ceil(x),ceil(y),ceil(z));
    if(value)
        % dist(x,y,z) is positive so that it could be foreground 
        isFg=1;
    else
        isFg=0;
        return
    end
%endif 
end

end

% check the candidate soma centroid is beyond the image boudary or not 
function isBeyond = CheckImgBorder(x,y,z,imgDist)
% check the soma centroid is beyond image boundaries
    isBeyond=sum([[x,y,z]>size(imgDist),[x,y,z]<=[0,0,0]]);
end