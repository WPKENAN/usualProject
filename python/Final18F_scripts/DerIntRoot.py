#
# name:
# email:
#
# Note you are not allowed to change the any of the function interface defined below,
# you should call these functions by using propers inputs to solve the problems 
# specified in the handout. 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import  quad
from nonlinear_eqn import *
from quadra import *


#the input x can be a vector, in that case your returned function values should also be a vector.
#this should be easily done by numpy array.
def func(x, n=100):
    ''' compute the function f(x,n) = 1 + sin(x) + sin(2x)/2 + sin(3x)/3 + ... + sin(nx)/n 
        (since n is given, essentially this is a single variable function)
        return the function evaluated at x (note, the input x can be a vector)
    '''
    result=[];
    # print(x)
    for xi in x:
        fn = 1;
        for i in range(1,n+1):
            fn=fn+np.sin(i*xi)/i;
        result.append(fn);
    return result;

def func1(x, n=100):
    ''' compute the function f(x,n) = 1 + sin(x) + sin(2x)/2 + sin(3x)/3 + ... + sin(nx)/n
        (since n is given, essentially this is a single variable function)
        return the function evaluated at x (note, the input x can be a vector)
    '''

    fn = 1;
    for i in range(1,n+1):
        fn=fn+np.sin(i*x)/i;

    return fn;


    
def fder(x, n=100):
    ''' compute the derivative of f(x,n) = 1 + sin(x) + sin(2x)/2 + sin(3x)/3 + ... + sin(nx)/n,
        you differentiate term by term (easy via basic calculus here), then sum them up.
        return the derivative evaluated at x (note, the input x can be a vector)
    '''
    result = [];
    # print(x)
    for xi in x:
        fn = 0;
        for i in range(1, n + 1):
            fn = fn + np.cos(i*xi);
        result.append(fn);
    return result;

def fder1(x, n=100):
    ''' compute the derivative of f(x,n) = 1 + sin(x) + sin(2x)/2 + sin(3x)/3 + ... + sin(nx)/n,
        you differentiate term by term (easy via basic calculus here), then sum them up.
        return the derivative evaluated at x (note, the input x can be a vector)
    '''


    fn = 0;
    for i in range(1, n + 1):
        fn = fn + np.cos(i*x);
    return fn;

    
def plot_funcs(func, nset=[2, 5, 8, 10], a=-5, b=5):
    ''' plot the func(x,n) on [a,b] for n in nset for x on [a, b], save plot to fourier.png '''
    for ni in nset:
        result=func(np.linspace(a,b,1001),ni);
        plt.plot(np.linspace(a,b,1001),result,label='n={}'.format(ni));
    plt.plot(np.linspace(a,b,1001),np.linspace(a,b,1001)*0,'--')
    plt.legend()
    plt.title("Plot of f(x,n)");
    plt.ylabel("f(x,n)")
    plt.xlabel("x")
    plt.savefig("fourier.png")
    plt.show()



    

def plot_funcs_der(func, fder, n=8, a=-5, b=5):
    ''' plot the derivative of func(x,n) on [a,b] for a fixed n;
        call fder() for exact derivative, plot this line with linestyle 'r--' and lw=4;  
        use numerical derivative via CFD with the two h values specifed in hand out, 
            you can plot these two lines using any linestyle but do not increase lw for them;
        save plot to fourier_der.png.
    '''

    # input below the first function in the project PDF using lambda
    f1 = lambda x: func1(x,n);
    # compute derivatives f1', f1'', f1''' manually and list them below as f1der, f1der2, f1der3 (use lambda)
    f1der = lambda x: fder1(x,n);

    x = [p for p in np.linspace(a, b, 1001)]  # intentionally set x to be a list
    der = fder(x, n);
    print(der)
    plt.plot(x, der,label="exact: n={}".format(n));
    for h in [0.2, 0.001]:
        cfd=FD_1st_order(f1, x, h, fder=f1der, filename='function1')
        plt.plot(x,cfd,'--',label="CFD: n={},h={}".format(n,h));
    plt.legend();
    plt.xlabel("x");
    plt.ylabel("f(x,15)");
    plt.title("first order derivative of f(x,15")
    plt.show()
    plt.savefig("fourier_der.png")

def FD_1st_order(f, x, h=1e-4, fder=None, filename=None):
    '''compute 1st order derivative of f(x) using FFD, CFD, BFD.
       tasks:
       (1) output f'(x) in a tuple named (ffd, cfd, bfd), where ffd, cfd, bfd store the
           f'(x) obtained by FFD, CFD, and BFD;
       (2) call FD_plot() to do the plotting:
           (2.1) when exact f'(x) is passed as input via fder, need to pass it on so that
                 a curve of exact dervative will be plotted in addition to FD curves
           (2.2) when filename is passed as input, need to pass it on so that the plot will
                 be saved to a png file using a modification of this filename
    '''
    #add code to make sure elementwise operations such as x+h and x-h are valid for x
    x = np.array(x)

    #add code to compute 1st order ffd, bfd, cfd
    cfd= [(f(i+h)-f(i-h))/(2*h) for i in x]

    #add code to call FD_plot(), for the 1st order, this is done for you below
    # FD_plot(x, h, cfd,fderivative=fder, FD_order='1st', filename=filename)


    return cfd


def FD_plot(x, h, cfd,fderivative=None, FD_order=None, filename=None):
    pass

def find_roots(func, n=10, tol=1e-12):
    """ find all roots of f(x)=func(x,n) on [-10, 10], you should call the bisection() or ridder() 
        in the provided file nonlinear_eqn.py. 
        (you may set SHOW=True to let the solver show results at each step.)
        
        generate a list [ (x1, f(x1)), (x2, f(x2), ..., (xk, f(xk)) ], where x1, x2, ..., xk are 
        all the roots of f(x) in [-10, 10] ordered in increasing order, 
        printout this list, and
        return this list.
    """
    #first define a lambda function to be passed to an equation solver


    


    


def fn_integral(f, a, b, npanel=1000, tol=1e-10):
    """ find integral of f(x) on [a, b], 
        use simpson-1/3 rule with npanels, save the integral value in fsimpson,
        use adaptive-trapezoid rule with accuracy tol, save the integral value in ftrap;
        (note1: the n and tol required are different from the default, and you 
         are not allowed to change the interface above;
        (note2: you can used the solvers provided in quadra.py; or you call your own code, just
         copy and paste your own code from your 3rd project into this file.)
        print out the integral values;  
        print out also the difference between the integrals obtained from the two solvers.
        return a tuple (fsimpson, ftrap,  fsimpson -ftrap) 
    """


    




    

if __name__=='__main__':
    """ call the functions above to achieve the tasks specified in the handout. 
        (since you are not allowed to change any of the function interfaces above, 
         you need to specify all the correct input variables in order to finish exactly 
         what the handout asks you to do.)
         most of this part only need you to pass proper inputs to functions 
    """
    x=np.linspace(-10,10,100);
    # call plot_funcs() to plot the functions  
    plot_funcs(func,[2,10,20,100],-10,10)
    plot_funcs_der(func,fder,n=15,a=-2,b=2)


    
    # call plot_funcs_der() to plot the derivative 
    # plot_funcs_der(   )


    
    # call find_roots() to find all the roots of func(x, 20) on [-10, 10]
    # roots_froots = find_roots( )
    # don't change the following two lines, it only checks if your output is correct
    # for (i, rf) in enumerate(roots_froots):
    #     print('root{} = {:.14f},  f = {:.14e}'.format(i, rf[0], rf[1]))

        
    
    # define a lambda functins, call fn_integral() to find the integral of this function
    # f1 = lambda x:
    # fn_integral(   )


