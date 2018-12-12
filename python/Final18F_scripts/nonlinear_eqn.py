#
# module for solving nonlinear equation f(x)=0, methods implemented inlcude
#
# 1. bisection,
# 2. Ridder's method 
# 3. Newton's method  
# 4. Newton combined with bisection
# 5. Quasi-Newton with CFD
#

import numpy as np


#----------------------------------------------------
def bisection(f, x1, x2, tol=10**(-15), SHOW=False):
  """ find a root of f(x)=0 on [x1,x2] by the bisection method, return this root """  

  if SHOW:  print("\n-------- bisection for {}------------".format(f))
  f1 = f(x1)
  if abs(f1) <= 10**(-15):  return x1
  f2 = f(x2)  
  if abs(f2) <= 10**(-15):  return x2

  if  f1*f2 >= 0:
     print("same sign at end points, need to use different interval")  
     return None
  else:
     i = 0
     while abs(x2-x1) > tol: 
        xm = (x1+x2)/2.0;  fm=f(xm)
        if SHOW:  print('i={}, a={}, x={}, b={}, f(x)={}'.format(i, x1, xm, x2, fm))
        if abs(fm)<=min(tol, 1e-14):  return xm
        if  f1*fm >=0: 
           x1 = xm; f1 = fm
        else: 
           x2 = xm; f2 = fm
        i+=1

  return (x1 + x2)/2.0


#----------------------------------------------------  
def ridder(f, a, b, tol=1.0e-15, SHOW=False):   
    """find a root of f(x)=0 on [a,b] using Ridder's method, return this root"""
    if SHOW:  print("\n-------- Ridder's method for {}-------".format(f))
    fa = f(a)
    if abs(fa) <= tol : return a
    fb = f(b)
    if abs(fb) <= tol : return b

    if  fa*fb >= 0:
       print("same sign at end points, need to use different interval")  
       return None

    itmax = 200   
    xold=a - abs(b-a)  #set an initial x (just for the 1st step comparison of abs(x-xold))
    for i in range(itmax):
        # Compute the improved root x from Ridder's formula
        c = 0.5*(a + b); fc = f(c)
        if abs(fc) < tol: 
          if SHOW: print('i={}, a={}, c={}, b={}, f(c)={}'.format(i, a, c, b, fc))
          return c

        s = (fc**2 - fa*fb)**0.5
        if s == 0.0: 
          print("s is 0, encounter divide by 0 exception, quit")
          return None
        dx = (c - a)*fc/s
        if (fa - fb) < 0.0: dx = -dx 
        x = c + dx; fx = f(x)
        if SHOW: print('i={}, a={}, x={}, b={}, f(x)={}'.format(i, a, x, b, fx))

        # Test for convergence
        if abs(x - xold) < tol*max(abs(x),1.0): return x

        xold = x
        # Re-bracket the root as tightly as possible
        if fc*fx >0: 
            if fa*fx<0 : b = x; fb = fx
            else: a = x; fa = fx
        else:
            a = c; b = x; fa = fc; fb = fx

    print('Not converged within {} iterations'.format(itmax))
    return None

#----------------------------------------------------  
def newton(f, fderivertive, x, tol=1.0e-15, SHOW=False):   
    """ find a root of f(x)=0 using Newton's method, starting from the initial input x """
    if SHOW:  print("\n-------- Newton's method for {} ------".format(f))        
    itmax=100
    for i in range(itmax):
        fx = f(x)
        if SHOW: print('i={},  x={},  f(x)={}'.format(i, x,  fx))
        if abs(fx) < tol: return x

        dfx = fderivertive(x)
        dx = -fx/dfx    # use the Newton step
        x = x + dx      # update the solution

    print('Newton iterations exceeds {} steps'.format(itmax))
    return None


#----------------------------------------------------  
def newton_bisect(f, fderivertive, a, b, tol=1.0e-15, SHOW=False):   
    """find a root of f(x)=0, using a combination of bisection and Newton's method """
    if SHOW:  print("\n-------- Newton-bisection method for {} ----".format(f))        
    fa = f(a)
    if abs(fa) < tol: return a
    fb = f(b)
    if abs(fb) < tol: return b
    if  fa*fb >= 0:
       print("same sign at end points, need to use different interval")  
       return False

    x = 0.5*(a + b); itmax=50
    for i in range(itmax):
        fx = f(x)
        if SHOW: print('i={}, a={}, x={}, b={}, f(x)={}'.format(i, a, x, b, fx))
        if abs(fx) < tol: return x
        # tighten the brackets on the root 
        if fa*fx <0: 
          b = x  
        else: 
          a = x

        dfx = fderivertive(x)
        if abs(dfx) < 1e-20:
          dx = b-a        # if dfx is zero, push x out of bounds
        else:
          dx = -fx/dfx    # use the Newton step

        x = x + dx        # update the solution with a Newton step

        # if the result is outside the brackets, replace the Newton update by a bisection step
        if (b - x)*(x - a) < 0.0:  
            dx = 0.5*(b - a)                      
            x = a + dx

        # check for convergence     
        if abs(dx) < tol*max(abs(b),1.0): return x

    print('Newton-bisection iterations exceeds {} steps'.format(itmax))
    return None

  
#----------------------------------------------------  
def quasi_newton(f, x, h=1e-4, tol=1.0e-14, FD='CFD', itmax=120, SHOW=False):   
    """ "find a root of f(x)=0, using Quasi Newton's method, starting from an initial value x.
        The derivative is automatically computed via numerical differentiation,
        it defaults to using central finite difference scheme.
        The default for the grid length used for FD is h=1e-4.
        (your code should not exceed itmax iterations. if SHOW is passed as True, then
         your code should print out intermediate results)
    """
    if SHOW:  print("\n-------- Quasi Newton's method,  FD scheme ={} ------------".format(FD))        
    for k in range(itmax):
        fx = f(x)
        if SHOW: print('k={},  x={},  f(x)={}'.format(k, x,  fx))
        if abs(fx) < tol: break

        ## compute the derivative of f(x) at x via FD (the default is CFD)
        if FD=='FFD':     #forward finite difference
           dfx = (f(x+h) - f(x))/h
        elif FD=='BFD':   #backward finite difference
           dfx = (f(x) - f(x-h))/h
        else:
           dfx = (f(x+h/2) - f(x-h/2))/h  #this is slightly better than the one below
           #dfx = (f(x+h) - f(x-h))/(2*h)
           
        if abs(dfx)==0:
          print('\n\n*** warning, zero FD encountered ***, fder({})={}\n\n'.format(x, dfx))
          break
        
        x = x -fx/dfx      #use the quasi Newton step to update the solution

    if k<= itmax and abs(fx)<=tol:
       print('Quasi-Newton({}) converged in {} steps: x={}, f(x)={}'.format(FD, k, x, fx))
    else:
       print('**Warning** Quasi-Newton({}) did NOT converge in {} steps: x={}, f(x)={}'.format(FD, k, x, fx))
    return (x, k, fx)   




#----------------------------------------------------
# define some functions to test the above code
#----------------------------------------------------

def  fun1(x):
  return  x**3 - 5*x**2 + 2

def  fun1_der(x):  #derivative of fun1()
  return  3*x**2 - 10*x 

#----------------------------------------------------
def  fun2(x):
  return  x**7 - 20*np.cos(x*5) - x - 900  

def  fun2_der(x):  #derivative of fun2()
  return  7*x**6  + 100*np.sin(x) - 1 

#----------------------------------------------------
def get_fV(V, N):
   """ retuns the function f(V) as specified in the project2 PDF """

   #first, set up the parameters of the equation 
   a=0.401;  b=4.27*1e-5;  T=300;  p=3.5*10**7;  k=1.3806503*10**(-23)

   return (p + a*(N/V)**2)*(V - N*b) - k*N*T 

def dfV(V, N):
   """ retuns the derevative of the function f(V) """

   #first, set up the parameters of the equation 
   a=0.401;  b=4.27*1e-5;  T=300;  p=3.5*10**7;  k=1.3806503*10**(-23)

   return  -2*N**2/(V**3)*(V - N*b) + (p + a*(N/V)**2)

#==============================================================
if __name__=='__main__':

    print("="*90)
    print("run log of an example from CAD (computer aided design):")
    print("    find the intersection point of the curve x^5 + y^5 = 1 with the line y = 2x-1.") 
    print("    so the funtion to solve for a root is  f(x) =  x**5 + (2*x-1)**5 - 1.")
    print("="*90)

    f = lambda x : x**5 + (2*x-1)**5 - 1 
    x1 = -1;  x2 =1
    xb = bisection(f, x1, x2, SHOW=True)
    xr = ridder(f, x1, x2, SHOW=True)
 
    df = lambda x: 5*x**4 + 10*(2*x-1)**4   #derivative of f above
    xntbi= newton_bisect(f, df, x1, x2, SHOW=True)

    #test on fun1 and fun2 defined above
    print("="*90)
    print("   test on fun1 ")
    a = -100;  b=100
    xb11 = bisection(fun1, a, b, SHOW=True)
    xr11 = ridder(fun1, a, b, SHOW=True)
    xntbi11 = newton_bisect(fun1, fun1_der, a, b, SHOW=True) 

    print("="*90)
    print("   test on fun2 ")
    a = -5;  b=5
    xb12 = bisection(fun2, a, b, SHOW=True)
    xr12 = ridder(fun2, a, b, SHOW=True)
    xntbi12 = newton_bisect(fun2, fun2_der, a, b, SHOW=True) 


    #test on the f from p6 in project 2
    N = 9000
    print("\n")
    print("="*90)
    print("run log of an example from project2 problem 6:")
    print("    here the number of molecules N is set to {}".format(N))
    print("="*90)
    f = lambda V: get_fV(V, N)
    x1 = 0.001;  x2 =1
    xb = bisection(f, x1, x2, SHOW=True)
    xr = ridder(f, x1, x2, SHOW=True)

    df = lambda V: dfV(V, N) 
    xnt= newton(f, df, (x1+x2)/2, SHOW=True)
    xnt= newton(f, df, x1, SHOW=True)
    xnt= newton(f, df, x2, SHOW=True)
    xntbi= newton_bisect(f, df, x1, x2, SHOW=True)
