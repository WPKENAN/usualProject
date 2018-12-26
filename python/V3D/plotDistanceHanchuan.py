import numpy as np
import matplotlib.pyplot as plt
import re
import os

def main():
    distanceFolder="D:\soamdata\\17302\distance"
    data={}
    for i in os.listdir(distanceFolder):
        tmplines=np.zeros((128,8))-1;
        # print(i)
        for j in os.listdir(os.path.join(distanceFolder,i)):
            tmpline = [];
            id=int(re.findall("\((.+?)\)",j)[0])
            # print(id)
            distanceFile=open(os.path.join(distanceFolder,i,j));
            lines=distanceFile.readlines();
            tmpline.append(id)
            for line in lines:
                if line[0]=='i':
                    continue
                line=line.strip('\n');
                line=line.split('=');
                # print(line)
                tmpline.append(float(line[-1]));
            tmplines[id,:]=np.array(tmpline);
        # print("***********************************************")
        # for item in tmplines:
            # print(item)
        data[i]=tmplines
        # print(len(data[i]))

    name=list(data.keys());
    name.sort();

    for i in name:
        # print(distanceFolder+i+".csv")
        outfile = open(distanceFolder+"\\..\\"+i+".csv",'w');
        # print("{},{},{},{},{},{},{}".format("manual_To_"+i.split('s')[-1],i.split('s')[-1]+"_To_manual","average of bi-directional entire-structure-averages","differen-structure-average ",4,5,6))
        outfile.write("{},{},{},{},{},{},{},{}\n".
                      format("id","manual_To_"+i.split('s')[-1],i.split('s')[-1]+"_To_manual","average of bi-directional entire-structure-averages","differen-structure-average ",4,5,6))
        for j in data[i]:
            # print(j)
            outfile.write("{},{},{},{},{},{},{}\n".
                          format(j[0],j[1],j[2],j[3],j[4],j[5],j[6],j[7]))
    # print(tmplines)

    # y={}
    # for i in name:
    #     y[i] = np.zeros((106, 8));
    #     count=0;
    #     for j in data[i]:
    #         if j[1]>0:
    #             y[i][count]=j;
    #             count=count+1;
    #
    # plt.scatter(y["17302_Whole_Cut_Prun(To)splitTofolders3.1"][:,0],y["17302_Whole_Cut_Prun(To)splitTofolders2.1"][:,3]-y["17302_Whole_Cut_Prun(To)splitTofolders3.1"][:,3])
    # plt.show()
    # for i in data["17302_Whole_Cut_Prun(To)splitTofolders3.2"]:

        # print(np.array(data[i]))

def plotMy(filePath):
    filePath="D:\soamdata\\17302\\result.txt"
    file=open(filePath);
    lines=file.readlines();
    matrix=np.zeros((27,14));
    index=0;
    for line in lines:
        line=line.strip('\n')
        line=line.split('\t')
        # print(line)
        while '' in line:
            line.remove('')
        # print(line)
        if int(line[1])>1:
            for i in range(len(line)):
                matrix[index,i]=float(line[i]);
            index=index+1

    print(matrix)


    plt.figure()
    # for i in range(len(matrix[:,0])):
        # if

    plt.plot(matrix[:,0],matrix[:,7],label="App3.1");
    plt.plot(matrix[:, 0], matrix[:, 10],label="App2.1");
    plt.title("distance betweet auto and manual")
    plt.legend()
    # plt.savefig("D:\soamdata\\17302\\0.png")
    plt.show()


    positive=matrix[:, 10] - matrix[:, 13]<0;
    negetive=matrix[:, 10] - matrix[:, 13]>0;
    zeros=matrix[:, 10] - matrix[:, 13]==0
    plt.scatter(matrix[ positive, 0],
                -matrix[positive, 10] + matrix[positive, 13], c='r',label="App2.2 - App2.1 > 0")
    plt.scatter(matrix[negetive, 0],
                -matrix[negetive, 10] + matrix[negetive, 13], c='b',label="App2.2 - App2.1 < 0")
    plt.scatter(matrix[zeros, 0],
                -matrix[zeros, 10] + matrix[zeros, 13], c='y', label="App2.2 - App2.1 == 0")
    plt.title("")
    plt.grid()
    plt.legend()
    # plt.savefig("D:\soamdata\\17302\\1.png")
    plt.show()


    positive = matrix[:, 7] - matrix[:, 10] > 0;
    negetive = matrix[:, 7] - matrix[:, 10] < 0;
    zeros = matrix[:, 7] - matrix[:, 10] == 0
    plt.scatter(matrix[positive, 0],
                matrix[positive, 7] - matrix[positive, 10], c='r', label="App3.1 - App2.1 > 0")
    plt.scatter(matrix[negetive, 0],
                matrix[negetive, 7] - matrix[negetive, 10], c='b', label="App3.1 - App2.1 < 0")
    plt.scatter(matrix[zeros, 0],
                matrix[zeros, 7] - matrix[zeros, 10], c='y', label="App3.1 - App2.1 == 0")
    plt.grid()
    plt.legend()
    # plt.savefig("D:\soamdata\\17302\\2.png")
    plt.show()

    positive = matrix[:, 13] - matrix[:, 10] > 0;
    negetive = matrix[:, 13] - matrix[:, 10] < 0;
    zeros = matrix[:, 13] - matrix[:, 10] == 0
    plt.scatter(matrix[positive, 0],
                matrix[positive, 13] - matrix[positive, 10], c='r', label="App3.2 - App2.1 > 0")
    plt.scatter(matrix[negetive, 0],
                matrix[negetive, 13] - matrix[negetive, 10], c='b', label="App3.2 - App2.1 < 0")
    plt.scatter(matrix[zeros, 0],
                matrix[zeros, 13] - matrix[zeros, 10], c='y', label="App3.2 - App2.1 == 0")
    plt.grid()
    plt.legend()
    plt.savefig("D:\soamdata\\17302\\3.png")
    plt.show()




if __name__=="__main__":
    main()
    plotMy('')
