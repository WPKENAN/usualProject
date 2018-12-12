#
# name:
# email:
#

import numpy as np
import matplotlib.pyplot as plt
#note: your code should not import other modules (all the math functions such as sin() etc are in numpy)



##
## do not change the function recursive_trape(f, a, b, fa=None, fb=None, tol=1e-10)
##
def recursive_trape(f, a, b, fa=None, fb=None, tol=1e-10):
    '''recursive implementation of the trapezoidal rule to compute the
       integral of f(x) for x in [a, b].
       this function returns the integral_value and the number_of_panels_used .

       Note: this recursive implementation reuses previous function evaluations, so it is economical.
 
       To use this function for evaluating integral of f(x) on [a, b], you only need to call it as

         recursive_trape(f, a, b)  #certainly you need to add variables to receive its returned values
    '''

    if fa==None : fa=f(a)
    if fb==None : fb=f(b)
    h = (b-a)/2
    Iold = (fa + fb)*h
    fmid = f(a+h)
    Inew = Iold/2 + fmid*h

    reltol = max(abs(Iold), abs(Inew), 0.01)*max(0.5e-10, tol)
    if abs(h) <= 1e-15  or abs(Inew-Iold)<= reltol:
        return Inew, 2
    else:
        left_integral,  left_panel  = recursive_trape(f, a, a+h, fa, fmid, tol)
        right_integral, right_panel = recursive_trape(f, a+h, b, fmid, fb, tol)
        return  left_integral +right_integral,  left_panel +right_panel


##
## add code below to call recursive_trape() to solve the two questions specified in the handout.
## there are several different ways to code, you are free to design your code (interfaces etc),
## as long as you can get answers of the y(x)'s being asked for, and can produce the required plot.
##

def  solve_ode_via_quad(f, xList, x0, y0):

    yx = np.zeros(len(xList))
    for i, x in enumerate(xList):
        yx[i] = y0 + recursive_trape(f, x0, x)[0]
        # print(recursive_trape(f, x0, x)[0])
        print('y({}) = {}'.format(x, yx[i]))
    
    return yx


def plot_quad_ode(f, xvect, x0, y0, filename=None):
    yx = np.zeros(len(xvect))
    yx[0]=y0;  i=0
    for x in xvect[1:]:
        i += 1
        ##the following line works, but it does not reuse previously computed integral (thus slow)
        #yx[i]= y0 + recursive_trape(f, x0, x)[0]

        ##the following line is far more efficient, it reuses previously computed integral 
        ##that has been saved in yx[i-1],  
        ##only need to integrate on [xvect[i-1],  xvect[i]] and add that to yx[i-1]
        yx[i] = yx[i-1] + recursive_trape(f, xvect[i-1], x)[0]  

        #printout some intermediate steps
        if i%10==0: print('y({}) = {}'.format(x, yx[i]))
        
    plt.plot(xvect, yx, 'r-', label='solution y(x)')
    plt.legend(loc='best')
    plt.xlabel('x');   plt.ylabel('y(x)');
    plt.title('plot of the ODE solution obtained via integration')    
    if filename !=None:  plt.savefig(filename)
    plt.show()        

    
if __name__=='__main__':

    f = lambda t:  np.sin(2*t)/t
    
    xList = [0.2, 0.5, 0.7, 1.1, 5, 10, 19, 20]
    yList = solve_ode_via_quad(f, xList, x0=0.1, y0=5)
    print(yList)
    
    
    x = np.linspace(0.1, 10, 100) 
    plot_quad_ode(f, x,  x0=0.1, y0=5, filename='quad_ode.png')


    
