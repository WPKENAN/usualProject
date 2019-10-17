import pandas as pd
import numpy as np
from pgmpy.models import BayesianModel
from pgmpy.estimators import BayesianEstimator
import networkx as nx
from matplotlib import pyplot as plt
from pgmpy.estimators import MaximumLikelihoodEstimator, BayesianEstimator
import seaborn as sns
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
interval=0.2
def showBN(model,save=False):
    '''传入BayesianModel对象，调用graphviz绘制结构图，jupyter中可直接显示'''
    from graphviz import Digraph
    node_attr = dict(
     style='filled',
     shape='box',
     align='left',
     fontsize='12',
     ranksep='0.1',
     height='0.2'
    )
    dot = Digraph(node_attr=node_attr, graph_attr=dict(size="12,12"))
    seen = set()
    edges=model.edges()
    for a,b in edges:
        dot.edge(a,b)
    if save:
        dot.view(cleanup=True)
    return dot
def bestBays(data):
    out = open('log.txt', 'w')
    from pgmpy.estimators import HillClimbSearch
    from pgmpy.estimators import BdeuScore, K2Score, BicScore
    print(data.columns)
    trainnums = 2000
    test = data.ix[:10, :]
    data = data.ix[:, :]

    hc = HillClimbSearch(data, scoring_method=K2Score(data))
    best_model = hc.estimate()
    print(showBN(best_model))
    # nx.draw(best_model, with_labels=True)
    # plt.plot()
    # plt.show()

    model=best_model

    model.fit(data, estimator=BayesianEstimator)
    for cpd in model.get_cpds():
        print("CPD of {variable}:".format(variable=cpd.variable))
        out.write('CPD of {variable}:\n'.format(variable=cpd.variable))
        print(cpd)
        out.write('{}\n'.format(cpd))
    print(showBN(model))

    print("*" * 20)
    out.write("*" * 20 + "\n")
    # print(model.get_independencies())
    out.write("{}\n".format(model.get_independencies()))



    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    nx.draw(model, with_labels=True)
    plt.plot()
    # plt.show()
    plt.savefig('baynet.png')

    predict_data = test.drop(columns=['BOYUEGrade'], axis=1)

    y_pred = model.predict(predict_data)
    # print(y_pred['BOYUEGrade']==data['BOYUEGrade'])
    # print(y_pred['BOYUEGrade'] == data['BOYUEGrade'])
    print((y_pred['BOYUEGrade'] == test['BOYUEGrade']).sum() / len(test))  # 测试集精度

def normalModel(data):
    plt.figure(figsize=(10, 10))
    sns.heatmap(data.corr(), annot=True)
    # plt.show()
    plt.savefig("相关性.png")
    plt.close()
    labels=['内饰grade','性价比grade','造型grade', '驾乘感受grade','油耗grade','BOYUEGrade']
    p=labels[:4]
    p.append(labels[-1])

    print(p)
    data = data[p]
    trainnums=6100
    test = data.ix[:10, :]
    data = data.ix[11:trainnums,:]


    out = open('log.txt', 'w')
    print(data.shape)
    out.write("{}\n".format(data.shape))
    print(data.info())

    label = data.columns

    # das

    print(label)
    out.write('{}\n'.format(label))

    bayesGraph = []
    for i in range(len(label) - 1):
        bayesGraph.append((label[i], label[-1]))
    print(bayesGraph)

    out.write('{}\n'.format(bayesGraph))

    model = BayesianModel(bayesGraph)

    model.fit(data, estimator=BayesianEstimator)
    for cpd in model.get_cpds():
        print("CPD of {variable}:".format(variable=cpd.variable))
        out.write('CPD of {variable}:\n'.format(variable=cpd.variable))
        print(cpd)
        out.write('{}\n'.format(cpd))
    print(showBN(model))

    print("*" * 20)
    out.write("*" * 20 + "\n")
    # print(model.get_independencies())
    # out.write("{}\n".format(model.get_independencies()))

    print("start")
    from pylab import mpl


    nx.draw(model, with_labels=True)
    # plt.plot()
    # plt.show()
    plt.savefig('baynet.png')
    plt.close()


    # test=data.ix[:100,:]
    predict_data = test.drop(columns=['BOYUEGrade'], axis=1)
    y_pred = model.predict(predict_data)
    # y_pred['BOYUEGrade']=5;
    print(y_pred)
    # print(y_pred['BOYUEGrade']==data['BOYUEGrade'])
    # print(y_pred['BOYUEGrade'] == data['BOYUEGrade'])
    print((y_pred['BOYUEGrade'] == test['BOYUEGrade']).sum() / len(test))

if __name__=="__main__":
    data=pd.read_excel('BOYUE.xlsx')-1
    # data=data[['动力grade','发动机grade','内饰grade','BOYUEGrade']]-1

    bestBays(data)
    # normalModel(data)




    # plt.show()

