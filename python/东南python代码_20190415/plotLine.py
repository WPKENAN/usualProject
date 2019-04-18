import numpy as np
import matplotlib.pyplot as plt
def readTxt(path):
    contents=open(path).readlines();
    # print(contents)
    contents=contents[1:len(contents)]

    time=[]
    for i in range(len(contents)):
        contents[i]=contents[i].strip('\n').split(',');
        time.append(int(contents[i][1]))

    return time

def main():
    path="C:\\Users\\admin\\Documents\\Tencent Files\\3272346474\\FileRecv\\复赛answer.txt"
    time=np.array(readTxt(path))
    cal={}
    for item in time:
        if item not in cal:
            cal[item]=0
        else:
            cal[item]=cal[item]+1

    keys=list(cal.keys())
    keys.sort();
    # print(keys)
    x=[]
    y=[]
    count=0
    x.append(keys[0])
    y.append(cal[keys[0]])
    for i in range(1,len(keys)):
        x.append(keys[i])
        y.append(cal[keys[i]]+y[i-1])

    print(cal[6])
    print(x)
    print(y)
    plt.figure();
    plt.plot(x,y);
    plt.title('answer')
    plt.show()
if __name__=="__main__":
    main()
