#
#  name:
#  email:
#

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import  quad, odeint, ode

#--------------------------------------------------------------------
def euler(f, y0, x0, xend, h):   #do not modify this function  
    """ solving y'=f(y, x),  where x is 1-dimensional, but y can be multi-dimensional.
        f is the function that returns f(y,x) = dy/dx.
        (x0, y0) is the initial condition y(x0)= y0, y0 can be either a scalar or a vector.
        xend is the end value of x,  h is the increment of x .
        the solution is returned in y as an np.array, its associated x is also returned (for plotting)
    """
    x = np.arange(x0, xend, h);   
    x = np.append(x, xend)  #add xend to x so that the last point in x is exactly xend
    nsteps = len(x);  
    try:   
        n = len(y0)
    except:
        n = 1

    y = np.zeros((nsteps,n))  #make y an array directly (to avoid issue with shallow-copy list)
    y[0,:] = np.array(y0)     #first row in y corresponds to the initial(s)
    for i in range(1, nsteps):
        y[i,:] = y[i-1,:] + h*f(y[i-1,:], x[i-1])
    return  y, x

    
#--------------------------------------------------------------------
def new_RK4(F, y0, x0, xend, h):
    """ solve y' = F(y,x) using another form of a 4th order Runge-Kutta method, 
              where x is 1-dimensional, but y can be multi-dimensional.
        F is the function that returns F(y,x) = dy/dx.
        (x0, y0) is the initial condition y(x0)= y0, y0 can be either a scalar or a vector.
        xend is the end value of x,  h is the increment of x .
        the solution is returned in y as an np.array, its associated x is also returned (for plotting)
    """
    #add code below to implement RK4 listed in handout



    


    


#--------------------------------------------------------------------
# modify this plot_solutions() function to make it complete:
# note that the calls to odeint() and euler and plotting the two solutions
# from these two solvers are already done for you.
# you only need to add two lines of code:
#   1. to call new_RK4() to get the solution,
#   2. plot this solution from you new_RK4 solver in the same figure
#
def plot_solutions(f, y0, x0, xend, h, title, filename=None):
    ''' solve y'(x) = f(y,x),  y(x0)=y0  on [x0, xend], 
        and plot the solution y(x) on [x0, xend] 
    '''
    #note Euler and odeint are done for you, no need to modify the following 4 lines
    ye, xe=euler(f, y0, x0, xend, h)
    plt.plot(xe, ye[:,0], 'b-.', label='euler (h={:.3f})'.format(h))
    yode = odeint(f, y0, xe)
    plt.plot(xe, yode[:,0], 'c-', label='scipy odeint')

    #add two lines of code below to call new_RK4() to get the solution and then plot this solution

    

    
    #no need to modify the following plotting lines within this funtion
    plt.legend(loc='best')
    plt.title(title)
    plt.ylabel('y(x)');  plt.xlabel('x')
    if filename != None:  #save the plot to the specified filename
        plt.savefig(filename+str(h)+'.png')
    plt.show()


#--------------------------------------------------------------------
if __name__=='__main__':
    #
    #add code to solve the first ODE and plot the three solutions by calling the 
    #plot_solutions() above.
    #(your RK4 and Euler solutions should become more accurate with decreasing h)
    #

    #for the 1st ODE, y is a scalar valued function:
    #add code to define the fuction f(y,x) that is needed to solve the 1st ODE;
    #add code to define the initial condition as well
    
    f= lambda y, x:
    x0 =
    xend=
    y0=

    #no need to modify the following two lines
    for h in [0.5,  0.05,  0.01]:  
        plot_solutions(f, y0, x0, xend, h, title="Solve $y'(x)=x - y*sin(x), \ y(-5)=2$", filename='ode1st')


    #
    #for the 2nd ODE, y should be made a vector (since the original ODE is 2nd order)
    #
    #add code to define the fuction f(y,x) that is needed to solve the ODE;
    #add code to define the initial conditions as well
    #
    f2= lambda y, x: 
    x0 =
    xend=
    y0= 

    #no need to modify code below: 
    for h in [0.3, 0.1, 0.01]:
        #(if your RK4 code is done right, RK4 solution should be quite accurate for all h)
        plot_solutions(f2, y0, x0, xend, h, title="Solve $y''(x)+y'e^{y}=\sin(xy), \ y(-5)=y'(-5)=-1$",
                       filename='ode2nd')





