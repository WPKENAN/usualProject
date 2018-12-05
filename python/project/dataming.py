import numpy as np
def kaf(mc):
    sumItems=np.sum(mc);
    alphaMilk=(mc[0]+mc[2])/sumItems;
    alphaCoff=(mc[0]+mc[1])/sumItems;

    value=[(mc[0]-alphaMilk*alphaCoff*sumItems)**2/(alphaMilk*alphaCoff*sumItems),
           (mc[1]-(1-alphaMilk)*alphaCoff*sumItems)**2/((1-alphaMilk)*alphaCoff*sumItems),
           (mc[2]-alphaMilk*(1-alphaCoff)*sumItems)**2/(alphaMilk*(1-alphaCoff)*sumItems),
           (mc[3]-(1-alphaMilk)*(1-alphaCoff)*sumItems)**2/((1-alphaMilk)*(1-alphaCoff)*sumItems)]
    return value

def liftDegree(mc):
    sumItems = np.sum(mc);
    alphaMilk = (mc[0] + mc[2]) / sumItems;
    alphaCoff = (mc[0] + mc[1]) / sumItems;
    alphaMilkCoff=mc[0]/sumItems;

    return alphaMilkCoff/(alphaMilk*alphaCoff)

def totalConfidence(mc):
    sumItems = np.sum(mc);
    alphaMilk = (mc[0] + mc[2]) / sumItems;
    alphaCoff = (mc[0] + mc[1]) / sumItems;
    alphaMilkCoff = mc[0] / sumItems;

    return alphaMilkCoff/max(alphaMilk,alphaCoff);

def maxConfidence(mc):
    sumItems = np.sum(mc);
    alphaMilk = (mc[0] + mc[2]) / sumItems;
    alphaCoff = (mc[0] + mc[1]) / sumItems;
    alphaMilkCoff = mc[0] / sumItems;

    return alphaMilkCoff / min(alphaMilk, alphaCoff);

def kulc(mc):
    sumItems = np.sum(mc);
    alphaMilk = (mc[0] + mc[2]) / sumItems;
    alphaCoff = (mc[0] + mc[1]) / sumItems;
    alphaMilkCoff = mc[0] / sumItems;

    return 1/2*(alphaMilkCoff/alphaMilk+alphaMilkCoff/alphaCoff)

def cosine(mc):
    sumItems = np.sum(mc);
    alphaMilk = (mc[0] + mc[2]) / sumItems;
    alphaCoff = (mc[0] + mc[1]) / sumItems;
    alphaMilkCoff = mc[0] / sumItems;
    return alphaMilkCoff/(alphaMilk*alphaCoff)**0.5

def func_api(mc=[0,0,0,0],func='all'):
    matrix = [];

    if func=='all':
        for i in range(len(mc)):
            matrix.append([np.sum(kaf(mc[i])),liftDegree(mc[i]),totalConfidence(mc[i]),\
                           maxConfidence(mc[i]),kulc(mc[i]),cosine(mc[i])]);
    elif func=='kaf':
        for i in range(len(mc)):
            matrix.append([np.sum(kaf(mc[i]))]);
    elif func=='liftDegree':
        for i in range(len(mc)):
            matrix.append([liftDegree(mc[i])]);
    elif func=='totalConfidence':
        for i in range(len(mc)):
            matrix.append([totalConfidence(mc[i])]);
    elif func=='maxConfidence':
        for i in range(len(mc)):
            matrix.append([maxConfidence(mc[i])]);
    elif func=='kulc':
        for i in range(len(mc)):
            matrix.append([kulc(mc[i])]);
    elif func=='consine':
        for i in range(len(mc)):
            matrix.append([cosine(mc[i])]);
    else:
        return -1;

    return matrix;

if __name__ == '__main__':
    mc = [];
    mc.append([10000, 1000, 1000, 100000]);#m_c nm_c m_nc nm_nc
    mc.append([10000, 1000, 1000, 100]);
    mc.append([100, 1000, 1000, 100000]);
    mc.append([1000, 1000, 1000, 100000]);
    mc.append([1000, 100, 10000, 100000]);
    mc.append([1000, 10, 100000, 100000]);

    print(["mileANDcoffee","NOTmilkANDcoffee","milkNOTcoffee","NOTmileNOTcoffee"])
    for i in range(len(mc)):
        print(mc[i])

    func='all'
    matrix=func_api(mc,func);
    np.set_printoptions(formatter={'float':'{:10.3f}'.format});
    # np.set_printoptions(precision=2,suppress=True)
    if func=='all':
        print(["kaf",'liftDegree','totalConfidence','maxConfidence','kulc','consine'])
    else:
        print([func])
    print(np.array(matrix))
