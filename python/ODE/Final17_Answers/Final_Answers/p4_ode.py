#
# module for solving ODEs
#

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import  quad, odeint, ode

#--------------------------------------------------------------------
def euler(f, y0, x0, xend, h):    
    """ solving y'=f(y, x),  where x and y are both 1-dimensionsional, by the forward euler method.
        f is the function that returns f(y,x) = dy/dx.
        (x0, y0) is the initial condition y(x0)= y0 ,
        xend is the end value of x,  h is the increment of x .
        the solution is returned in y as an np.array, its associated x is also returned (for plotting)
    """
    x = np.arange(x0, xend, h)
    x = np.append(x, xend)  #add xend to x so that the last point in x is exactly xend
    nsteps = len(x);    
    y = np.zeros(nsteps);     y[0] = y0
    for i in range(1, nsteps):
        y[i] = y[i-1] + h*f(y[i-1], x[i-1])

    return  y, x

#--------------------------------------------------------------------
def run_kut3(F, y, x, h):
    K0 = h*F(y, x)
    K1 = h*F(y + K0/2.0, x + h/2.0)
    K2 = h*F(y + 3*K1/2.0, x + 3*h/4.0)
    return (2.0*K0 + 3.0*K1 + 4.0*K2)/9.0    


def RK3(F, y0, x0, xend, h):
    """ solve y' = F(y,x) using the 3rd order Runge-Kutta method, both x and y are 1-dimension.
        F is the function that returns F(y,x) = dy/dx.
        (x0, y0) is the initial condition y(x0)= y0 ,
        xend is the end value of x,  h is the increment of x .
        the solution is returned in y as an np.array, its associated x is also returned for plotting
    """
    x = np.arange(x0, xend, h)
    x = np.append(x, xend)  #add xend to x so that the last point in x is exactly xend
    nsteps = len(x);    
    y = np.zeros(nsteps);     y[0] = y0
    for i in range(1, nsteps):
        y[i] = y[i-1] + run_kut3(F, y[i-1], x[i-1], h)

    return  y, x
  


#--------------------------------------------------------------------
#do not modify this plot_solutions() function, but you need to 
#read it and understand what it does
#
def plot_solutions(f, y0, x0, xend, h, title, filename=None):
    ''' solve y'(x) = f(y,x),  y(x0)=y0  on [x0, xend], 
        and plot the solution y(x) on [x0, xend] 
    '''
    
    ye, xe=euler(f, y0, x0, xend, h)
    yRK, xRK= RK3(f, y0, x0, xend, h)
    yode = odeint(f, y0, xRK)
    plt.plot(xRK, yode, 'c-', label='scipy odeint')
    plt.plot(xe, ye, 'b-.', label='euler (h={:.3f})'.format(h))
    plt.plot(xRK, yRK, 'r:', lw=3, label='RK3   (h={:.3f})'.format(h))
    plt.legend()
    plt.title(title)
    plt.ylabel('y(x)');  plt.xlabel('x')

    if filename != None:  #save the plot to the specified filename
        plt.savefig(filename+str(h)+'.png')

    plt.show()


#--------------------------------------------------------------------
if __name__=='__main__':

    #add code to solve the first ODE and plot the solution by calling plot_solutions(),
    #using different h in [0.5,  0.05,  0.01]
    #(solutions should become more accurate with decreasing h)
    #
    #remember to pass to plot_solutions() suitable title and filename so that title will
    #be printed, the plot will be saved
    #(use filename='ode1h' for the first ODE)

    #note for this problem f is only a function of one variable, while the solver requires
    #f to be a function of two variables, you should use the simple trick discussed in class.
    
    #note the ODE solvers take f(y,x), so y has to be before x, although y is not used 
    f= lambda y, x: np.sin(2*x)/x   #this is the same as f= lambda y, t: np.sin(2*t)/t 

    x0 = 0.1;  xend=20;  y0=5;
    for h in [0.5,  0.05,  0.01]:  
        plot_solutions(f, y0, x0, xend, h, title="Solving $y'(x)=sin(2x)/x, \ y(0.1)=5$", filename='ode1')


         
    #add code to solve the second ODE and plot the solution by calling plot_solutions(),
    #using different h as specified in the handout.
    #(solutions should become more accurate with decreasing h)
    #remember to pass to plot_solutions() suitable title and filename so that title will
    #be printed, the plot will be saved
    #(use filename='ode2h' for the second ODE)
     
    f2= lambda y, t:  np.cos(t*y)  #this is the same as f2= lambda y, x:  np.cos(x*y)
    x0 = -3;  xend= 5;  y0 = 8    
    for h in [0.2, 0.05, 0.01]:
        plot_solutions(f2, y0, x0, xend, h, title="Solving $y'(x)=\cos(x*y), \ y(-3)=8$", filename='ode2')





