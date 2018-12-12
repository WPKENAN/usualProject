#
#  name:
#  email:
#

import numpy as np
import matplotlib.pyplot as plt

### import nonlinear solvers implemented for problem 1 here
from p1_nonlinear import  bisection,  newton,  quasi_newton  

SHOW = True


#---------------------------------------------------- 
def  engin(eff,  gamma,  tol=1e-12):

    #add code to define the function f(x) to be solved for the root
    f = lambda x: eff-(np.log(x)-(1-1/x))/(np.log(x)+(1-1/x)/(gamma-1))

    #add a line of code to call bisection to solve f(x)=0
    (k, root, fx) = bisection(f, 1.001, 10**6, tol=1e-14, itmax=200, SHOW=False)
    
    #add code to return the root 
    return root


def engin_simulate():

    s = []   #use this list to store roots when gamma = 1.7 
    s2= []   #use this list to store roots when gamma = 5

    EFF = np.arange(0.1, 0.81, 0.025)
    #let eff loop over the range of efficieny from 0.1 to 0.8
    for eff in EFF:
        #add code below to store the roots in s (for gamma=1.7) and s2 (for gamma=5)
        gamma1 = 1.7
        gamma2 = 5
        s_ = engin(eff,  gamma1,  tol=1e-5)
        s2_ = engin(eff,  gamma2,  tol=1e-5)
        s.append(s_)
        s2.append(s2_)

    #add code below to print out the data stored in s and s2 using the format in project PDF
    for i in range(len(EFF)):
        print("efficiency={0:.3f},   T2/T1(1.7)={1},   T2/T1(5)={2}".format(EFF[i],s[i],s2[i]))

    #add code below to plot the data to generate a plot similar to the one in project PDF
    #remember to add legends, title, labels etc (you should use both plt.plot() and plt.semilogy())
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.plot(EFF,s,'r--',marker='o',label='r=1.7')
    ax1.plot(EFF,s2,'b--',marker='+',label='r=5')
    ax1.set_title("T2/T1 values needed for certain efficiency")
    ax1.set_ylabel("T2/T1")
    ax1.legend()
    ax2 = fig.add_subplot(212)
    ax2.plot(EFF,s,'r--',marker='o',label='r=1.7')
    ax2.plot(EFF,s2,'b--',marker='+',label='r=5')
    ax2.set_title("clear semilogy plot of the above figure")
    ax2.set_ylabel("T2/T1")
    ax2.set_xlabel("Engine efficiency")
    ax2.semilogy()
    ax2.legend()
    plt.tight_layout()


    #plt.tight_layout()  #uncomment this line if your plot has 'label overlapping title' issue 
    plt.savefig('engin_eff_vs_T.png')
    plt.show()





#=====================================================
if __name__=='__main__':

    engin_simulate()
