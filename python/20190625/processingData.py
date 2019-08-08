import pandas as pd

def readXlsx(path,header=None):
    df=pd.read_excel(path,header=header);
    # print(df)
    data=df.values[:,1:]
    # print(data)
    return data

if __name__=="__main__":
    path='data.xlsx'
    readXlsx(path,0)