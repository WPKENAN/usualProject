#
# name:
# email:
#

import math
#note: your code should not import other modules, in fact, even the math module is not necessary



def  sum_series(tol=1e-15):

    p1 = 1
    for i in range(2, 10**8):   #the default is 1e-15, so going up to 10**8 should be enough
        newterm = 1./(2*i-1)**2
        p1 += newterm
        if newterm <= tol:  break


    p2 = 1
    for j in range(2, 10**6):
        newterm = (-1.)**(j-1)/(2*j-1)**3
        p2  += newterm 
        if abs(newterm) <= tol:  break    


    p3 = 1
    for j in range(2, 10**5):      
        newterm = 1./j**4
        p3  += newterm 
        if newterm <= tol:  break    

        
    return  (p1, p2, p3),  ((p1*8)**.5,  (p2*32)**(1./3),  (p3*90)**(1/4)) 



if __name__ == '__main__':
    
    P, Q = sum_series()
    print('p1={},  p2={},  p3={}'.format(P[0], P[1], P[2]))
    print('second tuple =({:.15f},  {:.15f},  {:.15f})'.format(Q[0], Q[1], Q[2]))


    
