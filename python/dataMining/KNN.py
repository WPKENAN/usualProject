import pandas as pd
import numpy as np
import os
import time
# base_data=pd.read_csv("D:\github\\usualProject\python\dataMining\dataset\\001\\201807.csv");
#
# # print(base_data.info())
#
# print(base_data.loc[0:3,['ts','var001']])
#
# print(base_data.loc([0]))

my_NaN=-9999

def distance(a,b):
    count=0;
    diff=0;
    for i in range(len(a)):
        if a[i]==my_NaN or b[i]==my_NaN:
            continue
        else:
            count=count+1;
            diff=diff+(a[i]-b[i])**2;
    return diff/count


def my_main(csvPath):
    outCsvPath = csvPath + "\\..\\result.csv"
    content = open(csvPath).readlines();
    # print(len(content))
    # print(content[1]);
    matrix = np.zeros((len(content) - 1, 68));

    # 预处理
    for i in range(1, len(content)):
        content[i] = content[i].strip('\n');
        content[i] = content[i].split(',');
        # print(content[i])
        # print(len(content[1]))
        for j in range(2, 70):
            # print(j)
            try:
                matrix[i - 1][j - 2] = float(content[i][j])
            except:
                # print(content[i][j])
                matrix[i - 1][j - 2] = my_NaN * 1.0
                # print(content[i])

    # 归一化
    matrix_normal = matrix / (np.max(matrix, axis=0) - np.min(matrix, axis=0));

    # 空值设置为my_NaN
    for i in range(1, len(content)):
        for j in range(2, 70):
            if (content[i][j] == ''):
                # print(matrix_normal[i-1])
                matrix_normal[i - 1, j - 2] = my_NaN;

    # 计算距离
    con = 0;
    for i in range(len(matrix_normal)):
        if i%100==0:
            print(i)
        if sum(matrix_normal[i] == my_NaN) == 0:
            con = con + 1;
            continue

        min_diff = 99999999;
        min_index = i;

        for j in range(max(0, i - 1000), min(i + 1000, len(matrix_normal))):
            if j == i:
                continue;
            diff = distance(matrix_normal[i], matrix_normal[j]);
            if min_diff > diff:
                min_index = j;
                min_diff = diff;

        for j in range(len(matrix_normal[i])):
            if matrix_normal[i, j] == my_NaN and matrix_normal[min_index, j] != my_NaN:
                matrix_normal[i, j] = matrix_normal[min_index, j];
                matrix[i, j] = matrix[min_index, j];

    for i in range(len(matrix)):
        if sum(matrix_normal[i] == my_NaN) == 0:
            continue
        for j in range(len(matrix[0])):
            if matrix[i, j] == my_NaN and j != 15 and j != 19 and j != 46 and j != 52 and j != 65:
                matrix[i, j] = np.average(matrix[:, j]);

            elif matrix[i, j] == my_NaN:
                tmp = i;
                isOk = 1;
                while (isOk):
                    tmp = tmp - 1;
                    if tmp >= 0 and matrix[tmp, j] != my_NaN:
                        break;
                    tmp = tmp + 2;
                    if tmp <= len(matrix) - 1 and matrix[tmp, j] != my_NaN:
                        break;
                matrix[i, j] = matrix[tmp, j];

    outFile = open(outCsvPath, 'w');
    outFile.write(content[0]);

    for i in range(len(matrix)):
        outFile.write("{},{},".format(content[i + 1][0], content[i + 1][1]))
        for j in range(len(matrix[0])):
            outFile.write("{}".format(matrix[i, j]));
            if j != len(matrix[0] - 1):
                outFile.write(',');
        outFile.write('\n');
    outFile.close()


def my_main2(csvPath):
    outCsvPath = csvPath + "\\..\\result.csv"
    content = open(csvPath).readlines();
    # print(len(content))
    # print(content[1]);
    matrix = np.zeros((len(content) - 1, 68));

    # 预处理
    for i in range(1, len(content)):
        print(i)
        content[i] = content[i].strip('\n');
        content[i] = content[i].split(',');
        # print(content[i])
        # print(len(content[1]))
        for j in range(2, 70):
            # print(j)
            try:
                matrix[i - 1][j - 2] = float(content[i][j])
            except:
                # print(content[i][j])
                matrix[i - 1][j - 2] = my_NaN * 1.0
                # print(content[i])

    for i in range(len(matrix)):
        print(i)
        if sum(matrix[i] == my_NaN) == 0:
            continue
        matrix[i] = np.average(matrix[:])
        #15 and j != 19 and j != 46 and j != 52 and j != 65:
        for j in [15,19,46,52,65]:
            tmp=i;
            tmpadd = i;
            tmpsub=i;
            isOk = 1;
            while (isOk):
                tmpsub = tmpsub - 1;
                if tmpsub >= 0 and matrix[tmpsub, j] != my_NaN:
                    tmp=tmpsub;
                    break;
                tmpadd = tmpadd + 1;
                if tmpadd <= len(matrix) - 1 and matrix[tmpadd, j] != my_NaN:
                    tmp=tmpadd;
                    break;
            matrix[i, j] = matrix[tmp, j];

    outFile = open(outCsvPath, 'w');
    outFile.write(content[0]);

    for i in range(len(matrix)):
        outFile.write("{},{},".format(content[i + 1][0], content[i + 1][1]))
        for j in range(len(matrix[0])):
            outFile.write("{}".format(matrix[i, j]));
            if j != len(matrix[0] - 1):
                outFile.write(',');
        outFile.write('\n');
    outFile.close()

def selectResult(templateFilePath):

    templateFile=open(templateFilePath);
    content=templateFile.readlines();

    wtid=0;
    lines = {}
    for i in range(1,len(content)):
        if int(content[i].split(',')[1])!=wtid:

            lines = {}
            print("********************{}**********************".format(i))
            wtid = int(content[i].split(',')[1])
            tempFilePath="D:\github\\usualProject\python\dataMining\\dataset\\{0:03}\\result.csv".format(int(content[i].split(',')[1]));
            print(tempFilePath)
            tempContent=open(tempFilePath).readlines();
            for j in range(len(tempContent)):
                # tempContent[j]=tempContent[j].strip('\n');
                # tempContent[j]=tempContent[j].split(',');
                lines[(tempContent[j].split(',')[0]).split('.')[0]]=tempContent[j];

        # print(lines['2018-07-01 10:12:52.365'])
        print(i)
        if (content[i].split(',')[0]).split('.')[0] in lines:
            content[i]=lines[(content[i].split(',')[0]).split('.')[0]];
        else:
            hms=(content[i].split(',')[0]).split('.')[0];
            h=hms.split(':')[0];
            m=hms.split(':')[1];
            s=hms.split(':')[2];
            cnt=0
            while((h+":"+m+":"+s) not in lines):
                cnt=cnt+1
                if cnt>100:
                    break;
                # print((h + ":" + m + ":" + s))
                if int(s)==0:
                    s=str(59)
                    m=str(int(m)-1)
                else:
                    s=str(int(s)-1)

                if int(m)<=0:
                    break
            hms=(h+":"+m+":"+s);
            if hms in lines:
                content[i] = lines[hms];
            else:
                hms = (content[i].split(',')[0]).split('.')[0];
                h = hms.split(':')[0];
                m = hms.split(':')[1];
                s = hms.split(':')[2];
                cnt = 0
                while ((h + ":" + m + ":" + s) not in lines):
                    cnt = cnt + 1
                    if cnt > 100:
                        break;
                    # print((h + ":" + m + ":" + s))
                    if int(s) == 60:
                        s = str(0)
                        m = str(int(m) + 1)
                    else:
                        s = str(int(s) + 1)

                    if int(m) >= 59:
                        break
                hms = (h + ":" + m + ":" + s);
                if hms in lines:
                    content[i] = lines[hms];


    outPath = templateFilePath + "\\..\\result.csv";
    outFile=open(outPath,'w');
    # outFile.write(content[0]);

    for i in range(0,len(content)):
        outFile.write(content[i]);





if __name__ == '__main__':
    Folders = "D:\github\\usualProject\python\dataMining\dataset"
    '''
    for sonFolder in os.listdir(Folders):
        start=time.time();
        csvFolder=Folders+"\\"+sonFolder
        print(csvFolder)
        my_main(csvFolder+"\\201807.csv")
        print(time.time()-start)
    '''
    # selectResult("D:\github\\usualProject\python\dataMining\\template_submit_result\\template_submit_result.csv")
    my_main2("D:\github\\usualProject\python\dataMining\\template_submit_result\\result2.csv")




















