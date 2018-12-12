#
# name:
# email:
#

import numpy as np
import matplotlib.pyplot as plt
#note: your code should not import other modules (all the math functions such as sin() etc are in numpy)



##
## do not change the following function recursive_trape(f, a, b, fa=None, fb=None, tol=1e-10)
##
def recursive_trape(f, a, b, fa=None, fb=None, tol=1e-10):
    '''recursive implementation of the trapezoidal rule to compute the
       integral of f(x) for x in [a, b].
       this function returns the integral_value and the number_of_panels_used .

       Note: this recursive implementation reuses previous function evaluations, so it is economical.
 
       To use this function for evaluating integral of f(x) on [a, b], you only need to call it as

         recursive_trape(f, a, b)  #certainly you need to add variables to receive its returned values
    '''

    if fa==None : fa=f(a)
    if fb==None : fb=f(b)
    h = (b-a)/2
    Iold = (fa + fb)*h
    fmid = f(a+h)
    Inew = Iold/2 + fmid*h

    reltol = max(abs(Iold), abs(Inew), 0.01)*max(0.5e-10, tol)
    if abs(h) <= 1e-15  or abs(Inew-Iold)<= reltol:
        return Inew, 2
    else:
        left_integral,  left_panel  = recursive_trape(f, a, a+h, fa, fmid, tol)
        right_integral, right_panel = recursive_trape(f, a+h, b, fmid, fb, tol)
        return  left_integral +right_integral,  left_panel +right_panel


    

##
## add code below to call recursive_trape() to solve the two problems specified in the handout.
## there are several different ways to code, you are free to design your code (interfaces etc),
## as long as you can get answers of the y(x)'s being asked for, and can produce the required plot.
##




