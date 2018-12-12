#
# module for solving ODEs
#

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import  quad, odeint, ode

#--------------------------------------------------------------------
#do not modify this euler() function
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
#
def RK3(F, y0, x0, xend, h):
    """ solve y' = F(y,x) using the 3rd order Runge-Kutta method, both x and y are 1-dimension.
        F is the function that returns F(y,x) = dy/dx.
        (x0, y0) is the initial condition y(x0)= y0 ,
        xend is the end value of x,  h is the increment of x .
        the solution is returned in y as an np.array, its associated x is also returned for plotting
    """
    #add code below to implement RK3 using the formula specified in the handout



    
    

#--------------------------------------------------------------------
#do not modify this plot_solutions() function, but you need to 
#read it and understand what it does
#
def plot_solutions(f, y0, x0, xend, h, title, filename=None):
    ''' solve y'(x) = f(y,x),  y(x0)=y0  on [x0, xend], 
        and plot the solution y(x) on [x0, xend].

        if filename is passed in, the plot will be saved to a file named filename+str(h)+'.png'
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

    #add code below to solve the first ODE and plot the solution by calling plot_solutions(),
    #using different h in [0.5,  0.05,  0.01]
    #(solutions should become more accurate with decreasing h)
    #
<<<<<<< p4_ode.py
    #remember to pass to plot_solutions() suitable title and filename so that title will
    #be printed, and that plots will be saved to filename+str(h)+'.png' as specified
=======
    #remember to input to plot_solutions() suitable title and filename so that title same
    #as those in the handoout will be printed, and that the plot will be saved
>>>>>>> 1.2
    #(use filename='ode1h' for the first ODE)

    #note for this problem f is only a function of one variable, while the solver requires
    #f to be a function of two variables, you can use the simple trick discussed in class.
    #(if you did not miss class when this was discussed, you would know what to do here)
    
    f= lambda          #finish this line to define f

    x0 = 0.1;  xend=20;  y0=5;     #initial conditions and interval are given for you here
    for h in [0.5,  0.05,  0.01]:
        #loop over h, add a line below to call plot_solutions()
        



<<<<<<< p4_ode.py
         
    #add code to solve the second ODE and plot the solution by calling plot_solutions(),
    #using different h specified in the handout.
=======
        
    #     
    #add code below to solve the second ODE and plot the solution by calling plot_solutions(),
    #using different h in [0.2, 0.01, 0.001]
>>>>>>> 1.2
    #(solutions should become more accurate with decreasing h)
<<<<<<< p4_ode.py
    #remember to pass to plot_solutions() suitable title and filename so that title will
    #be printed, and the plots will be saved
=======
    # 
    #remember to input to plot_solutions() suitable title and filename so that title same
    #as those in the handoout will be printed, and that the plot will be saved
>>>>>>> 1.2
    #(use filename='ode2h' for the second ODE)
    # 
    #it is similar to the above, just apply to the second ODE


