import matplotlib.pyplot as plt
import numpy as np
def readCsv(path):
    lines = open(path).readlines();
    lines=lines[1:len(lines)];
    return lines;

def output_dir_speed(lines):
    dir_speed=[]
    for i in range(len(lines)):
        lines[i]=lines[i].strip('\n').split(',');
        #lng-3,lat-4,time-10

        lines[i][2]=float(lines[i][2]);
        lines[i][11]=float(lines[i][11]);
        dir_speed.append([lines[i][2],lines[i][11]])
    # print(dir_speed)
    return dir_speed
if __name__=="__main__":
    path="D:\\github\\Data\\AA00160.csv";
    lines=readCsv(path);
    dir_speed=output_dir_speed(lines);
    dir_speed=np.array(dir_speed);

    swerve=np.zeros((len(dir_speed)));
    for i in range(1,len(dir_speed)):
        swerve[i]=abs(dir_speed[i,0]-dir_speed[i-1,0]);#前后两次角度做差就是转弯角度,取绝对值
    plt.scatter(range(len(swerve)),swerve)
    plt.title('swerve')
    plt.xlabel('index')
    plt.ylabel('angle')
    plt.show()
    angle=30#定义超过30°为转弯
    speed=40;#定义速度60为超速
    count=0;
    outfile=open("result.csv","w");
    outfile.write("在原excel中的第几行(行号从1开始),真实数据序号(序号从0开始),转弯角度,转弯速度,vehicleplatenumber,device_num,direction_angle,lng,lat,acc_state,right_turn_signals,left_turn_signals,hand_brake,foot_brake,location_time,gps_speed,mileage\n")
    for i in range(len(swerve)):
        if swerve[i]>angle and dir_speed[i,1]>40:
            outfile.write("{},{},{},{}".format(i+2,i,swerve[i],dir_speed[i,1]));
            # print(lines[i])
            for item in lines[i]:
                outfile.write(",{}".format(item));
            outfile.write("\n")
            count=count+1;
    print("转弯角度超过{},并且速度大于{}的总共有{}次".format(angle,speed,count))
