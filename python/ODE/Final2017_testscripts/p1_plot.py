#
# name:
# email:
#

import numpy as np
import matplotlib.pyplot as plt
#note: your code should not import other modules 


def  plot_gaussian(x, abList):  
    '''plot G(x, a, b) on the input x and the (a,b) from the abList
       the x is a vector containing the x-coordinates of the data points to be plotted;
       the abList is a list containing the (a,b) pairs, e.g., abList=[(0,1), (10, 2)] etc.

       note:  
       (1) your code is allowed to use only one plot command (it should be within a loop,
           this means you let python decide the plotting line style automatically)
           to plot all the curves associated with different (a,b);
       (2) save your plot to a file in png format named 'gaussian_plot.png'
    '''
    
    #since the input x may be a list, you may need to first transform x into an numpy array
    #so that vectorized operation such as x**2 etc can be valid
    for (a,b) in abList:
        fx=1/np.sqrt(2*np.pi*(b**2)) * np.exp(-(x-a)**2 / 2 / b**2);
        plt.plot(x,fx,label="a={}, b={}".format(a,b));

    plt.legend();
    plt.xlabel('x');
    plt.ylabel('y=G(x,a,b)');
    plt.title("plot of Gaussian distribution functions G(x,a,b)");
    plt.grid(color='c',linestyle=':',lw=0.5);
    plt.savefig('gaussian_plot.jpg');
    plt.show()

    
    

    ## plot the functions, you should use only one plt.plot() command for plotting
    ## all the functions, which means you need to plot within a loop over alphaVect
    ## (should let python decide the plotting line style automatically)



    



    

#
#you only need to take care of the above plotting function, the following code 
#(not to be modified) should produce the figure in the handout if your above code works right
#
if __name__=='__main__':

    abList = [(0, 1), (-2, 3), (3, 1.5), (-6, 2)]

    # x = [t for t in np.linspace(-10, 10, 200)]  #note x is intentionally set to be a list here
    x=np.linspace(-10,10,200)
    
    plot_gaussian(x, abList)





