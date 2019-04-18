clear
clc
Student_Number =[1,0,1,0,3,0,3,4,1];

%M*x=c
M=[26.6,30.2;3100,6400]
c=[162;23610+10*Student_Number(9)]
x=inv(M)*c

% the amount of A and B burned
A=x(1)
B=x(2)

rankM=rank(M)
rankMC=rank([M,c])
disp('This system is determined')

%You are provided with additional data and measurements: 
M=[M;[240,340]]
c=[c;1566]
x=M\c
disp('This system is over-determined')


