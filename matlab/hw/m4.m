clear
clc
Student_Number =[1,0,1,0,3,0,3,4,1];
M=[1,0,1;0,3,0;3,4,1]
b=[1;1;1]

%a  find the original vector x
x=inv(M)*b

%b Perform the following calculation
c=b'*M*b

%c report the value ''E=c/pi''.
E=c/pi