import os

def shiftSwc(inpath,outpath,dx,dy,dz,dindex):
    lines=open(inpath).readlines();
    output=open(outpath,'w');
    for i in range(len(lines)):
        if lines[i][0]=='#':
            output.write(lines[i])
            continue
        lines[i]=lines[i].strip('\n');
        lines[i]=lines[i].split(' ');
        output.write("{} {} {} {} {} {} {}\n".format(eval(lines[i][0])+dindex,lines[i][1],eval(lines[i][2])+dx,eval(lines[i][3])+dy,eval(lines[i][4])+dz,lines[i][5],eval(lines[i][6])+dindex))
        # print(lines[i])
    output.close()

def mergeSwc(inpath1,inpath2,outpath):
    contents1=open(inpath1).read();
    contents2=open(inpath2).read();

    output=open(outpath,"w")

    output.write(contents1);
    output.write('\n');
    output.write(contents2)

def main():
    swcFolder1="D:\\soamdata\\ultratracer\\17545\\17545_app3\individual"
    swcFolder2="D:\\soamdata\\ultratracer\\17545\\17545_app2\individual"
    outFolder="D:\\soamdata\\ultratracer\\17545\\merge_swc"
    if not os.path.exists(outFolder):
        os.mkdir(outFolder)

    for file in os.listdir(swcFolder2):
        if file[-3:]=='swc':
            print(swcFolder2+"\\"+file)
            shiftSwc(swcFolder2+"\\"+file,outFolder+"\\"+(swcFolder2+"\\"+file).split("\\")[-1]+"_shift.swc",1000,0,0,999999)
            # break

    for file in os.listdir(swcFolder1):
        if file[-3:] == 'swc':
            print(outFolder+"\\"+file+"_shift.swc")

            mergeSwc(swcFolder1+"\\"+file,outFolder+"\\"+file+"_shift.swc",outFolder+"\\"+file)
            os.remove(outFolder + "\\" + file + "_shift.swc")


if __name__=="__main__":
    # path="D:\\soamdata\\ultratracer\\17302\\17302_app2\individual\\2_8100.000_7804.000_1474.000.v3draw.marker_nc_APP2_GD.swc"
    # shiftSwc(path,path+"\\..\\..\\..\\merge_swc\\"+path.split("\\")[-1]+"_shift.swc",10,10,10,999999);
    main()


