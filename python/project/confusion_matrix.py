from __future__ import division
import  numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def plotCM(classes, matrix, savname):
    """classes: a list of class names"""
    # Normalize by row
    # matrix = matrix.astype(np.float)
    # linesum = matrix.sum(1)
    # linesum = np.dot(linesum.reshape(-1, 1), np.ones((1, matrix.shape[1])))
    # matrix /= linesum
    # plot
    # plt.switch_backend('agg')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(matrix)
    fig.colorbar(cax)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[0]):
            ax.text(i, j, str('%.2f' % (matrix[i, j])), va='center', ha='center',fontsize=25,color='r')
    ax.set_xticklabels([''] + classes, rotation=90,fontsize=25)
    ax.set_yticklabels([''] + classes,fontsize=25)
    # save
    # plt.savefig(savname)
    plt.show()

if __name__=='__main__':
    classes=['false','true'];
    matrix=np.array([[9552,10],[12,104]])
    plotCM(classes,matrix,"")