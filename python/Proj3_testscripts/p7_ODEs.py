## 
## name: 
## email: 

#--------------------------------------------------------------------
#study the demo_ODEs.py code to solve this problem.
#--------------------------------------------------------------------
#

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import  quad, odeint

from ODEs import *   #import the self-coded ODE solvers


#--------------------------------------------------------------------
# Forced Van der Pol oscillator with sinusoidal forcing 
#  u'' - mu * (1-u**2) *u' + u = A * sin(omega * t)
# with initial conditons to u(0)=0, u'(0)=0
A=0.5;  mu=0.8;  omega=np.pi/4










#--------------------------------------------------------------------
#Solve a 3rd oder nonlinear ODE
#   y''' + 2y*y'' - (y')**2 = x/(y+5)  -1  on [0, 10]
# with initial conditions  y(0)=0,  y'(0)=0, y''(0)=1.   
#(note: This ODE is very sensitive to numbers, you should input the numbers carefully)









#====================================================================
if __name__=='__main__':  
    pass
    #call your functions defined above to solve problem 7