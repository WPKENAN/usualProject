function Y1 = imagequilt_conditional_3D_v13(X, var_type, m, n, o, D, w, tilesize, overlap, nbreplicates, w_v, temp_split ,do_cut)
% Performs the Efros/Freeman Unconditional Image quilting algorithm on the
% input TI  var_type,w,w_v,temp_split

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
x_cord=D(:,1); % x coordinates of conditioning points
y_cord=D(:,2); % y coordinates of conditioning points
z_cord=D(:,3); % y coordinates of conditioning points
P = size (D,1); % Number of Conditioning points

if( overlap(1) >= tilesize(1) || overlap(2) >= tilesize(2) || overlap(3) >= tilesize(3))
    error('Overlap must be less than tilesize');
end;

destsize_x = m * tilesize(1) - (m-1) * overlap(1);
destsize_y = n * tilesize(2) - (n-1) * overlap(2);
destsize_z = o * tilesize(3) - (o-1) * overlap(3);
Y1 = zeros(destsize_x, destsize_y, destsize_z);   % Y = the size of output
% Y = zeros(destsize_x, destsize_y, destsize_z, Nvar);

%% Determining starting and ending points of each tile in both i, j direction
for kk=1:2*m-1
    if kk>m
        nn = 2*m-kk;
    else
        nn = kk;
    end
    for k = 1:o
        parfor pp = 1:nn
            qq = mod(pp-1,nn) + 1;
            if nn==kk
                i = qq;
            else
                i = kk+qq-m;
            end
            j = kk+1-i;
            pos = [i,j,k];
            [Y,start1,end1,start2,end2,start3,end3] = GPU_v13(i,j,k,Y1,X,tilesize,overlap,nbreplicates,pos,do_cut,x_cord,y_cord,z_cord,P,var_type,w);
            M=matfile(sprintf('output%d%d%d.mat',kk,pp,k),'writable',true);
            M.YY = Y;
            M.startI=start1;
            M.endI=end1;
            M.startJ=start2;
            M.endJ=end2;
            M.startK=start3;
            M.endK=end3;
        end   
        for pp2 = 1:nn
            path = sprintf('output%d%d%d.mat',kk,pp2,k);% i代表动态文件名
            load (path,'YY','startI','endI','startJ','endJ','startK','endK')
            Y1(startI:endI, startJ:endJ,startK:endK) = YY(startI:endI, startJ:endJ, startK:endK);
        end
    end
end

