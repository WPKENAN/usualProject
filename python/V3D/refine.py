import os
import sys
import os
def sortSwc(v3dPath,inPath,outPath):
    commandStr="{} /x sort_neuron_swc /f sort_swc /i {} /o {} /p 0 1".format(v3dPath,inPath,outPath)
    os.system(commandStr)

if __name__=="__main__":
    v3dPath="D:\\v3d\\v3d_external\\bin\\vaa3d_msvc.exe"
    inPath="C:\\Users\\wpkenan\\Desktop\\refine\\refinement\\test.swc"
    outPath=inPath+"sorted.swc"
    sortSwc(v3dPath,inPath,outPath)
