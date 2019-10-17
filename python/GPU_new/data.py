
from dataloader import *



truedir="/home/cva/data/true"
falsedir="/home/cva/data/false"
def setdatadir(dirn):
    global truedir
    global falsedir
    truedir=f"{dirn}/true"
    falsedir=f"{dirn}/false"
#机械
# truedir="/save/data/true"
# falsedir="/save/data/false"

#小批量测试开关
# truedir="./data/true"
# falsedir="./data/false"

nshape=(841,25)
starts=(0,0)
def read_rawdata():
    """
    读取数据 返回dataframe
    为原始数据 仅填充了nan 删除了第一列（时间）
    """
    global truedir
    global falsedir
    truedata=readall_items(truedir)
    falsedata=readall_items(falsedir)
    #预处理
    #生成原始全部数据表 用于计算mean值
    alldata=pd.concat([truedata,falsedata])
    #填充nan
    truedata,_=fillWithMean(truedata,alldata)
    falsedata,_=fillWithMean(falsedata,alldata)
    #打标签
    truedata=labelit(truedata,1)
    falsedata=labelit(falsedata,0)
    alldata=pd.concat([truedata,falsedata])
    #混淆
    alldata=shuffle(alldata)
    #返回 true false all
    return truedata,falsedata,alldata




def readdata_matrix(normalize=True):
    """
    读取数据 返回numpy数组 
    得到concat axis=0 的标准数据集
    """
    truedata,falsedata,alldata=read_rawdata()
    #提取标签
    tlabel=truedata["class"].as_matrix()
    flabel=falsedata["class"].as_matrix()
    alabel=alldata["class"].as_matrix()
    del truedata["class"]
    del falsedata["class"]
    del alldata["class"]
    #转换为numpy matrix
    tdata=truedata.as_matrix()
    fdata=falsedata.as_matrix()
    adata=alldata.as_matrix()
    #归一化处理
    if normalize:
        tdata=scale(tdata)
        fdata=scale(fdata)
        adata=scale(adata)
    #测试输出 前后为 数据 标签 内部为 正 负 重采样的全部样本 没有重采样的全部样本
    return (tdata,fdata,adata),(tlabel,flabel,alabel)


def validation(trues,falses):
    allimages=[]
    allimages.extend(trues)
    allimages.extend(falses)
    #校验维度错误
    shapes=[i.shape for i in allimages]
    rori=[shapes[0]]
    testv=[i==rori for i in shapes]
    isok=True
    for i,s in enumerate(shapes):
        if s not in rori:
            isok=False
            print(f"第{i}个样本拥有新的shape:{s}")
            rori.append(s)
    print(f"是否全部拥有相同shape:{isok}")
    print(f"样本所有的shape列表:{rori}")
    return isok
def filterData(imgs):
    global nshape
    #标准shape
    ret=[i for i in imgs if i.shape==tuple(nshape)]
    return ret

needscale=False
def images_preproc(images,dofilter=True):
    global starts
    global nshape
    # print(f"starts:{starts} nshape:{nshape}")
    if needscale:
        images=[scale(fillWithZero(pd.DataFrame(i)).as_matrix()) for i in images]
    else:
        images=[fillWithZero(pd.DataFrame(i)).as_matrix() for i in images]
    #剪切
    images=[i[starts[0]:starts[0]+nshape[0],starts[1]:starts[1]+nshape[1]] for i in images]
    if dofilter:images=filterData(images)
    return images
 
def readdata_images_raw(trueimages,falseimages):
    #allimages=np.concatenate([trueimages,falseimages],axis=0)
    # #计算图片每一列的mean值
    # cmeans=np.mean(np.concatenate(allimages,axis=0),axis=0)
    #对nan用0 并标准化（可能不需要标准化）
    trueimages=images_preproc(trueimages)
    falseimages=images_preproc(falseimages)
    #减去列均值
    #由于全是一样的行数 化为ndarray
    trueimages,falseimages=np.array(trueimages,dtype="float32"),np.array(falseimages,dtype="float32")
    #生成标签
    tlabel=np.ones(shape=(len(trueimages,)))
    flabel=np.zeros(shape=(len(falseimages,)))
    #生成全体数据集
    adata=np.concatenate([trueimages,falseimages],axis=0)
    alabel=np.concatenate([tlabel,flabel],axis=0)
    #混淆
    adata,alabel=shuffle_data(adata,alabel)
    #返回
    return (trueimages,falseimages,adata),(tlabel,flabel,alabel)

def readdata_images(truemaxsize=-1,falsemaxsize=-1):
    """
    把数据集当图片读取出来
    从默认目录
    """
    global truedir
    global falsedir
    trueimages=readall_image(truedir,maxsize=truemaxsize)
    falseimages=readall_image(falsedir,maxsize=falsemaxsize)
    return readdata_images_raw(trueimages,falseimages)

def readdata_images_list(trueflist,falseflist):
    """完文件名列表 从默认路径合成"""
    global truedir
    global falsedir
    trueflist=[os.path.join(truedir,i) for i in trueflist]
    falseflist=[os.path.join(falsedir,i) for i in falseflist]
    trueimages=readall_image_list(trueflist)
    falseimages=readall_image_list(falseflist)
    return readdata_images_raw(trueimages,falseimages)


#纯粹读取函数 文件名要求完整路径
def readflist_to_images(flist,dofilter=True):
    """单纯的文件到图片列表"""
    images=readall_image_list(flist)
    images=images_preproc(images,dofilter=dofilter)
    return images


#辅助大数据量处理函数
def batch_dirgenerator(maxsize):
    global truedir
    global falsedir
    tflist=os.listdir(truedir)
    fflist=os.listdir(falsedir)
    yield from batch_flistgenerator(tflist,fflist,maxsize)


def batch_flistgenerator(tflist,fflist,maxsize):
    tstart=0
    fstart=0
    print(f"flen:{len(fflist)} tlen:{len(tflist)}")
    while max(tstart,fstart)<max(len(tflist),len(fflist)):
        if fstart>=len(fflist):
            fstart=0
        if tstart>=len(tflist):
            tstart=0
        yield tflist[tstart:tstart+maxsize],fflist[fstart:fstart+maxsize]
        fstart+=maxsize
        tstart+=maxsize
        print(f"fstart:{fstart} tstart:{tstart}")

def getflens():
    """获取文件列表长度"""
    global truedir
    global falsedir
    tflist=os.listdir(truedir)
    fflist=os.listdir(falsedir)
    return len(tflist),len(fflist)

def getflist():
    global truedir
    global falsedir
    tflist=os.listdir(truedir)
    fflist=os.listdir(falsedir)
    return tflist,fflist

def getfalldatas():
    """获取文件名列表和标签"""
    global truedir
    global falsedir
    tflist,fflist=getflist()
    tlabel=np.ones(shape=(len(tflist,)))
    flabel=np.zeros(shape=(len(fflist),))
    #合成完整文件路径
    tflist=[os.path.join(truedir,i) for i in tflist]
    fflist=[os.path.join(falsedir,i) for i in fflist]
    #合并
    alabel=np.concatenate([tlabel,flabel],axis=0)
    aflist=np.array(tflist+fflist)
    aflist,alabel=shuffle_data(aflist,alabel)
    return aflist,alabel


def filterDataAndLabel(imgs,label):
    """依据data的shape对data和label进行协同过滤 返回img,label"""
    #标准shape
    global nshape
    ret=[(imgs[i],label[i]) for i in range(len(imgs)) if imgs[i].shape==tuple(nshape)]
    ret=list(zip(*ret))
    return ret


# 数据batch生成器部分
def provider(flist,label,batch_count,batch_size,mqueue):
    for i in range(batch_count):
        start=i*batch_size
        end=start+batch_size
        #剪切枚举
        bdata,blabel=flist[start:end],label[start:end]
        #同步长度
        minlen=min(len(bdata),len(blabel))
        bdata=bdata[:minlen]
        blabel=blabel[:minlen]
        #这里考虑使用指针形式以适配长度不等的情况
        #将bdata读取
        bdata=readflist_to_images(bdata,dofilter=False)
        #过滤
        bdata,blabel=filterDataAndLabel(bdata,blabel)
        #转换为numpy矩阵
        bdata=np.array(bdata,dtype="float32")
        blabel=np.array(blabel,dtype="float32")
        #加入队列
        mqueue.put((bdata,blabel))
        
#读取器部分
def generator(flist,label,batch_count,batch_size,mqueue):
    #消费者
    for i in range(batch_count):
        bdata,blabel=mqueue.get()
        # print(f"nshape:{nshape}shape:{bdata.shape}")
        yield bdata,blabel


from multiprocessing import Process,Queue
batchqueue=None
def datagenerator(flist,label,batch_size,queue_size=100000):
    """数据枚举器 文件名列表为完整路径"""
    assert len(flist)==len(label)
    #每个epoch进行混合增加随机性
    flist,label=shuffle_data(flist,label)
    flen=len(flist)
    count=flen//batch_size
    if count*batch_size<flen:
        count+=1
    #考虑增加提供者队列
    #队列机制
    global batchqueue
    if batchqueue is None:
        batchqueue=Queue(maxsize=queue_size//batch_size)
    prov=Process(target=provider,args=(flist,label,count,batch_size,batchqueue))
    prov.start()
    yield from generator(flist,label,count,batch_size,batchqueue)
    #释放进程资源
    prov.join()

#对接
def set_buffersize(m):
    set_maxfx(m)
    

    


def dataflow(*args,**kwargs):
    while True:
        yield from datagenerator(*args,**kwargs)



def random_cut(lst,maxsize):
    """随机不重复采样"""
    idxs=list(range(len(lst)))
    import random as rd
    rd.shuffle(idxs)
    idxs=idxs[:maxsize]
    if type(lst)==list:
        return [lst[i] for i in idxs]
    else:return lst[idxs]
    
def random_cut_datalabel(data,label,maxsize):
    lst=list(zip(data,label))
    clst=random_cut(lst,maxsize)
    rdata,rlabel=list(zip(*clst))
    return rdata,rlabel