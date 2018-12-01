function [ somaLocation ] = ReadSwc( filename )
% read swc files
somaLocation=load(filename);
somaLocation=somaLocation(:,3:5);
tmp=somaLocation(:,2);
somaLocation(:,2)=somaLocation(:,1);
somaLocation(:,1)=tmp;
end

