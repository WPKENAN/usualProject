"""
Name:
email:

"""
import numpy as np
import pylab as plt


def simpson(f, a, b, n=1000, type='1/3'):
    """the simpson's rules,   type='1/3',  '3/8', or '1/48',  corresponding to the three formulas 
       in the project pdf file.
       return a tuple that contains (integral_val, number_of_panels_used)
    """
    if type == '1/3':
        if n%2 !=0: n+=1
        h = (b-a)/n
        sum = f(a) + f(b) + 4*f(a+h)
        x = a+h
        for i in range(1, int(n/2)):
            x += h; sum += 2*f(x)
            x += h; sum += 4*f(x)
        return sum*h/3,n

    elif  type == '3/8':
        while(n%3!=0):n+=1
        h = (b-a)/n
        sum = f(a) + f(b) + 3*(f(a+h)+f(a+2*h))
        x = a+2*h
        for i in range(1, int(n/3)):
            x += h; sum += 2*f(x)
            x += h; sum += 3*f(x)
            x += h; sum += 3*f(x)
        return(sum*3*h/8,n)


    elif type =='1/48':
        h = (b-a)/n
        sum =17*f(a)+59*f(a+h)+43*f(a+2*h)+49*f(a+3*h)+17*f(b)+59*f(b-h)+43*f(b-2*h)+49*f(b-3*h)
        x = a+3*h
        for i in range(4, n-3):
            x += h; sum += 48*f(x)
        return(sum*h/48,n)   
        
    else:
        raise Exception('Error: type not implemented')



#==========================================================================================
# do not change the code below.  instead, make interfaces (especially the returns)
# of your functions above fit the function calls below to avoid any mismatch.
#
def NumSum(f, a, b, n=1000, rule='TrapSum'):
    """ get appriximation of integration of f(x) on [a,b]  using specific summation rules """
    
    h = (b-a)/n;   sum = 0.;   x = a
    if rule=='MSum':
        for i in range(0,n):  sum += f(x+h/2); x+=h
    else:
        for i in range(1,n):  x+=h;  sum += f(x) 

        if rule=='LESum':  
            sum += f(a)
        elif rule=='RESum':
            sum += f(b)
        elif rule=='TrapSum':
            sum += (f(a)+f(b))/2 
        else:
            raise Exception('rule not implemented yet')
    
    return sum*h, n
    


def  plot_numrical_integral(f, a, b, iexact, plot_EndPointSum=False, savefigfile=None):

    N = range(10, 2000, 100);
    MS = np.zeros(len(N))
    TS = np.zeros(len(N))
    Simp1over3 = np.zeros(len(N))
    Simp3over8 = np.zeros(len(N))
    Simp1over48 = np.zeros(len(N))

    for i, n in enumerate(N):
        MS[i], _ = NumSum(f, a, b, n, rule='MSum')
        TS[i], _ = NumSum(f, a, b, n, rule='TrapSum')        
        Simp1over3[i], _  = simpson(f, a, b, n, type='1/3')
        Simp3over8[i], _  = simpson(f, a, b, n, type='3/8')
        Simp1over48[i], _ = simpson(f, a, b, n, type='1/48')


    fh = plt.figure
    plt.semilogy(N, abs(MS- iexact), 'b-.', label='MiddleSum' )
    plt.semilogy(N, abs(TS- iexact), 'c-', label='TrapSum' )
    plt.semilogy(N, abs(Simp1over3- iexact), 'r-', label='Sim 1/3' )
    plt.semilogy(N, abs(Simp3over8- iexact), 'y--', label='Sim 3/8' )
    plt.semilogy(N, abs(Simp1over48- iexact), 'k:', label='Sim 1/48' )
    if plot_EndPointSum:
        LS = np.zeros(len(N));  RS = np.zeros(len(N))
        for i, n in enumerate(N):
            LS[i] = NumSum(f, a, b, n, rule='LESum')
            RS[i] = NumSum(f, a, b, n, rule='RESum')       
        plt.semilogy(N, abs(LS- iexact), 'g-', label='LeftSum' )
        plt.semilogy(N, abs(RS- iexact), 'r:', label='RightSum' )

    plt.legend(loc='best')
    plt.xlabel(' # of panels ');  plt.ylabel(' integration error ')
    if savefigfile!=None:  
        plt.title('error evolution with increasing # of panels for '+ savefigfile)
        plt.savefig(savefigfile+'.jpg')
    else:
        plt.title('error evolution with increasing # of panels')
    plt.show()
    

    
if __name__=='__main__':
    
    f1 = lambda x: np.sin(x);  a1 = -np.pi;  b1 = 1.5*np.pi;  iexact1 =  np.cos(a1) - np.cos(b1)
    f2 = lambda x: np.exp(x);  a2 = -5;   b2 = 5;    iexact2 = (f2(b2) - f2(a2))

    F = lambda x : np.cos(np.exp(x) - x**2)   #anti-derivative
    f3 = lambda x : -np.sin(np.exp(x) - x**2)*(np.exp(x) - x*2)
    a3 = -3;  b3=3;  iexact3 = F(b3) - F(a3)

    F = lambda x : np.log(np.exp(x) + x**4)   #anti-derivative
    f4 = lambda x : 1/(np.exp(x) + x**4)*(np.exp(x) + 4*x**3)
    a4 = -10;  b4=10;  iexact4 = F(b4) - F(a4)
    
    F = lambda x : (np.exp(x) + x*np.sin(x))**2   #anti-derivative
    f5 = lambda x : 2*(np.exp(x) + x*np.sin(x))*(np.exp(x) + np.sin(x) + x*np.cos(x))
    a5 = -20;  b5=5;  iexact5 = F(b5) - F(a5)

    i = 1
    for (f, a, b, iexact) in zip((f1, f2, f3, f4, f5), (a1, a2, a3, a4, a5), (b1, b2, b3, b4, b5), 
                                 (iexact1, iexact2,  iexact3,  iexact4, iexact5)):
        plot_numrical_integral(f, a, b, iexact, plot_EndPointSum=False, savefigfile='function'+str(i))
        i += 1
