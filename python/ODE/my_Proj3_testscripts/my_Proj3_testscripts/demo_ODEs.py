#--------------------------------------------------------------------
# demo code on the usage of the euler() and RK4() solvers
#
# prepared by Yunkai Zhou,  F16 & S17
#--------------------------------------------------------------------
#

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import  quad, odeint

from ODEs import *   #import the self-coded ODE solvers

#--------------------------------------------------------------------
#1. solve the 1st order 1-dim logistic ODE   y'(t)= r*y*(1- y/K) where 
#   r and K are constants, with initial condition y(0)=y0.  
#   the exact solution is known to be y(t) = y0*K /(y0 + (K-y0)*exp(-r*t))
#

r=1.;  K=1000    #set two global variables 
def  yprime(y, t):
    return r*y*(1- y/K)

def  test_logistic():
    x0=0;   y0 = 15   #pick set initial condition
    hrange = np.arange(0.01, 0.8, 0.15)
    for h in hrange:  #observe that the larger h becomes, the less accurate the solution
        y, t = euler(yprime, y0, x0, 9., h)
        plt.plot(t, y, label="euler h="+str(h))

    #compare with the exact solution 
    yexact = y0*K /(y0 + (K-y0)*np.exp(-r*t))
    plt.plot(t, yexact, 'r:', lw=4, label="exact")
    plt.title("Logistic model solved by Euler with varing h")
    plt.xlabel("t"); plt.ylabel("y(t)");
    plt.legend(loc='best');  plt.savefig('ODE_logistic_euler.png');  plt.show()

    hrange2 = np.arange(0.01, 0.9, 0.2)  #RK can use larger h (with better accuracy) than euler!
    for h in hrange2:
        y, t = RK4(yprime, y0, x0, 9., h)
        plt.plot(t, y, label="RK4 h="+str(h))

    #compare with the exact solution 
    yexact = y0*K /(y0 + (K-y0)*np.exp(-r*t))
    plt.plot(t, yexact, 'r:', lw=4, label="exact")
    plt.title("Logistic model solved by Runge-Kutta with varing h")
    plt.xlabel("t"); plt.ylabel("y(t)");
    plt.legend(loc='best');  plt.savefig('ODE_logistic_RK4.png');  plt.show()


#--------------------------------------------------------------------
#2. solve the second order differential equation for the angle z of a pendulum acted on by gravity 
#   with friction and external force:  
#                                   z''(t) + b*z'(t) + c*sin(z) = e**(-t*z)
#   (this is a difficult nonlinear ODE, for which euler has to use a very small h)
#

b=0.5; c=6  #set two global variables
def pendu(y, t):  #this returns the dy/dt vector, where y = [z, z'], as mentioned in class
    return np.array([y[1],    -b*y[1] - c*np.sin(y[0]) + np.exp(-t*y[0])])  

def pendu_simu():
    #assume z(0) = pi/2, and it is initially at rest. the vector of initial conditions is
    y0 = np.array([np.pi/2,  0.0])
    tend =25
    t = np.linspace(0, tend, 300); 
    ## call the scipy ode solver 'odeint()' for comparision (since no exact solution is known)
    sol = odeint(pendu, y0, t)

    ## call self-coded RK4()  solver 
    solRK, x = RK4(pendu, y0, 0, tend, 0.01) 

    ## call self-coded euler()  solver 
    soleu, xeu = euler(pendu, y0, 0, tend, 0.002)  #if h is increased, euler would have sizeable error 

    plt.plot(t, sol[:, 0], 'r:', lw=3.5, label='z(t) by odeint')
    plt.plot(x, solRK[:, 0], 'c-', label='z(t) by RK (h=0.01)')
    plt.plot(xeu, soleu[:, 0], '--', label='z(t) by euler (h=0.002)')
    plt.title("Pendulum motion under friction and positive forcing");
    plt.legend(loc='best');  plt.xlabel('t');  plt.ylabel('Angle(t)');   #plt.grid()
    plt.savefig('ODE_pendulum.png');  plt.show()


#--------------------------------------------------------------------
#3. solve u'' = -u + u**(1/2)   with  u(0)=pi/50,  u'(0)=0
#
def fring(y, t):    #returns dy/dt,  where y=[u, u']  
    return  np.array([ y[1],    -y[0] + np.sqrt(y[0])] )

def ring_simu():
    tend = 10*np.pi
    t = np.linspace(0.0, tend, 500)
    y0 = np.array([ np.pi/50,  0. ])
    y = odeint(fring, y0, t)   #call scipy odeint() for comparison 
    fig, ax = plt.subplots()
    ax.plot(1/y[:,0]*np.cos(t), 1/y[:,0]*np.sin(t), 'r:', lw=4, label="odeint")

    # call self-coded RK4()  solver 
    yRK, xRK = RK4(fring, y0, 0, tend, 0.05)
    ax.plot(1/yRK[:,0] * np.cos(xRK), 1/yRK[:,0]*np.sin(xRK), 'g-', label="RK h=0.05" )

    ## call self-coded euler()  solver 
    yeu, xeu = euler(fring, y0, 0, tend, 0.0005)  #even with small h, euler still has sizable error
    ax.plot(1/yeu[:,0] * np.cos(xeu), 1/yeu[:,0]*np.sin(xeu), 'b-.', label="Eu h=0.0005" )
    ax.legend(loc='best');  plt.savefig('ODE_ring_phase.png');  plt.show()

    plt.plot(t, y[:,0], 'r:', lw=4, label="odeint")
    plt.plot(xRK, yRK[:,0], 'g-', label="RK h=0.05" )
    plt.plot(xeu, yeu[:,0], 'b-.', label="Eu h=0.0005" )
    plt.legend(loc='best'); plt.savefig('ODE_ring.png');  plt.show() 


#--------------------------------------------------------------------
#4. solve the 1st order 2x2 ODE system, which is the famous Predator-Prey ODE model, also known 
#   as the Lotka-Volterra equations:  
#          x' = ax - bxy;  y'= cxy - dy,    where a, b, c, d are positive constants
#   with initial conditions  x(0)=x0;  y(0)=y0
#
def dP_dt(P, t, a=.62, b=.3, c=.3, d=.25):   #returns dP/dt,  where P(t)=[x(t), y(t)] 
    return np.array([ P[0]*(a - b*P[1]),   P[1]*(c*P[0] -d) ])

def lotk_volt():
    tend=50;    ts = np.linspace(0, tend,  200)
    x0=2;  y0=1;    P0 = [x0,  y0]   #set the initial conditions

    #call scipy odeint() to solve the ODE 
    Ps = odeint(dP_dt, P0, ts) 

    Pse,  x  = euler(dP_dt, np.array(P0), 0, tend, 0.01)    #h=0.01 is fine for euler
    Pse2, x2 = euler(dP_dt, np.array(P0), 0, tend, 0.25)    #h=0.25 is too large for euler 
    PsRK, xRK =  RK4(dP_dt, np.array(P0), 0, tend, 0.25)    #h=0.25 is fine for RK4

    plt.plot(ts, Ps[:,0], "b-", label="x(t) (odeint)")
    plt.plot(ts, Ps[:,1], "b-.", label="y(t) (odeint)")
    plt.plot(xRK, PsRK[:,0], "r-",  label="x(t) (RK h=0.25)")
    plt.plot(xRK, PsRK[:,1], "r-.",  label="y(t) (RK h=0.25)")
    plt.plot(x, Pse[:,0], "g-", label="x(t) (Eu h=0.01)")
    plt.plot(x, Pse[:,1], "g-.", label="y(t) (Eu h=0.01)")
    plt.plot(x2, Pse2[:,0], "y-", label="x(t) (Eu h=0.25)")  #note that h=0.25 euler has larger 
    plt.plot(x2, Pse2[:,1], "y-.",  label="y(t) (Eu h=0.25)") #accumulated error when t becomes larger
    plt.xlabel("Time t"); plt.ylabel("x(t) and y(t)"); plt.legend(loc='best');
    plt.title("Lotka-Volterra Prey vs Predator Model");
    plt.savefig('ODE_lotkvolt.png');  plt.show()

    #apply RK4 to do some phase-space plot
    for prey in np.arange(0.25,  5.75,  1):
        P0 = np.array([prey, 0.5])
        #Ps = odeint(dP_dt, P0, ts); plt.plot(Ps[:,0], Ps[:,1], "-", label="x="+str(prey))
        PsRK, xRK =  RK4(dP_dt, P0, 0, tend, 0.25) 
        plt.plot(PsRK[:,0], PsRK[:,1], "-", label="x0="+str(prey))
    plt.xlabel("Prey x(t)");    plt.ylabel("Predator y(t)")
    plt.title("Phase-space plot of Prey vs Predator (y0=0.5)");   plt.legend(loc='best');
    plt.savefig('ODE_lotkvolt_phase.png'); plt.show()




#====================================================================
if __name__=='__main__':  

    test_logistic()
    pendu_simu()
    ring_simu()
    lotk_volt()
