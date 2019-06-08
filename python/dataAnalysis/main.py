import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df=ts.get_hist_data('600415',start='2016-04-01',end='2017-06-18')
print(df)
# 所有的结果汇图
# plt.figure()
df.plot()
plt.legend()
# 只将stock最高值进行汇图
plt.figure()
df.high.plot()
plt.legend()
# # 指定绘图的四个量，并指定线条颜色
plt.figure()
with pd.plotting.plot_params.use('x_compat', True):
    df.open.plot(color='g')
    df.close.plot(color='y')
    df.high.plot(color='r')
    df.low.plot(color='b')
    plt.legend()
# 指定绘图的长宽尺度及背景网格
plt.figure()
with pd.plotting.plot_params.use('x_compat', True):
    df.high.plot(color='r',figsize=(10,4),grid='on')
    df.low.plot(color='b',figsize=(10,4),grid='on')
plt.legend()
plt.show()