clear
clc
Student_Number =[1,0,1,0,3,0,3,4,1];

B=[1,-1,0,0,0,0;
    0,1,-1,0,0,0;
    0,0,1,-1,0,0;
    0,0,0,1,-1,0;
    0,0,0,0,1,-1;
    -1,0,0,0,0,1]
c=[75;-60;115;-120;55;-65]
B\c
rankB=rank(B)
rankBC=rank([B,c])
disp('We find the system is under-determined');

% Code this constraint into the system of equations, and solve for the vector of x values
disp('Code this constraint into the system of equations, and solve for the vector of x values')
B=[B;1,1,1,1,1,1]
c=[c;0]
x=B\c
% Check the solution by calculating
disp('Check the solution by calculating')
B*x-c