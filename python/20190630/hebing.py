import pandas as pd
import os
import numpy as np

if __name__=="__main__":
    path="./data"
    files=sorted(os.listdir(path))
    count=0

    for file in files:
        fullpath=os.path.join(path,file)
        print(fullpath)
        df=pd.read_excel(fullpath,header=None)
        data=df.values[1:,:]
        print(data.shape)

        if data.shape[0]==0:
            continue
        if count==0:
            all=df.values[0,:]
            all=np.vstack((all,data));
            count+=1
        else:
            all=np.vstack((all,data))

    print(all.shape)

    all=pd.DataFrame(all)
    all.to_excel('Results_1.xlsx', index=False, header=False)
    # outfile=open("result.csv",'w')



