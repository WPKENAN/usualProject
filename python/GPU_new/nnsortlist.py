"""大数据量处理程序 可自定义缓存大小 和batch大小"""
from sklearn.externals import joblib
from dataloader import readall_image_list,fillWithZero,fillWithMean,scale
import numpy as np
import pandas as pd


import os



import data as dt
needscale=dt.needscale

import pickle as pk
import argparse
opt=argparse.ArgumentParser(description="神经网络样本筛选排序程序 ")
opt.add_argument("-m","--model",type=str,default=".",help="train程序导出的模型目录")
opt.add_argument("-b","--batchsize",type=int,default=1000,help="一次处理的文件的数量")
opt.add_argument("-c","--cachesize",type=int,default=100000,help="文件缓存队列的大小")
opt.add_argument("-f","--datadir",type=str,default="./data/true",help="数据目录")
opt.add_argument("-t","--tofile",type=str,default="./result.csv",help="输出文件（csv格式）")
opt=opt.parse_args()
#读取模型的固有参数
modelpath=opt.model
mfile=f"{modelpath}/nclf.m"
parfile=f"{modelpath}/par.conf"
#参数字典
with open(parfile,"rb") as f:
    pardict=pk.load(f)

nshape=pardict["nshape"]
starts=pardict["starts"]
#设置dt中的参数
dt.nshape=nshape
dt.starts=starts

#得到src和dst
srcdir,outfile=opt.datadir,opt.tofile
def filterData(files,imgs):
    #标准shape
    global nshape
    ret=[(imgs[i],files[i]) for i in range(len(imgs)) if imgs[i].shape==tuple(nshape)]
    ret=list(zip(*ret))
    return ret



def dealwith(clf,flist,data):
    """data为与处理过的数据"""
    #预测
    res=clf.predict(data)
    resp=clf.predict_proba(data)
    selector=resp.argmax(axis=1)==1
    #选出resp中正类位置的proba向量
    sresp=resp[selector]
    #正类置信度
    tprobs=sresp[:,1]
    #取正类文件列表 与正类置信度一一对应
    tflist=flist[selector]
    #idx排序
    idxs=np.arange(0,len(tflist),step=1)
    idxs=sorted(idxs,key=lambda i:tprobs[i],reverse=True)
    #用idxs进行assign操作
    tprobs,tflist=tprobs[idxs],tflist[idxs]
    #输出提示信息
    # print(f"已处理{len(flist)}个样本 其中正类数:{len(sresp)} 正类比例:{100*(len(sresp)/len(flist))}% 正类样本平均置信度:{tprobs.mean()}")



    #输出
    rd=list(zip(tprobs,tflist))
    ret=pd.DataFrame(data=rd,columns=["置信度","文件名"])
    return ret

def generator(clf,bqueue):
    while True:
        bt=bqueue.get()
        if bt=="end":break
        yield dealwith(clf,*bt)


def provider(flist,bs,bqueue):
    #分批处理 一次处理1000个
    step=len(flist)//bs
    if step*bs<len(flist):step+=1
    #记录保存
    bili,zhixindu=[],[]
    for i in range(step):
        start=i*bs
        end=start+bs
        #剪切
        cflist=flist[start:end]
        data=readall_image_list(cflist)
        #预处理
        data=dt.images_preproc(data,dofilter=False)
        #过滤
        data,cflist=filterData(cflist,data)
        ###
        cflist=np.array(cflist)
        bqueue.put((cflist,np.array(data)))
    bqueue.put("end")

from multiprocessing import Queue,Process
def getresults(clf,flist,bs):
    bq=Queue(maxsize=100000//bs)
    prov=Process(target=provider,args=(flist,bs,bq))
    prov.start()
    yield from generator(clf,bq)
    prov.join()


#除此之外 所有flist都为全路径
def main():
    clf=joblib.load(mfile)
    # clf=None
    flist=np.array([os.path.join(srcdir,i) for i in os.listdir(srcdir)])
    #分批处理 一次处理1000个
    bs=1000
    step=len(flist)//bs
    if step*bs<len(flist):step+=1
    allret=None
    #记录保存
    bili,zhixindu=[],[]
    for i,ret in enumerate(getresults(clf,flist,bs)):
        if allret is None:allret=ret
        else:allret=pd.concat([allret,ret]).reset_index(drop=True)
        #输出
        print(f"已处理:{i*bs+bs}个文件 平均正类置信度:{ret['置信度'].mean()} 正类比例:{100*(len(ret)/bs)}%")
        zhixindu.append(ret['置信度'].mean())
        bili.append(100*(len(ret)/bs))
    #输出总的比比例和置信度
    print(f"总正类比例:{np.array(bili).mean()}% 总平均置信度:{100*np.array(zhixindu).mean()}")
    allret=allret.sort_values(by=["置信度"],ascending=False).reset_index(drop=True)
    allret.to_csv(outfile)
    
if __name__=="__main__":
    main()