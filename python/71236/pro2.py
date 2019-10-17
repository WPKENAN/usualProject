from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
import networkx as nx
from matplotlib import pyplot as plt
# %matplotlib inline

# 构建一个网络模型
model = BayesianModel([('D', 'G'),   # 一条有向边，D ---> G
                       ('I', 'G'),   # I ---> G
                       ('G', 'L'),   # G ---> L
                       ('I', 'S')])  # I ---> S

# 设置CPD参数

# variable='D'：节点名为 D，
# variable_card=2：有两种可能的情况，
# values=[[0.6, 0.4]]：概率分别是0.6和0.4
cpd_d = TabularCPD(variable='D', variable_card=2, values=[[0.6, 0.4]])

# variable='I'：节点名为I
# variable_card=2：有两种可能的情况，
# values=[[0.7, 0.3]]：概率分别是0.7和0.3
cpd_i = TabularCPD(variable='I', variable_card=2, values=[[0.7, 0.3]])

# In pgmpy the colums are the evidences and rows are the states of the variable.
# 在设置G节点时，结构与上图显示的有点不同，这里，列：evidence 行：state，设置参数时，结构如下表：
#    +---------+---------+---------+---------+---------+
#    | diff    | intel_0 | intel_0 | intel_1 | intel_1 |
#    +---------+---------+---------+---------+---------+
#    | intel   | diff_0  | diff_1  | diff_0  | diff_1  |
#    +---------+---------+---------+---------+---------+
#    | grade_0 | 0.3     | 0.05    | 0.9     | 0.5     |
#    +---------+---------+---------+---------+---------+
#    | grade_1 | 0.4     | 0.25    | 0.08    | 0.3     |
#    +---------+---------+---------+---------+---------+
#    | grade_2 | 0.3     | 0.7     | 0.02    | 0.2     |
#    +---------+---------+---------+---------+---------+

# variable='G'：节点名为 G，
# variable_card=3：有两种可能的情况，
# values=[[0.3, 0.05, 0.9,  0.5],
#        [0.4, 0.25, 0.08, 0.3],
#        [0.3, 0.7,  0.02, 0.2]],：针对不同的父节点的情况组合，具有不同的概率分布，如上表
# evidence=['I', 'D']：父节点为 I 和 D，即 I 和 D 指向 G
# evidence_card=[2, 2]：父节点分别有两种可能的情况
cpd_g = TabularCPD(variable='G', variable_card=3,
                   values=[[0.3, 0.05, 0.9,  0.5],
                           [0.4, 0.25, 0.08, 0.3],
                           [0.3, 0.7,  0.02, 0.2]],
                  evidence=['I', 'D'],
                  evidence_card=[2, 2])

cpd_l = TabularCPD(variable='L', variable_card=2,
                   values=[[0.1, 0.4, 0.99],
                           [0.9, 0.6, 0.01]],
                   evidence=['G'],
                   evidence_card=[3])

cpd_s = TabularCPD(variable='S', variable_card=2,
                   values=[[0.95, 0.2],
                           [0.05, 0.8]],
                   evidence=['I'],
                   evidence_card=[2])

# Associating the CPDs with the network
# 将概率分布表加入到贝叶斯网络中
model.add_cpds(cpd_d, cpd_i, cpd_g, cpd_l, cpd_s)

# check_model checks for the network structure and CPDs and verifies that the CPDs are correctly
# defined and sum to 1.
# 验证模型数据的正确性（检测节点是否定义，概率和是否为1）
model.check_model()

# 绘制网络结构图，并附上概率分布表
nx.draw(model,
        with_labels=True,
        node_size=1000,
        font_weight='bold',
        node_color='y',
        pos={"L": [4, 3], "G": [4, 5], "S": [8, 5], "D": [2, 7], "I": [6, 7]})
plt.text(2, 7, model.get_cpds("D"), fontsize=10, color='b')
plt.text(5, 6, model.get_cpds("I"), fontsize=10, color='b')
plt.text(1, 4, model.get_cpds("G"), fontsize=10, color='b')
plt.text(4.2, 2, model.get_cpds("L"), fontsize=10, color='b')
plt.text(7, 3.4, model.get_cpds("S"), fontsize=10, color='b')
plt.title('test')
plt.show()
