import pandas as pd
import os
import numpy as np
from sklearn.utils import shuffle
from multiprocessing.dummy import Pool as TPool

#虚拟进程池（线程池)
pool=TPool()
#多县城读取开关 生产者消费者情境不适用
multi=False
def dofunc(flist,func):
    """并行执行函数"""
    #由于此函数可能导致混合（true false）读取时标签数据不同步 导致训练失败 故临时屏蔽shuffle操作
    def farg(par):
        return func(*par)
    idxs=list(enumerate(flist))
    #多线程版本的读取 用于大批量读取文件
    if multi:
        res=list(pool.map(farg,idxs))
    else:
        res=list(map(farg,idxs))
    # print(f"已读取:{len(res)}个文件")
    return res

def _df_preprocess(df:pd.DataFrame):
    """
    对dataframe全体的预处理操作
    """
    ret=df.copy()
    #del ret[0]
    return ret




def readall_items(dirname)->pd.DataFrame:
    """
    读取一个目录里的所有csv文件并合并成一个列表
    返回的是一个DataFrame 列名维持原状
    """
    flist=os.listdir(dirname)
    def proc(i,fname):
        fpath=os.path.join(dirname,fname)
        return pd.read_csv(fpath)
    plist=dofunc(flist,proc)
    #合并
    retdata=pd.concat(plist)
    #处理
    retdata=_df_preprocess(retdata)
    return retdata

#以下函数都返回列表 若要转换为ndarray或dataframe 自行转换

def readall_vector(dirname):
    """
    一个csv文件当做一个图片处理 图片拉长成向量
    由于csv中的行数不同 向量长度不同 返回的是矩阵列表 item type=ndarray
    """
    flist=os.listdir(dirname)
    def proc(i,fname):
        fpath=os.path.join(dirname,fname)
        #读取并加入
        table=pd.read_csv(fpath)
        #预处理
        table=_df_preprocess(table)
        table=table.as_matrix().reshape((-1,))
        #合并
        return table
    plist=dofunc(flist,proc)
    return plist
    


#图片读取部分
def readall_image(dirname,maxsize=-1,fd=True):
    """
    读一个目录的csv文件 每个文件作为一个宽度为25 长度为
    返回为一个图片列表 (因为行数不同无法化为3d张量)
    """
    flist=os.listdir(dirname)
    #随机从一个目录读取文件 保证每次读取的文件列表都不一样
    flist=shuffle(flist)
    #根据限制剪切文件列表
    if maxsize!=-1:
        flist=flist[:maxsize]
    flist=[os.path.join(dirname,i) for i in flist]
    return readall_image_list(flist,fd)

#读取文件列表
fdmap={}
maxfd=40000
def set_maxfx(m):
    global maxfd
    maxfd=m
def readall_image_list(flist,fd=True):
    """要求flist中的每一项为完整路径名 fd为是否做缓存"""
    global maxfd
    # print(f"maxfd:{maxfd}")
    def proc(i,fname):
        fpath=fname
        #检查缓存
        if fd and fpath in fdmap:
            return fdmap[fpath]
        #读取并加入
        table=pd.read_csv(fpath)
        table=_df_preprocess(table)
        table=table.as_matrix()
        #如果缓存没满就加入缓存
        #优先缓存正类
        if fd and len(fdmap)<maxfd:
            #判断条件 只缓存正样本
            if fpath.find("true")!=-1:
                fdmap[fpath]=table
        return table
    plist=dofunc(flist,proc)
    return plist
        


def fillWithMean(data:pd.DataFrame,meandata:pd.DataFrame): 
    """
    使用列均值(非nan行的均值)填充含有nan的列
    data中必须全为number列
    meandata为用于求mean的data 列必须与data一致
    """
    #以0填充nan
    mdata=data.copy()
    #将k列的0填充均值 均值为非nan行均值
    meanlist=[]
    for k in data:
        mean=meandata[k].mean()
        if mean is np.nan:
            mdata[k]=mdata[k].fillna(value=0)
            meanlist.append(0)
        else:
            mdata[k]=mdata[k].fillna(value=mean)
            meanlist.append(mean)
    return mdata,meanlist


def fillWithZero(data:pd.DataFrame):
    return data.fillna(value=0)


def labelit(data:pd.DataFrame,clfid:int):
    """
    给data加上label列 值为clfid 列名为class
    """
    ret=data.copy()
    ret["class"]=clfid
    return ret

from imblearn import under_sampling as us
from imblearn import over_sampling as ov
def ensure_balance(data:np.ndarray,label:np.ndarray,pre_random_simple=False):
    """
    对data和label进行重采样保证平衡
    """
    #判断 维度转换
    rawshape=None
    if len(data.shape)!=2:        
        rawshape=data.shape
        data=data.reshape((len(data),-1))
    #随机重复
    if pre_random_simple:
        rsimp=ov.RandomOverSampler()
        data,label=rsimp.fit_sample(data,label)
    #近邻
    simp=ov.ADASYN(n_neighbors=5)
    #simp=us.NearMiss(n_jobs=4)
    rdata,rlabel=simp.fit_sample(data,label)
    if rawshape is not None:
        rdata=rdata.reshape(rawshape)
    return rdata,rlabel

def ensure_balance_random(data:np.ndarray,label:np.ndarray,pre_random_simple=False):
    """
    对data和label进行重采样保证平衡
    """
    #判断 维度转换
    rawshape=None
    if len(data.shape)!=2:        
        rawshape=data.shape
        data=data.reshape((len(data),-1))
    rsimp=ov.RandomOverSampler()
    rdata,rlabel=rsimp.fit_sample(data,label)
    if rawshape is not None:
        rdata=rdata.reshape(rawshape)
    return rdata,rlabel

def ensure_balance_filelist(flist:np.ndarray,label:np.ndarray):
    """
    对data和label进行重采样保证平衡
    对少的进行随机过采样
    """
    #随机重复
    flist=flist.reshape([-1,1])
    rsimp=ov.RandomOverSampler()
    rdata,rlabel=rsimp.fit_sample(flist,label)
    rdata=rdata.reshape((-1,))
    #混合
    rdata,rlabel=shuffle_data(rdata,rlabel)
    return rdata,rlabel



from sklearn.preprocessing import StandardScaler
def scale(data):
    """
    归一化处理
    """
    sd=StandardScaler()
    return sd.fit_transform(data)

def shuffle_data(u_adata:np.ndarray,u_alabel:np.ndarray):
    """
    根据data和label进行重采样
    """
    assert len(u_adata)==len(u_alabel)
    idxs=list(range(len(u_adata)))
    idxs=shuffle(idxs)
    u_adata=u_adata[idxs]
    u_alabel=u_alabel[idxs]
    return u_adata,u_alabel

def gen_resimple(data:np.ndarray,label:np.ndarray,pre_random_simple=False):
    """
    通用重采样
    """
    return shuffle_data(*ensure_balance(data,label,pre_random_simple=pre_random_simple))




