import os
# os.system("D:/v3d_external/bin/vaa3d_msvc.exe /x D:/vaa3d_tools/bin/plugins/neuron_tracing\Vaa3D_Neuron2/vn2.dll /f app2 /i D:/soamdata/test/test.v3draw /p 100 0 -1")
path="D:\soamdata"
files=os.listdir(path)
for file in files:
    # print(file[-6:])
    if file[-6:]=="v3draw":
        # print(file)
        commandStr="D:/v3d_external/bin/vaa3d_msvc.exe " \
                   "/x D:/vaa3d_tools/bin/plugins/neuron_tracing\Vaa3D_Neuron2/vn2.dll " \
                   "/f app2 " \
                   "/i  \"%s\" " \
                   "/p \"\" 0 -1"%(path+"/"+file)
        print(commandStr)
        os.system(commandStr)