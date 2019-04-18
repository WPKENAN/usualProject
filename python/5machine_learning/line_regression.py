# coding=utf-8
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


def run_plt():
    plt.figure()
    plt.title('Price-Size')
    plt.xlabel('Size')
    plt.ylabel('Price')
    plt.axis([0, 25, 0, 25])
    plt.grid(True)
    return plt

x = [[6], [8], [10], [14], [18]]
y = [[7], [9], [13], [17.5], [18]]
model = LinearRegression()
model.fit(x, y)

plt = run_plt()
x2 = [[0], [10], [14], [25]]
y2 = model.predict(x2)
plt.plot(x, y, '.')  # 最后一个参数指定绘图类型，'.' 为点
plt.plot(x2, y2, '-')  # 最后一个参数指定绘图类型，'.' 为点
plt.show()