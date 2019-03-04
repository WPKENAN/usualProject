import os
import platform
import subprocess
import signal
import time

class TimeoutError(Exception):
    pass

def command(cmd, timeout=60):
    """Run command and return the output
    cmd - the command to run
    timeout - max seconds to wait for
    """
    is_linux = platform.system() == 'Linux'

    p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True,
                         preexec_fn=os.setsid if is_linux else None)
    t_beginning = time.time()
    seconds_passed = 0
    while True:
        # print(p.poll())
        if p.poll() is not None:
            break
        seconds_passed = time.time() - t_beginning
        if timeout and seconds_passed > timeout:
            if is_linux:
                os.killpg(p.pid, signal.SIGTERM)
            else:
                p.terminate()
            raise TimeoutError(cmd, timeout)
        # time.sleep(0.01)
        print("进度:{0}%".format(seconds_passed*100/timeout), end="\r")
    return p.stdout.read()

#os.system("D:/v3d_external/bin/vaa3d_msvc.exe /x D:/vaa3d_tools/bin/plugins/neuron_tracing\Vaa3D_Neuron2/vn2.dll /f app2 /i D:/soamdata/test/test.v3draw /p 100 0 -1")
#D:/v3d_external/bin/vaa3d_msvc.exe /x D:/vaa3d_tools/bin/plugins/neuron_tracing/Vaa3D_Neuron2/vn2.dll /f app2 /i  D:\soamdata\6\most\test\18454-1.v3draw /p "" 0 -1
#D:/v3d_external/bin/vaa3d_msvc.exe /x D:/vaa3d_tools/bin/plugins/neuron_tracing/Vaa3D_Neuron2/vn2.dll /f app3 /i  D:\soamdata\6\most\test\18454-1.v3draw /p "" 0 -1

def app2(path):
    print("app2 start:")
    files = os.listdir(path)
    count = 0;
    for file in files:
        # print(file[-6:])
        if file[-6:] == "v3draw":
            count = count + 1;
            print(file)
            commandStr = "D:/v3d_external/bin/vaa3d_msvc.exe " \
                         "/x D:/vaa3d_tools/bin/plugins/neuron_tracing\Vaa3D_Neuron2/vn2.dll " \
                         "/f app2 " \
                         "/i  \"%s\" " \
                         "/p \"\" 0 -1" % (path + "/" + file)
            # commandStr="ping www.baidu.com"
            # try:
            #     result = command(commandStr, timeout=60 * 10)
            # except TimeoutError:
            #     print('%s Run command timeout.' % (file))
            # else:
            #     print(result)

            os.system(commandStr)
            # break;

def app1(path):
    files = os.listdir(path)
    count=0;
    for file in files:
        # print(file[-6:])
        if file[-6:]=="v3draw":
            count=count+1;
            if count<20:
                continue;
            print(file)
            commandStr="D:/v3d_external/bin/vaa3d_msvc.exe " \
                       "/x D:/vaa3d_tools/bin/plugins/neuron_tracing\Vaa3D_Neuron2/vn2.dll " \
                       "/f app1 " \
                       "/i  \"%s\" " \
                       "/p \"\" 0 -1"%(path+"/"+file)
            # print(commandStr)

            # try:
            #     result = command(commandStr, timeout=60*10)
            # except TimeoutError:
            #     print('%s Run command timeout.'%(file))
            # else:
            #     print(result)

            os.system(commandStr)


def app3(path):
    print("app3 start:")
    files = os.listdir(path)
    count = 0;
    for file in files:
        # print(file[-6:])
        if file[-6:] == "v3draw":
            count = count + 1;
            print(file)
            commandStr = "D:/v3d_external/bin/vaa3d_msvc.exe " \
                         "/x D:/vaa3d_tools/bin/plugins/neuron_tracing\Vaa3D_Neuron2/vn2.dll " \
                         "/f app3 " \
                         "/i  \"%s\" " \
                         "/p \"%s\" 0 -1" % (path + "/" + file,path + "/" + file+".marker")
            print(commandStr)
            # commandStr="ping www.baidu.com"
            # try:
            #     result = command(commandStr, timeout=60 * 10)
            # except TimeoutError:
            #     print('%s Run command timeout.' % (file))
            # else:
            #     print(result)

            os.system(commandStr)
            # break;
if __name__ == '__main__':
    # path1 = "D:\soamdata\\7\mouseID_321237-17302\\app1"
    # app1(path1);
    # path2 = "D:\soamdata\\7\mouseID_321237-17302\\app2"
    # app2(path2);
    path3 = "D:\\soamdata\\7\\mouseID_321237-17302\\app3.1"
    path32="D:\\soamdata\\7\mouseID_321237-17302\\app3.2"
    app3(path32)
    # print("dsa")
