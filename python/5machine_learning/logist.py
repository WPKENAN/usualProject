import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split

# 加载diabetes数据集
iris = datasets.load_iris()
# print(iris.keys())
# print(iris.data)
# print(iris.data.shape)# 数据集有150个样本，4个特征

iris_X = iris.data[:,:2] # 只取前两个特征
print(iris_X)
print(iris_X.shape)

# 划分数据集，后20个数据划分为测试集，其它的为训练集
iris_X_train = iris_X[:-20]
iris_X_test = iris_X[-20:]
iris_y_train = iris.target[:-20]
iris_y_test = iris.target[-20:]
print('train:', iris_X_train.shape, iris_y_train.shape)
print('test: ', iris_X_test.shape, iris_y_test.shape)

# 构建线性回归模型
logreg = linear_model.LogisticRegression()
# 使用训练数据训练模型
logreg.fit(iris_X_train, iris_y_train)
# 预测
iris_y_pred = logreg.predict(iris_X_test)
print('pred: ', iris_y_pred.shape)

# 回归系数
print('Coefficients: \n', logreg.coef_)

h = .02
x_min, x_max = iris_X_train[:, 0].min() - .5, iris_X_train[:, 0].max() + .5
y_min, y_max = iris_X_train[:, 1].min() - .5, iris_X_train[:, 1].max() + .5
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
Z = logreg.predict(np.c_[xx.ravel(), yy.ravel()])

Z = Z.reshape(xx.shape)
plt.figure(1, figsize=(4, 3))
plt.pcolormesh(xx, yy, Z, cmap=plt.cm.Paired)

plt.scatter(iris_X_train[:, 0], iris_X_train[:, 1], c=iris_y_train, edgecolors='k', cmap=plt.cm.Paired)
plt.xlabel('Sepal length')
plt.ylabel('Sepal width')

plt.xticks(())
plt.yticks(())

plt.show()