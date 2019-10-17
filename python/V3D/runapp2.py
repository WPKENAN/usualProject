import os
import numpy as np

def app2(path):
    commandStr = "D:\\v3d\\v3d_external\\bin\\vaa3d_msvc.exe " \
                 "/x D:\\v3d\\v3d_external\\bin\\plugins\\wpkenanPlugin\\Vaa3D_Neuron2\\vn2.dll " \
                 "/f app2 " \
                 "/i  {} " \
                 "/p {} 0 1".format(path,path+".marker")


    print(commandStr)
    os.system(commandStr)
    out=None
    out=os.popen(commandStr).readlines()
    return out

def createMarker(path,center,sigma,vector):
    path=path+".vec.marker"
    outfile=open(path,'w')
    color=["0,0,255","0,255,0","255,0,0"]

    inter=2

    for i in range(3):
        # print((int(-inter*sigma[i]//sigma[3]),int(inter*sigma[i]//sigma[3])))
        # print(int(-inter*sigma[0,i]//sigma[0,2]),int(inter*sigma[0,i]//sigma[0,2]))
        for j in range(int(-inter*sigma[0,i]//sigma[0,2]),int(inter*sigma[0,i]//sigma[0,2])):
            pixel=center+j*vector[i]
            outfile.write("{}, {}, {}, 1, 1, , , {}\n".format(pixel[0],pixel[1],pixel[2],color[i]))



    outfile.close()



if __name__=="__main__":
    path="C:\\Users\wpkenan\Desktop\\data\\34616.2_19386.1_3625.72.v3draw"
    out=app2(path)
    print(out)
    # exit(0)
    center = np.array([104.415, 19.089, 46.824])
    vector = np.zeros((3,3))
    sigma = np.zeros((1,3))
    print("start")
    for i in range(3,6):
        out[-i]=out[-i].strip(',\n').split(',')
        print(out[-i])
        for j in range(len(out[-i])):
            vector[i-3,j]=float(out[-i][j])

    out[-6]=out[-6].strip(',\n').split(',')

    for j in range(len(out[-6])):
        sigma[0,j]=out[-6][j]

    print(sigma)
    print(vector)
    # createMarker()
    createMarker(path,center,sigma,vector)