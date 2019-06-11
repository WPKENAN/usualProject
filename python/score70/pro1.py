#数据读取、分割、标准化处理、SVM回归模型

#第一步：读取波士顿房价数据
from sklearn.datasets import load_boston
boston = load_boston()
print(boston.DESCR)
#从输出结果来看，该数据共有506条波士顿房价的数据，每条数据包括对指定房屋的13项数值型特征和目标房价
#此外，该数据中没有缺失的属性/特征值，更加方便了后续的分析

#第二步：波士顿房价数据分割
from sklearn.cross_validation import train_test_split
import numpy as np
X_train,X_test,y_train,y_test = train_test_split(boston.data,boston.target,test_size=0.25,random_state=33)
#分析回归目标值的差异
print('The max target value is ',np.max(boston.target))
print('The min target value is ',np.min(boston.target))
print('The average target value is ',np.mean(boston.target))

#第三步：训练数据和测试数据标准化处理
from sklearn.preprocessing import StandardScaler
#分别初始化对特征值和目标值的标准化器
ss_X = StandardScaler()
ss_y = StandardScaler()
#训练数据都是数值型，所以要标准化处理
X_train = ss_X.fit_transform(X_train)
X_test = ss_X.transform(X_test)
#目标数据（房价预测值）也是数值型，所以也要标准化处理
#说明一下：fit_transform与transform都要求操作2D数据，而此时的y_train与y_test都是1D的，因此需要调用reshape(-1,1)，例如：[1,2,3]变成[[1],[2],[3]]
y_train = ss_y.fit_transform(y_train.reshape(-1,1))
y_test = ss_y.transform(y_test.reshape(-1,1))

#第四步：使用三种不同核函数配置的支持向量机回归模型进行训练，并且分别对测试数据进行预测
#从sklearn.svm中导入支持向量机回归模型SVR
from sklearn.svm import SVR
#1.使用线性核函数配置的支持向量机进行回归训练并预测
linear_svr = SVR(kernel='linear')
linear_svr.fit(X_train,y_train)
linear_svr_y_predict = linear_svr.predict(X_test)
#2.使用多项式核函数配置的支持向量机进行回归训练并预测
poly_svr = SVR(kernel='poly')
poly_svr.fit(X_train,y_train)
poly_svr_y_predict = poly_svr.predict(X_test)
#3.使用径向基核函数配置的支持向量机进行回归训练并预测
rbf_svr = SVR(kernel='rbf')
rbf_svr.fit(X_train,y_train)
rbf_svr_y_predict = rbf_svr.predict(X_test)

#第五步：对三种核函数配置下的支持向量机回归模型在相同测试集下进行性能评估
#使用R-squared、MSE、MAE指标评估
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error
#1.线性核函数配置的SVR
print('R-squared value of linear SVR is',linear_svr.score(X_test,y_test))
print('the MSE of linear SVR is',mean_squared_error(ss_y.inverse_transform(y_test),ss_y.inverse_transform(linear_svr_y_predict)))
print('the MAE of linear SVR is',mean_absolute_error(ss_y.inverse_transform(y_test),ss_y.inverse_transform(linear_svr_y_predict)))
#2.多项式核函数配置的SVR
print('R-squared value of Poly SVR is',poly_svr.score(X_test,y_test))
print('the MSE of Poly SVR is',mean_squared_error(ss_y.inverse_transform(y_test),ss_y.inverse_transform(poly_svr_y_predict)))
print('the MAE of Poly SVR is',mean_absolute_error(ss_y.inverse_transform(y_test),ss_y.inverse_transform(poly_svr_y_predict)))
#3.径向基核函数配置的SVR
print('R-squared value of RBF SVR is',rbf_svr.score(X_test,y_test))
print('the MSE of RBF SVR is',mean_squared_error(ss_y.inverse_transform(y_test),ss_y.inverse_transform(rbf_svr_y_predict)))
print('the MAE of RBF SVR is',mean_absolute_error(ss_y.inverse_transform(y_test),ss_y.inverse_transform(rbf_svr_y_predict)))


#在不同配置下支持向量基模型在相同数据上表现出不同的性能，核函数是一种非常有用的特征映射技巧
#将低维度不好区分的特征，映射到高纬度空间以便可区分
#在实际应用时，可采用不同核函数来寻找最佳的预测模型