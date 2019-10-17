#导入各种需要的包#
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize


#定义所需要拟合的带参数的一般函数类型#
def fmax(x,a,b,c):
    return a*np.sin(x*np.pi/6+b)+c
'''
def func(x, a, b, c):
    return a * np.exp(-b * x) + c'''
def ekc(x,a,b1,b2,u):
    return np.exp(a+u+b1*np.log(x)+b2*(np.log(x)**2))

#输入数据#
# x=np.arange(1,13,1)
# x1=np.arange(1,13,0.01)
#第1、2个参数为坐标范围的起始点和终止点，第3个参数为最小刻度#
#这里的x和y就是实际数据的量一定要一样，但是拟合的曲线就不一定啦#
# ymax=np.array([17, 19, 21, 28, 33, 38, 37, 37, 31, 23, 19, 18 ])
'''
np.arange(a,b,c)其实返回的也是一个数组
np.arange(1,3)
返回array([1, 2])
'''
xy=np.array([[566742.88,6847612.15],
[623023.66,6954432.72],
[679279.49,7161750.54],
[737610.54,7353226.82],
[803625.55,7110953.89],
[873148.75,6996609.97]])
xy=xy/100
x=xy[:,0]
y=xy[:,1]
x1=np.arange(min(x),max(x),100)
print(x1)

print(x)
print(y)

# fita,fitb=optimize.curve_fit(fmax,x,y,[1,1,1])

fita,fitb=optimize.curve_fit(ekc,x,y,[0,1,1,0])
#最后的数组是对所求函数除x外参数的大小限制#
'''
参数分别为函数一般形式、横坐标范围、纵坐标范围、
返回两个数组，第一个是定义的函数中除x外各个参数的值，第二个是协方差
'''
print(fita)
plt.scatter(x,y)
#画出原来实际数据的图形#
plt.plot(x1,fmax(x1,fita[0],fita[1],fita[2]))
#画出拟合后获得曲线的图形#
plt.show()