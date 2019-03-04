function Y1 = imagequilt_Unconditional_3D_v13(X, m, n, o, tilesize, overlap, nbreplicates, do_cut)
% Performs the Efros/Freeman Unconditional Image quilting algorithm on the input TI

% Inputs
% X:  The source image to be used in synthesis
% Tilesize: The dimensions of each square tile
% m:  The number of tiles to be placed in the output image, in X dimension
% n:  The number of tiles to be placed in the output image, in Y dimension
% D: Conditioning values
% w: Weightage of conditioning
% overlap: The amount of overlap to allow between pixels (def: 1/6 tilesize)
% nbreplicates: Number of replicas considered to find the best possible patch
% w_v: Weightage of different variables

%%
X = double(X);  % convert X to double precision X
% Nvar = size(X,3);
% Nlayer = size(X,4);

if( overlap(1) >= tilesize(1) || overlap(2) >= tilesize(2) || overlap(3) >= tilesize(3))
    error('Overlap must be less than tilesize');
end;

destsize_x = m * tilesize(1) - (m-1) * overlap(1);
destsize_y = n * tilesize(2) - (n-1) * overlap(2);
destsize_z = o * tilesize(3) - (o-1) * overlap(3);
Y1 = zeros(destsize_x, destsize_y, destsize_z);   % Y = the size of output
% Y = zeros(destsize_x, destsize_y, destsize_z, Nvar);
if m<n
    aM=n;
else
    aM=m;
end
%% Determining starting and ending points of each tile in both i, j direction
for kk=1:2*aM-1
    if kk>aM
        nn = 2*aM-kk;
    else
        nn = kk;
    end
    for k = 1:o
        for pp = 1:nn
            if nn==kk
                i = pp;
            else
                i = kk+pp-aM;
            end
            j = kk+1-i;
            if i>m||j>n
                continue
            else
        %         k = floor((pp-1)/nn) + 1;
                pos = [i,j,k];
                [Y,start1,end1,start2,end2,start3,end3] = GPU_v13(i,j,k,Y1,X,tilesize,overlap,nbreplicates,pos,do_cut);
                M=matfile(sprintf('output%d_%d_%d.mat',kk,pp,k),'writable',true);
                M.YY = Y;
                M.startI=start1;
                M.endI=end1;
                M.startJ=start2;
                M.endJ=end2;
                M.startK=start3;
                M.endK=end3;
            end
        end
        for pp2 = 1:nn
            path = sprintf('output%d_%d_%d.mat',kk,pp2,k);% i代表动态文件名
            if ~exist(path,'file')==0
                load (path,'YY','startI','endI','startJ','endJ','startK','endK')
                Y1(startI:endI, startJ:endJ,startK:endK) = YY(startI:endI, startJ:endJ, startK:endK);
            end
        end
    end
end
save result Y1;


