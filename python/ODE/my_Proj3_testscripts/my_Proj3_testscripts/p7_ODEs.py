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
def VdPol(y, t):  
    return np.array([y[1],mu*(1-y[0]**2)*y[1]-y[0]+A*np.sin(omega*t)])

def VdPol_osci():
    y0 = np.array([0,  0.0])
    tend =50
    t = np.linspace(0, tend, 300); 
    ## call the scipy ode solver 'odeint()' for comparision (since no exact solution is known)
    sol = odeint(VdPol, y0, t)

    ## call self-coded RK4()  solver 
    solRK, x = RK4(VdPol, y0, 0, tend, 0.1) 

    ## call self-coded euler()  solver 
    soleu, xeu = euler(VdPol, y0, 0, tend, 0.01)  

    plt.plot(t, sol[:, 0], 'b--',marker='+',lw=0.5, label='odeint')
    plt.plot(x, solRK[:, 0], 'r--', label='RK4 h=0.1)')
    plt.plot(xeu, soleu[:, 0], 'y', label='euler h=0.01)')
    plt.title("Sinusoidal forcingForced Van der Pol oscillator");
    plt.legend(loc='best');  plt.xlabel('Time t');  plt.ylabel('Amplitude u(t)');   
    plt.savefig('ODE_Van_der_Pol_oscillator.png');  plt.show()






#--------------------------------------------------------------------
#Solve a 3rd oder nonlinear ODE
#   y''' + 2y*y'' - (y')**2 = x/(y+5)  -1  on [0, 10]
# with initial conditions  y(0)=0,  y'(0)=0, y''(0)=1.   
#(note: This ODE is very sensitive to numbers, you should input the numbers carefully)
def Third_oder(y, t):  
    return np.array([y[1],y[2],t/(y[0]+5)-1-2*y[0]*y[2]+(y[1])**2])

def Third_oder_solve():
    y0 = np.array([0.0,  0.0,  1.0])
    tend =12
    t = np.linspace(0, tend, 200); 
    ## call the scipy ode solver 'odeint()' for comparision (since no exact solution is known)
    sol = odeint(Third_oder, y0, t)

    ## call self-coded RK4()  solver 
    solRK, x = RK4(Third_oder, y0, 0, tend, 0.04) 

    ## call self-coded euler()  solver 
    soleu, xeu = euler(Third_oder, y0, 0, tend, 0.01)  #if h is increased, euler would have sizeable error 
    
    # call self-coded euler()  solver 
    soleu2, xeu2 = euler(Third_oder, y0, 0, tend, 0.001)  #if h is increased, euler would have sizeable error 

    plt.plot(t, sol[:, 0], 'b--',marker='+',lw=0.5, label='odeint')
    plt.plot(x, solRK[:, 0], 'r--', label='RK4 h=0.04)')
    plt.plot(xeu, soleu[:, 0], 'c', label='euler h=0.01)')
    plt.plot(xeu2, soleu2[:, 0], 'y', label='euler h=0.001)')
    plt.title("Solution of a 3rd oder nonliear ODE");
    plt.legend(loc='best');  plt.xlabel('Time t');  plt.ylabel('y(t)');   #plt.grid()
    plt.savefig('ODE_3rd_oder_nonliear.png');  plt.show()


#====================================================================
if __name__=='__main__':  

    #call your functions defined above to solve problem 7
	VdPol_osci()
	Third_oder_solve()