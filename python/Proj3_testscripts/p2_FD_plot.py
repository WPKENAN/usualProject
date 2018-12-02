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
    x =     

    #add code to compute 1st order ffd, bfd, cfd
    ffd=
    bfd=
    cfd=

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
    x =     

    #add code to compute 2nd order ffd, bfd, cfd
    ffd  = 
    bfd  = 
    cfd  = 

    #add code to call FD_plot() for the 2nd order FD


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
    x =     

    #add code to compute 3rd order ffd, bfd, cfd
    ffd  = 
    bfd  = 
    cfd  = 

    #add code to call FD_plot() for the 3rd order FD


    return (ffd, cfd, bfd)



def FD_plot(x, h, ffd, cfd, bfd, fderivative=None, FD_order=None, filename=None):

    if fderivative != None:  
        fd  = fderivative(x);   maxfd = max(abs(fd))
        plt.plot(x, fd,  'r-', lw=0.8, label="exact " +FD_order+ " deriv.")
        print('\nmax err between FDs and the exact {} order derivative when h={}:'.format(FD_order,h))
        print('\t  max(fd - ffd)={}'.format(max(abs(ffd-fd))))
        print('\t  max(fd - bfd)={}'.format(max(abs(bfd-fd))))
        print('\t  max(fd - cfd)={}'.format(max(abs(cfd-fd))))
        print('\t  exact max(fd)={}'.format(maxfd)) 
        if h<=0.01:
            tol = 0.01*max(maxfd,1)
            if (max(abs(cfd-fd))> 2*tol or max(abs(bfd-fd))>10*tol or max(abs(ffd-fd))>10*tol): 
                print('{0} Error in your {1} order FD code, need debugging {0}\n\n\n'
                      .format(10*'*', FD_order))


    #add code below to plot ffd, bfd, cfd with proper legends title etc




    if filename!=None: plt.savefig(filename+'_'+FD_order+'_'+str(h)+'.png')
    plt.show()



def FD_tests():

    #input below the first function in the project PDF using lambda
    f1 = lambda x: 
    #compute derivatives f1', f1'', f1''' manually and list them below as f1der, f1der2, f1der3 (use lambda)
    f1der =   
    f1der2= 
    f1der3= 
    x = [a for a in np.linspace(0, np.pi, 400)]  #intentionally set x to be a list
    for h in [0.5, 0.05, 0.001]:
        FD_1st_order(f1, x, h, fder=f1der, filename='function1')
        #add code below to plot the 2nd and 3rd order FDs, using same filename='function1' as above

        

    f2 = lambda x:  x/(1 + np.exp(-x))
    #compute derivatives f2', f2'' manually and list them below as f2der, f2der2 (use lambda)
    f2der = 
    f2der2= 
    #analytic 3rd derivative is quite complicated to derive, you can use the following one
    f2der3= lambda x: np.exp(x)*(np.exp(2*x)*(x-3)-4*np.exp(x)*x+x+3)/(np.exp(x)+1)**4  
    x = np.arange(-15, 15, 0.01)
    for h in [0.5, 0.2, 1e-2]:
        FD_1st_order(f2, x, h, fder=f2der, filename='swish')
        #add code below to plot the 2nd and 3rd order FDs, using same filename='swish' as above



#===============================================================
if __name__=='__main__':

    FD_tests()
