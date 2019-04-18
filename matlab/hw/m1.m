clear
clc
Student_Number =[1,0,1,0,3,0,3,4,1];
f=Student_Number;
b=f(9:-1:1);

%a
disp('a)')
f*f'

%b
disp('b)')
f*b'

%c
disp('c)')
f*b'*f*f'

%d
disp('d)')
sum(f)

%e
disp('e)')
dot(f,b)

%f
disp('f)')
norm(f)

%g
disp('g)')
corr(f,b)
corr(f',b')

%h
disp('h)');
length(f)

%i
disp('i)')
mean(f)

%j
disp('j)')
cumsum(f)

%k
disp('f)')
size(f)

%l
disp('l)')
size(f,1)

%m
disp('m)')
size(f,2)

%n
disp('n)')
size(b)




