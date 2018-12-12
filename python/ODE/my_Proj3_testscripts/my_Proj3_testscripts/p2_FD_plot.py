#
# name:
# email: 
#

import numpy as np
import matplotlib.pylab as plt


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
    ffd= [(f(i+h)-f(i))/h for i in x]
    bfd= [(-f(i-h)+f(i))/h for i in x]
    cfd= [(f(i+h)-f(i-h))/(2*h) for i in x]

    #add code to call FD_plot(), for the 1st order, this is done for you below
    FD_plot(x, h, ffd, cfd, bfd, fderivative=fder, FD_order='1st', filename=filename)


    return (ffd, cfd, bfd)


def FD_2nd_order(f, x, h=1e-4, fder2=None, filename=None):
    '''compute 2nd order derivative of f(x) using FFD, CFD, BFD. 
       tasks: 
       (1) output f''(x) in a tuple named (ffd, cfd, bfd), where ffd, cfd, bfd store the 
           f''(x) obtained by FFD, CFD, and BFD;
       (2) call FD_plot() to do the plotting:
           (2.1) when exact f''(x) is passed as input via fder2, need to pass it on so that
                 a curve of exact dervative will be plotted in addition to FD curves
           (2.2) when filename is passed as input, need to pass it on so that the plot will 
                 be saved to a png file using a modification of this filename          

    '''
    #add code to make sure elementwise operations such as x+h and x-h are valid for x
    x = np.array(x)    

    #add code to compute 2nd order ffd, bfd, cfd
    ffd  = [(f(i+2*h)-2*f(i+h)+f(i))/(h**2) for i in x]
    bfd  = [(f(i)-2*f(i-h)+f(i-2*h))/(h**2) for i in x]
    cfd  = [(f(i+h)-2*f(i)+f(i-h))/(h**2) for i in x]

    #add code to call FD_plot() for the 2nd order FD
    FD_plot(x, h, ffd, cfd, bfd, fderivative=fder2, FD_order='2nd', filename=filename)

    return (ffd, cfd, bfd)


def FD_3rd_order(f, x, h=1e-4, fder3=None, filename=None):
    """compute 3rd order derivative of f(x) using FFD, CFD, BFD. 
       tasks: 
       (1) output f'''(x) in a tuple named (ffd, cfd, bfd), where ffd, cfd, bfd store the 
           f'''(x) obtained by FFD, CFD, and BFD;
       (2) call FD_plot() to do the plotting:
           (2.1) when exact f'''(x) is passed as input via fder2, need to pass it on so that
                 a curve of exact dervative will be plotted in addition to FD curves
           (2.2) when filename is passed as input, need to pass it on so that the plot will 
                 be saved to a png file using a modification of this filename          
    """
    #add code to make sure elementwise operations such as x+h and x-h are valid for x
    x = np.array(x)

    #add code to compute 3rd order ffd, bfd, cfd
    ffd  = [(-f(i)+3*f(i+h)-3*f(i+2*h)+f(i+3*h))/(h**3) for i in x]
    bfd  = [(-f(i-3*h)+3*f(i-2*h)-3*f(i-h)+f(i))/(h**3) for i in x]
    cfd  = [(-f(i-2*h)+2*f(i-h)-2*f(i+h)+f(i+2*h))/(2*h**3) for i in x]

    #add code to call FD_plot() for the 3rd order FD
    FD_plot(x, h, ffd, cfd, bfd, fderivative=fder3, FD_order='3rd', filename=filename)

    return (ffd, cfd, bfd)



def FD_plot(x, h, ffd, cfd, bfd, fderivative=None, FD_order=None, filename=None):

    if fderivative != None:  
        fd  = fderivative(x);   maxfd = max(abs(fd))
        plt.plot(x, fd,  'r-', lw=0.8, label="exact " +FD_order+ " deriv.")
        print('\nmax err between FDs and the exact {} order derivative when h={}:'.format(FD_order,h))
        # print('\t  max(fd - ffd)={}'.format(max(abs(ffd-fd))))
        # print('\t  max(fd - bfd)={}'.format(max(abs(bfd-fd))))
        print('\t  max(fd - cfd)={}'.format(max(abs(cfd-fd))))
        print('\t  exact max(fd)={}'.format(maxfd)) 
        if h<=0.01:
            tol = 0.01*max(maxfd,1)
            if (max(abs(cfd-fd))> 2*tol or max(abs(bfd-fd))>10*tol or max(abs(ffd-fd))>10*tol): 
                print('{0} Error in your {1} order FD code, need debugging {0}\n\n\n'
                      .format(10*'*', FD_order))


    #add code below to plot ffd, bfd, cfd with proper legends title etc
    # plt.plot(x, ffd,  'c-', lw=0.8, label="forward FD")
    plt.plot(x, cfd,  'g--', lw=0.8, label="central FD")
    # plt.plot(x, bfd,  'b--', lw=0.8, label="backward FD")
    plt.title(FD_order+' order derivative: h='+str(h))
    plt.legend()


    if filename!=None: plt.savefig(filename+'_'+FD_order+'_'+str(h)+'.png')
    plt.show()



def FD_tests():

    #input below the first function in the project PDF using lambda
    f1 = lambda x: np.cos(pow(x,2)-x)
    #compute derivatives f1', f1'', f1''' manually and list them below as f1der, f1der2, f1der3 (use lambda)
    f1der = lambda x: -(2*x-1)*np.sin(x**2-x)

    x = [a for a in np.linspace(0, np.pi, 400)]  #intentionally set x to be a list
    for h in [0.2, 0.001]:
        FD_1st_order(f1, x, h, fder=f1der, filename='function1')





#===============================================================
if __name__=='__main__':

    FD_tests()
