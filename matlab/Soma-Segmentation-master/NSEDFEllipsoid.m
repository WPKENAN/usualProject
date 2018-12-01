function alpha = NSEDFEllipsoid(X,Y,Z)
% fitellip gives the 10 parameter vector of the algebraic ellipsoid fit
% to a(1)x^2 + a(2)y^2 + a(3)z^2 + a(4)xy + a(5)xz + a(6)yz + a(7)x + a(8)y + a(9)z + a(10) = 0
% X & Y & Z are lists of point coordinates and must be column vectors.

   mx = min(X);
   my = min(Y);
   mz = min(Z);

   %scaling factors
   sx = (max(X)-min(X))/2;
   sy = (max(Y)-min(Y))/2;
   sz = (max(Z)-min(Z))/2;
   x = (X-mx)/sx;
   y = (Y-my)/sy;
   z = (Z-mz)/sz;

   % Build design matrix
   D1 = [ x.*x  y.*y  z.*z  x.*y  x.*z  y.*z];
   D2 = [ x  y  z  ones(size(x)) ];

   % Build 6x6 constraint matrix
   C(6,6) = -1; 
   C(1,2) = 1; C(1,3) = 1; C(2,1) = 1; C(2,3) = 1; C(3,1) = 1; C(3,2) = 1;
   C(1,1) = -1;C(2,2) = -1;C(3,3) = -1;C(4,4) = -1; C(5,5) = -1;
   
   % Build scatter matrix
   S1 = D1'*D1;
   S2 = D1'*D2;
   S3 = D2'*D2;
   T = -inv(S3)*S2';
   M = (S1+S2*T);
   M = inv(C)*M;

   % Solve eigensystem
   [evec, eval] = eig(M);

   % Find eigenvector corresponding to aCa>0(equalling to diag(ACA)>0)
   a1 = evec(repmat(diag(evec'*C*evec)'>0,length(C),1)>0);
   
   a = [a1;T*a1];
   
   %unnormalize
   alpha = [
       a(1)/(sx*sx),...
       a(2)/(sy*sy),...
       a(3)/(sz*sz),...
       a(4)/(sx*sy),...
       a(5)/(sx*sz),...
       a(6)/(sy*sz),...
       -2*mx*a(1)/(sx*sx)-my*a(4)/(sx*sy)-mz*a(5)/(sx*sz)+a(7)/sx,...
       -2*my*a(2)/(sy*sy)-mx*a(4)/(sx*sy)-mz*a(6)/(sy*sz)+a(8)/sy,...
       -2*mz*a(3)/(sz*sz)-mx*a(5)/(sx*sz)-my*a(6)/(sy*sz)+a(9)/sz,...
       mx*mx*a(1)/(sx*sx) + my*my*a(2)/(sy*sy) + mz*mz*a(3)/(sz*sz) + mx*my*a(4)/(sx*sy) + mx*mz*a(5)/(sx*sz) + my*mz*a(6)/(sy*sz) - mx*a(7)/sx - my*a(8)/sy - mz*a(9)/sz + a(10)
       ]';
%    f=sum(([D1,D2]*a).^2)

end