import os

if __name__=="__main__":

    # folder="C:\\Users\Anzhi\Documents\WXWork\\1688850161522981\Cache\File\\2019-04\\2Dpng-result\predict\\0\\1"
    folder="D:\soamdata\\ultratracer\\17545\\17545_app3\in\\124_10394.590_19439.407_1837.117.v3draw.marker"
    outfile=open(folder+"\\..\\FP.apo",'w')
    count=1+100000000;
    for file in os.listdir(folder):
        file=file.split('.')[0].split('_');
        outfile.write("{}, ,  {},, {},{},{}, 0,0,0,50,0,,,,0,255,0\n".format(count,count,int(file[2])*2, int(file[0])*2, int(file[1])*2))
        count=count+1

