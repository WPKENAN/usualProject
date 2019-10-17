import dataloader as dl
import data as dt
from sklearn import decomposition as dec
import numpy as np


import argparse
opt=argparse.ArgumentParser(description="神经网络训练程序 （第一个EPOCH比较慢，缓存主要用于加速中后期训练)")
opt.add_argument("-m","--model",type=str,default="cnnmodel",help="模型名字（models内模型文件的名字 不带.py后缀")
opt.add_argument("-e","--epochs",help="训练轮数",type=int,default=15)

#数据行列（不算时间列和第一行)
opt.add_argument("-ls","--height",help="需要取的数据的行数",type=int,default=841)
opt.add_argument("-cs","--width",help="需要取的数据的列数",type=int,default=25)
#含义：从开始行开始  取hegith行数据
#从开始列开始 取width列数据
#裁剪
opt.add_argument("-sl","--startline",help="取数据开始的行数",type=int,default=0)
opt.add_argument("-sc","--startcolumn",help="取数据开始的列数",type=int,default=0)
opt.add_argument("-bs","--batchsize",help="训练批次大小",type=int,default=30)
opt.add_argument("-c","--cache",help="数据准备队列缓存大小",type=int,default=100000)
opt.add_argument("-pc","--positive_cache",help="正类样本缓存大小",type=int,default=40000)
opt.add_argument("-ts","--train_size")
opt.add_argument("-d","--data",type=str,help="训练用数据的保存目录（正类在子文件夹 true中  负类在子文件夹 false中)")
#模型保存位置
opt.add_argument("-o","--output",help="训练后模型输出目录(输出文件为nclf.m和par.conf)",type=str,default="./")
#默认 20000
opt=opt.parse_args()

input_shape=(int(opt.height),int(opt.width))
epochs=int(opt.epochs)
outputfile=opt.output
#裁剪参数
startline=int(opt.startline)
startcolumn=int(opt.startcolumn)
#数据参数
cachesize=int(opt.cache)
batch_size=int(opt.batchsize)
pcache=int(opt.positive_cache)

dt.set_buffersize(pcache)
#设置数据处理器参数
dt.nshape=input_shape
dt.starts=(startline,startcolumn)
# epochs=15
#
dtdir=opt.data
dt.setdatadir(dtdir)
def main():
    data,label=dt.getfalldatas()
    #平衡
    # data,label=dt.ensure_balance_filelist(data,label)
    #得到数据集参数
    allcount=len(data)
    trainlen=int(allcount*0.8)
    testlen=allcount-trainlen
    #生成训练和测试
    train=[data[:trainlen],label[:trainlen]]
    test=[data[trainlen:],label[trainlen:]]
    #输出数据集参数
    print(f"训练样本中 正样本:{train[1].sum()} 负样本:{len(train[1])-train[1].sum()}")
    print(f"测试样本中 正样本:{test[1].sum()} 负样本:{len(test[1])-test[1].sum()}")
    #平衡
    train[0],train[1]=dt.ensure_balance_filelist(train[0],train[1])
    test[0],test[1]=dt.ensure_balance_filelist(test[0],test[1])
    #训练集重采样
    #train=dl.gen_resimple(*train,pre_random_simple=False) 



    from sklearn.metrics import accuracy_score,recall_score,roc_curve,auc,precision_score
    from sklearn import preprocessing as prep
    from scipy import interp
    #神经网络
    import kerasmodel as kmodel
    #设置模型文件名 
    kmodel.modelfilename=opt.model
    clf=kmodel.model(batch_size,input_shape)

    import math
    datagen=dt.dataflow(train[0],train[1],batch_size=batch_size,queue_size=cachesize)
    testgen=dt.dataflow(test[0],test[1],batch_size=batch_size,queue_size=cachesize)
    steps=[int(math.ceil(len(train[0])/batch_size)),int(math.ceil(len(test[0])/batch_size))]
    clf.fit_generator(datagen,classes=2,steps_per_epoch=steps[0],epochs=epochs,verbose=1,validation_data=testgen,validation_steps=steps[1])
    #枚举器

    ###训练结束

    #准备一部分测试数据 样本大小为10000
    scgen=dt.datagenerator(test[0],test[1],batch_size=max(10000,len(test[0])))
    tdata,tlabel=scgen.__next__()
    clfres=clf.predict(tdata)
    #计算预测概率
    clfres_prop=clf.predict_proba(tdata)
    #计算正确率-
    acc=accuracy_score(tlabel,clfres)
    rec=recall_score(tlabel,clfres)
    pre=precision_score(tlabel,clfres)
    #输出参数
    logtxt=f"accuracy:{acc} recall:{rec} precision:{pre}"
    print(logtxt)
    with open("./log.txt","w") as f:
        f.write(logtxt)
    #得到标签的onehot编码
    enc=prep.OneHotEncoder(sparse=False)
    test_oh_label=enc.fit_transform(tlabel.reshape((-1,1)))
    #计算roc曲线 fpr为假阳性率  tpr为recall率 所有
    fpr,tpr,thresholds=roc_curve(tlabel,clfres_prop[:,1],pos_label=1)
    #画ROC曲线和计算AUC
    mean_tpr = 0.0  
    mean_fpr = np.linspace(0, 1, 100)  
    mean_tpr += interp(mean_fpr, fpr, tpr)          #对mean_tpr在mean_fpr处进行插值，通过scipy包调用interp()函数  
    mean_tpr[0] = 0.0                               #初始处为0  
    #计算auc值
    roc_auc = auc(fpr, tpr)  


    from matplotlib import pyplot as plt
    #画图，只需要plt.plot(fpr,tpr),变量roc_auc只是记录auc的值，通过auc()函数能计算出来  
    plt.plot(fpr, tpr, lw=1, label='ROC  %s (area = %0.3f)' % (type(clf).__name__, roc_auc))
    #画对角线
    plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Luck')  
    plt.legend()
    plt.savefig(f"{outputfile}./result.png")

    #保存模型

    from sklearn.externals import joblib

    joblib.dump(clf,f"{outputfile}/nclf.m")

    #保存参数
    import pickle as pk
    opts={
        "nshape":dt.nshape,
        "starts":dt.starts
    }
    with open(f"{outputfile}/par.conf","wb") as f:
        pk.dump(opts,f)

    with open(f"{outputfile}/par.txt","w") as f:
        f.write(f"以下内容仅供查看\n\n")
        f.write(f"{opts}")


if __name__=="__main__":
    main()