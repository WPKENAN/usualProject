# 
# module containing the Euler's method and the 4th order Runge-Kutta Method for solving ODEs
#     y'= f(y, x),  where y is a function of x
#
# coded by Yunkai Zhou  (yzhou@smu.edu)
# Fall 2016, SMU, Dallas
#
import numpy as np

#--------------------------------------------------------------------
# Note:  For the user defined function f(y, x) = y' ,
# make sure the returned value should be of np.array type
# (this is because a list type would have trouble being multiplied by a scalar, 
# while in ODE solves one would frequently need operations such as h*f(y,x) )
#--------------------------------------------------------------------
#
def euler(f, y0, x0, xend, h): 
    """ Usage:  y, x = euler_ndim(f, y0, x0, xend, h).
        this implements the forward euler method for solving y'=f(y,x), where x is 1-dimensional, 
        y is the unknow function of dimension n>1:  y = (y_0, y_1, ..., y_(n-1)). 
        F is the function that returns the array F(y,x) = dy/dx = (y_0, y_1, ..., y_(n-1))'.

        (x0, y0) is the initial condition y(x0)= y0 ,
        xend is the end value of x,  h is the increment of x .
       
       The solution is returned in y as a 2-dim np.array, the i-th column of y, y[:,i], contains 
       the ith component y_i of y;  the associated x of y is also returned. 
    """
    x = np.arange(x0, xend, h);   
    x = np.append(x, xend)  #add xend to x so that the last point in x is exactly xend
    nsteps = len(x);  
    try:   #using try-except, we can handle both 1-dim and higher-dim ODEs in one function
        n = len(y0)
    except:
        n = 1

    y = np.zeros((nsteps,n))  #make y an array directly (to avoid issue with shallow-copy list)
    y[0,:] = np.array(y0)
    for i in range(1, nsteps):
        y[i,:] = y[i-1,:] + h*f(y[i-1,:], x[i-1])
    return  y, x


#--------------------------------------------------------------------
def run_kut4(F, y, x, h):  #this is an internal subroutine used inside RK4() and RK4_ndim()
    K0 = h*F(y, x)
    K1 = h*F(y + K0/2.0, x + h/2.0)
    K2 = h*F(y + K1/2.0, x + h/2.0)
    K3 = h*F(y + K2, x + h)
    return (K0 + 2.0*K1 + 2.0*K2 + K3)/6.0    

#--------------------------------------------------------------------
def RK4(F, y0, x0, xend, h):
    """ Usage:  y, x = RK4_ndim(F, y0, x0, xend, h).
        solve y' = F(y,x) using the 4th order Runge-Kutta method,  where x is 1-dimensional, 
        y is the unknow function of dimension n>1:  y = (y_0, y_1, ..., y_(n-1)). 
        F is the function that returns the array F(y,x) = dy/dx = (y_0, y_1, ..., y_(n-1))'.

        (x0, y0) is the initial condition y(x0)= y0 ,
        xend is the end value of x,  h is the increment of x .
       
       The solution is returned in y as a 2-dim np.array, the i-th column of y, y[:,i], contains 
       the ith component y_i of y;  the associated x of y is also returned. 
    """
    x = np.arange(x0, xend, h)
    x = np.append(x, xend)  #add xend to x so that the last point in x is exactly xend
    nsteps = len(x)
    try:
        n = len(y0)
    except:
        n = 1
    y = np.zeros((nsteps, n))  #make y an array directly (to avoid issue with shallow-copy list)
    y[0,:] = np.array(y0)
    for i in range(1, nsteps):
        y[i,:] = y[i-1,:] + run_kut4(F, y[i-1,:], x[i-1], h)
    return  y, x
