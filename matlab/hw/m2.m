clear
clc
Student_Number =[1,0,1,0,3,0,3,4,1];
f=Student_Number';
b=f(9:-1:1);
U=[f,b]
x=(1:9)
plot(x,U)
title('Gang Han-101030341')
disp(strcat('image saved as',pwd,'\m2.png'));
saveas(gcf,'m2.png')

%a
disp('a)')
U*U'

%b
disp('b)')
U'*U

%c
disp('c)')
U.^2
