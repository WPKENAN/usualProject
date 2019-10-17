import pandas as pd
from pgmpy.models import BayesianModel
from pgmpy.estimators import BayesianEstimator


def buildModel():
    model = BayesianModel([('Age', 'Survived'), ('Sex', 'Survived'), ('Fare', 'Pclass'), ('Pclass', 'Survived'), ('Cabin', 'Survived')])

    testModel = BayesianModel([('Fare', 'Pclass')])

    dot=showBN(model)
    print(dot)

    from pgmpy.factors.discrete import TabularCPD
    # 构建cpd表
    cpd_d = TabularCPD(variable='Fare', variable_card=2, values=[[0.6, 0.4]])
    my_cpd = TabularCPD(variable='Pclass', variable_card=3,
                        values=[[0.65, 0.3], [0.30, 0.6], [0.05, 0.1]],
                        evidence=['Fare'], evidence_card=[2])
    # 填cpd表
    model.add_cpds(cpd_d,my_cpd)

    # 执行检查（可选，用于检查cpd是否填错）
    model.check_model()




    return model


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



if __name__=="__main__":
    data=pd.read_excel('BOYUE.xlsx')
    print(data.shape)
    buildModel()
