clear
clc
Student_Number =[1,0,1,0,3,0,3,4,1];

startPoint=[0,0];
xyShift=[4,10;-8,1;5,-19;-13,7;1,Student_Number(9)]
xyPoint=zeros(length(xyShift)+1,2);

for i=1:length(xyShift)
    xyPoint(i+1,:)=xyPoint(i,:)+xyShift(i,:);
end
xyPoint

%a plot image
plot(xyPoint(:,1),xyPoint(:,2))
xlim([-15,15])
ylim([-15,15])
xlabel('East')
ylabel('North')
grid()
title('Gang Han-101030341')
disp(strcat('image saved as',pwd,'\m3.png'));
saveas(gcf,'m3.png')

%b sum up all of the vectors to find the final location
disp('sum up all of the vectors to find the final location:')
sum(xyShift)

%c determine the total distance traveled by the helicopter by finding the norm of each vector and calculating the sum
distance=zeros(length(xyShift),1);
for i = 1:length(xyShift)
    distance(i)=sqrt(xyShift(i,1)^2+xyShift(i,2)^2);
end
distance

disp('calculating the sum(distance):')
sum(distance)

