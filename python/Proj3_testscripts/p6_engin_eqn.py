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
    f = lambda x: 

    #add a line of code to call bisection to solve f(x)=0

    
    #add code to return the root 



def engin_simulate():

    s = []   #use this list to store roots when gamma = 1.7 
    s2= []   #use this list to store roots when gamma = 5

    EFF = np.arange(0.1, 0.81, 0.025)
    #let eff loop over the range of efficieny from 0.1 to 0.8
    for eff in EFF:
        #add code below to store the roots in s (for gamma=1.7) and s2 (for gamma=5)




    #add code below to print out the data stored in s and s2 using the format in project PDF




    #add code below to plot the data to generate a plot similar to the one in project PDF
    #remember to add legends, title, labels etc (you should use both plt.plot() and plt.semilogy())




    #plt.tight_layout()  #uncomment this line if your plot has 'label overlapping title' issue 
    plt.savefig('engin_eff_vs_T.png')
    plt.show()





#=====================================================
if __name__=='__main__':

    engin_simulate()
