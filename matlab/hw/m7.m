clear
clc
Student_Number =[1,0,1,0,3,0,3,4,1];

R1=6;
R2=5;
R3=1;
R4=8;
V1=5.41;
V2=3.41;

%B*x=c
B=[R1+R2,-R1,-R2,0;
    -R1,R1+R3,-R3,0;
    -R2,-R3,R2+R3,R4;]
c=[-V1;
    -V2;
    0]
x=B\c
rankB=rank(B)
rankBC=rank([B,c])
disp('This system is under-determined')