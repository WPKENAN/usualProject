## module containing quadrature rules such as the trapezoid, simpson, romberg 

import numpy as np

#--------------------------------------------------------------------
def adap_trap(f, a, b, tol=1e-5): 
    ''' Usage:  integral_value, npanels = Trapezoid_adap(f,a,b,tol=1e-5).
        Apply the adaptive trapezoidal rule to compute integral of f on [a,b] using
        2^k panels at each iteration,  starting with k=0. 
        Break the loop when the difference between two adjacent integral values are below tolerance.
        Return the integral value and the number of panels used.
        (this is not truly adaptive since it kept dividing each subinterval)
    '''
    Iold = (f(a) + f(b))*(b-a)/2
    Itmax= 50
    for k in range(1, Itmax): 
        n = 2**k;   h = (b-a)/n
        x = a + h           #coordinate of 1st new node, the next ones will be obtained by x <- x+h*2 
        sum = f(x)
        for i in range(1, n//2): 
            x = x + 2*h     #coordinates of newly added nodes
            sum = sum + f(x)  

        Inew = Iold/2 + h*sum;  
        if abs(Inew - Iold) < tol :   return Inew, n
        Iold = Inew

    print("Warning:  Trapezoid_adap did not converge within {} steps".format(Itmax))
    return Inew, n

#--------------------------------------------------------------------
def simpson(f, a, b, n=1000):
    """compute integral of f from a to b by the composite Simpson's h/3 rule, 
       using n panels (if n is not even, set n=n+1)
    """
    if n % 2 !=0:  n += 1       
    h = (b - a) / n
    sum21, sum41 = 0, 0
    for i in range(2, n-1, 2):
        sum21 += f(a + i*h)
        sum41 += f(a + i*h -h)
    return (f(a) + f(b) + 4*sum41 + 2*sum21 + 4*f(a + i*h+h)) * h/3,  n


#--------------------------------------------------------------------
def recursive_simpson2(f, a, b, c=None, fa=None, fb=None, fc=None, tol=1e-6):
    '''recursive implementation of the simpson's h/3 rule'''
    if fa==None: fa = f(a)
    if fb==None: fb = f(b)
    if c == None or fc == None:  
        c = (a+b)/2;  fc = f(c)

    h = (b-a)/2
    Iold = h/3*(fa + 4*fc + fb)
    h = h/2;  
    midL=a+h;    fmidL=f(midL)
    midR=a+3*h;  fmidR=f(midR)
    Inew = h/3*(fa + 2*fc + fb + 4*(fmidL + fmidR))
    
    reltol = max(abs(Iold), abs(Inew), 0.01)*max(0.5e-11, tol/10000)
    if abs(h) < 1e-15  or abs(Inew - Iold) < reltol:
        return Inew, 4
    else:
        Ileft,  nleft  = recursive_simpson2(f, a, c, c=midL, fa=fa, fb=fc, fc=fmidL, tol=tol)
        Iright, nright = recursive_simpson2(f, c, b, c=midR, fa=fc, fb=fb, fc=fmidR, tol=tol)
        return Ileft + Iright,  nleft + nright



