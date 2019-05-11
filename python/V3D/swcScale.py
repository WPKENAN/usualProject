import shutil
import os

def scaleSwc(inpath,outpath,scale):
    lines = open(inpath).readlines();
    output = open(outpath, 'w');
    for i in range(len(lines)):
        if lines[i][0] == '#':
            output.write(lines[i])
            continue
        lines[i] = lines[i].strip('\n');
        lines[i] = lines[i].split(' ');
        output.write("{} {} {} {} {} {} {}\n".format(eval(lines[i][0]), lines[i][1], eval(lines[i][2])*scale,
                                                     eval(lines[i][3])*scale, eval(lines[i][4])*scale, lines[i][5],
                                                     eval(lines[i][6])))
        # print(lines[i])
    output.close()


def main():

if __name__=="__main__":
    scaleSwc("D:\soamdata\\ultratracer\\17302\\17302_manual\\17302_CPU_001.processed.swc","D:\soamdata\\ultratracer\\17302\\17302_manual\\test.swc",0.5)

