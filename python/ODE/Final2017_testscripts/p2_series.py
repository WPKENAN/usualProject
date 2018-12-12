#
# name:
# email:
#

import math
#note: your code should not import other modules, in fact, even the math module need not be necessary



def  sum_series(tol=1e-6):
    ## add code to compute p1, p2, p3, and return the required two tuples

    j=1;
    p1=0;
    while abs(1/(2*j-1)**2)>tol:
        p1=p1+1/(2*j-1)**2;
        j=j+1;

    j=1;
    p2=0;
    while abs((-1)**(j-1)/(2*j-1)**3)>tol:
        p2=p2+(-1)**(j-1)/(2*j-1)**3;
        j=j+1;

    j=1;
    p3=0;
    while abs(1/j**4)>tol:
        p3=p3+1/j**4;
        j=j+1




    
    return (p1,p2,p3),(math.sqrt(p1*8),(p2*32)**(1/3),(p3*90)**(1/4))


    




#-----------------------------------------------------------
#do not modify the lines below, design your function so that it agrees with the function call below
#
if __name__ == '__main__':
    
    P, Q = sum_series()
    print('p1={},  p2={},  p3={}'.format(P[0], P[1], P[2]))
    print('second tuple =({:.10f},  {:.10f},  {:.10f})'.format(Q[0], Q[1], Q[2]))


    
