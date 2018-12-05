def dx(f,x):
    return abs(0-f(x));

def f(x):
    return 6 * x ** 5 - 5 * x ** 4 - 4 * x ** 3 + 3 * x ** 2

def df(x):
    return 30 * x ** 4 - 20 * x ** 3 - 12 * x ** 2 + 6 * x

def newtonsMethod(f, df, x0, e):
    delta=dx(f,x0);
    while delta>e:
        x0=x0-f(x0)/df(x0);
        delta=dx(f,x0);
        print('Root is at:%lf'%(x0));
        print('f(x) at root is:%f'%(f(x0)))
    print('Root is at:%lf' % (x0));
    print('f(x) at root is:%f' % (f(x0)))

x0s=[0,0.5,1]
#牛顿法
for x0 in x0s:
    print("seed start at:%lf"%(x0))
    newtonsMethod(f,df,x0,1e-10)
    print("==============================")

#二分法
print("================二分法==============")
def bisection(left,right,e):
    middle=(left+right)/2;
    count=0;
    while dx(f,middle)>e:
        middle=(left+right)/2;
        if f(left)*f(middle)<=0:
            right=middle;
        else:
            left=middle;
        count=count+1;
        print('Root is at:%lf' % (middle));
        print('f(x) at root is:%f' % (f(middle)))
    return count,middle;
left=0;
right=1;
e=1e-10;
count,middle=bisection(left,right,e);
print("迭代%d次得到的根是%f" %(count,middle))

from scipy.optimize import leastsq

leastsq()
