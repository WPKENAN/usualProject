X=27300
Y=17206
Z=4923

Cx=int((12800-3520)/512);
Cy=int((24000-5120)/512);
Cz=int((3520-320)/512);


def main(path):
    xyz=[]
    file=open(path);
    lines=file.readlines();
    for i in range(len(lines)):
        lines[i]=lines[i].strip('\n').split(',');
        xyz.append([int(lines[i][5]),int(lines[i][6]),int(lines[i][4])])
    print(xyz)
    return xyz;

if __name__=="__main__":
    path="D:\wp\微信文件夹\WeChat Files\WPKENAN\FileStorage\File\\2019-04\\4.apo"
    xyz=main(path)
    index=0;
    center_xyz=xyz.copy()

    for i in range(Cz):
        for j in range(Cy):
            for k in range(Cx):
                px=k*512+256+3520;
                py=j*512+256+5120;
                pz=i*512+256+320;
                for index in range(len(xyz)):
                    if abs(xyz[index][0]-px)<=256 and abs(xyz[index][1]-py)<=256 and abs(xyz[index][2]-pz)<=256:
                        center_xyz[index]=[px,py,pz]
                        break

    print(center_xyz)
    outfile=open(path+"\\..\\center_xyz.apo",'w');
    for i in range(len(center_xyz)):
        outfile.write("{}, ,  {},, {},{},{}, 0,0,0,50,0,,,,0,0,255\n".format(i,i,center_xyz[i][2],center_xyz[i][0],center_xyz[i][1]))






