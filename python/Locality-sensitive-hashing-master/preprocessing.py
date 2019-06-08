from min_hash import *
import matplotlib.pyplot as plt


def txtToCsv(txtPath,csvPath):
    out=open(csvPath,'w');
    count=0;
    with open(txtPath) as f:
        for line in f:
            out.write(line.split()[0]+",")
            line = line.split()[3:]
            for i in line:
               if str(i) == "9.999000e+003":
                  i = "0"
               out.write(i+",")
            out.write("\n")
            count = 1 + count
    print(count)

def csvTohwCsv(csvPath,hwCsvPath):
    out = open(hwCsvPath, 'w');
    count = 0;
    with open(csvPath) as f:
        for line in f:
            out.write(line.split(',')[0] + ",")
            line = line.split(',')[1:89]
            i=0
            # print(len(line))
            while i < len(line):
                out.write('{},'.format(float(line[i])*float(line[i+1])))
                i=i+2;
            out.write('\n')
            count+=1

    print(count)


if __name__=="__main__":

    print("txt转换成csv，一次性")
    #txt转换成csv，一次性
    txtToCsv('./data/hzqso_ssw.txt','./data/hzqso_ssw.csv')
    txtToCsv('./data/mstar_ssw.txt', './data/mstar_ssw.csv')
    txtToCsv('./data/qso_ssw.txt', './data/qso_ssw.csv')
    txtToCsv('./data/star_ssw.txt', './data/star_ssw.csv')
    txtToCsv('./data/galaxy_ssw1.txt', './data/galaxy_ssw1.csv')

    print("转换两列相乘")
    #转换两列相乘
    csvTohwCsv('./data/hzqso_ssw.csv','./data/hzqso_ssw_hw.csv')
    csvTohwCsv('./data/mstar_ssw.csv', './data/mstar_ssw_hw.csv')
    csvTohwCsv('./data/qso_ssw.csv', './data/qso_ssw_hw.csv')
    csvTohwCsv('./data/star_ssw.csv', './data/star_ssw_hw.csv')
    csvTohwCsv('./data/galaxy_ssw1.csv', './data/galaxy_ssw1_hw.csv')

    #合并csv


