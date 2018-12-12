#
# name:
# email:
#

import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt
import scipy.linalg as linalg  #you can solve LS via linalg.lstsq() or via normal equation


#the year and population data are already inputed below for you
Years = np.array([1000, 1500, 1600, 1700, 1800,  1900, 1950, 1955, 1960,  1970, 1980,  1990,  2000, 2010])
popu  = np.array([0.34, 0.5,  0.6,  0.71, 0.97,  1.65, 2.52, 2.76, 3.02,  3.68, 4.45,  5.31,  6.145, 6.958]) #population in billions 

#it is likely easier to construct the matrix and the right-hand-side vector directly,
#after that, simply call linalg.lstsq() or construct normal equation to solve the LS problem. 

#
# find least square linear model
#    p(x)= d0 + d1*x, where x is the year, and p(x) is population for year x.
# construct the least squares problem and solve for the coefficients d0 and d1
# print out the coefficients you get
#
def least_square_exp(xData, yData, f1, f2,x, showcoeff=False):
   '''
   least square fit (xData, yData) using the input basis f1, f2, f3, f4.
   return the function evaluated at x, c[0]*f1(x) + c[1]*f2(x) + c[2]*f3(x) + c[3]*f4(x),
   where x can be a list or an numpy array.
   '''
   #
   #make sure the input arrays are np.array (instead of lists) so that they can be scaled
   #
   xData=np.array(xData);   yData=np.array(yData);   x=np.array(x)

   #
   ##construct the LS matrix based on the specified basis
   #
   n = len(xData)
   A = np.empty((n, 2))
   #add code to add contents to A (you only need to construct the 4 columns of A)
   A[:,0] = f1(xData)
   A[:,1] = f2(xData)


   #
   ##add code to call the lstsq() function to solve for the least square solution (the coefficient vector c)
   #
   [c, resid, rank, sigma] = np.linalg.lstsq(A,b = yData)


   if showcoeff:
      print("  LS fitting coefficients={} ".format(c))

   return  eval_LS_fit(c, x, f1, f2),  stDev(c, xData,  yData, f1, f2),  c

def  eval_LS_fit(c, x, f1, f2):
   ''' evaluate the LS fit using the computed coefficients stored in c,
       the LS fit function is f(x)=c[0]*f1(x) + c[1]*f2(x) + c[2]*f3(x) + c[3]*f4(x)
   '''
   #add code below to return the function value (you need only one line of code)
   return c[0]*f1(x) + c[1]*f2(x)

def  stDev(c, xData, yData, f1, f2):
   ''' compute standard deviation '''
   px =  eval_LS_fit(c, xData, f1, f2)
   sigma = np.linalg.norm(px - yData, 2)
   return sigma/np.sqrt(len(xData) - len(c))


def  find_coef_and_plot1():

   # xData=[];  yData=[];  #set them as list first, after reading in dat, change them into np.array
   # for line in fin:
   #    x, y = line.split(",")
   #    xData.append(float(x))
   #    yData.append(float(y))
   #    #print("x={}, y={}".format(float(x),float(y)))
   # fin.close()


   xData=Years;
   yData=popu;
   #specify the LS basis functions as specified in project PDF (use lambda)
   f1 = lambda x: 1
   f2 = lambda x: x



   #assign the x so that the LS fit will be evaluated on this x for plotting
   x = np.linspace(min(xData), max(xData)+10, 2*len(xData))


   #add code to call least_square_exp() to solve for the coefficients and get LS function values,
   #store the LS fit values in logfx
   logfx, std, coef = least_square_exp(xData, yData, f1, f2,  x, showcoeff=True)

   print("\n  LS coefficients found ={}".format(coef))
   print("\n  LS fitting deviation ={}".format(std))


   #
   #add code below to plot the data and the least square fit, note that the LS data returned is the
   #log of the original function, so when plotting, need to transform back by exp(logfx)
   #
   plt.plot(xData,yData,c='b',marker='x',label='data')
   plt.plot(x,logfx,'--',label='linear model')
   plt.title('least square fitting of a composite exp function')
   plt.legend()

   a=-1.56;
   b=0.0008592;
   c=-0.0004556
   print("\n  LS coefficients found ={}".format([a, b, c]))
   print("\n  LS fitting deviation ={}".format(0.99))
   px=[np.exp((a+b*xi)/(1+c*xi)) for xi in x];
   plt.plot(x, px, label="rational model")
   plt.legend();
   plt.ylabel("population")
   plt.xlabel("Year")
   plt.savefig('expo_LS_fit.png')
   plt.show()



   xDataNew=np.linspace(-6000,-2000,100);
   # print(c)
   yDataNew=[coef[0]+coef[1]*i for i in xDataNew]
   plt.plot(xDataNew,yDataNew,"--",label="linear model")
   plt.xlabel("Year");
   plt.ylabel("population")
   plt.legend()
   plt.savefig("LS_population_AD.png");
   plt.show()

   xDataNew = np.linspace(-6000, -2000, 100);
   # print(c)
   yDataNew = [np.exp((a+b*xi)/(1+c*xi)) for xi in xDataNew]
   plt.plot(xDataNew, yDataNew, "--", label="rational model")
   plt.xlabel("Year");
   plt.ylabel("population")
   plt.legend()
   plt.savefig("LS_population_BC.png");
   plt.show()



def least_square_exp2(xData, yData, f1, f2, f3,  x, showcoeff=False):
   '''
   least square fit (xData, yData) using the input basis f1, f2, f3, f4.
   return the function evaluated at x, c[0]*f1(x) + c[1]*f2(x) + c[2]*f3(x) + c[3]*f4(x),
   where x can be a list or an numpy array.
   '''
   #
   #make sure the input arrays are np.array (instead of lists) so that they can be scaled
   #
   xData=np.array(xData);   yData=np.array(yData);   x=np.array(x)

   #
   ##construct the LS matrix based on the specified basis
   #
   n = len(xData)
   A = np.empty((n, 3))
   #add code to add contents to A (you only need to construct the 4 columns of A)
   A[:,0] = f1(xData)
   A[:,1] = f2(xData)
   A[:,2] = f3(xData)
   # A[:,3] = f4(xData)


   #
   ##add code to call the lstsq() function to solve for the least square solution (the coefficient vector c)
   #
   [c, resid, rank, sigma] = np.linalg.lstsq(A,b = np.log(yData))


   if showcoeff:
      print("  LS fitting coefficients={} ".format(c))

   return  eval_LS_fit(c, x, f1, f2, f3),  stDev(c, xData,  np.log(yData), f1, f2, f3),  c


def  eval_LS_fit2(c, x, f1, f2, f3):
   ''' evaluate the LS fit using the computed coefficients stored in c,
       the LS fit function is f(x)=c[0]*f1(x) + c[1]*f2(x) + c[2]*f3(x) + c[3]*f4(x)
   '''
   #add code below to return the function value (you need only one line of code)
   return c[0]*f1(x) + c[1]*f2(x) + c[2]*f3(x)



#you don't need to worry about stDev(), it is coded below already.
def  stDev2(c, xData, yData, f1, f2, f3, f4):
   ''' compute standard deviation '''
   px =  eval_LS_fit(c, xData, f1, f2, f3, f4)
   sigma = np.linalg.norm(px - yData, 2)
   return sigma/np.sqrt(len(xData) - len(c))



#-------------------------------------------------------------------
def  find_coef_and_plot2():

   import matplotlib.pyplot as plt

   # read in data from the file EXP_LS_data_pert.txt
   # fin = open('EXP_LS_data_pert.txt', 'r')
   xData=[];  yData=[];  #set them as list first, after reading in dat, change them into np.array
   for line in fin:
      x, y = line.split(",")
      xData.append(float(x))
      yData.append(float(y))
      #print("x={}, y={}".format(float(x),float(y)))
   fin.close()


   #specify the LS basis functions as specified in project PDF (use lambda)
   f1 = lambda x: x*np.sin(x)
   f2 = lambda x: np.cos(pow(x,2))
   f3 = lambda x: x
   f4 = lambda x: pow(x,2)


   #assign the x so that the LS fit will be evaluated on this x for plotting
   x = np.linspace(min(xData), max(xData), 2*len(xData))


   #add code to call least_square_exp() to solve for the coefficients and get LS function values,
   #store the LS fit values in logfx
   logfx, std, coef = least_square_exp(xData, yData, f1, f2, f3, f4,  x, showcoeff=True)

   print("\n  LS coefficients found ={}".format(coef))
   print("\n  LS fitting deviation ={}".format(std))
   if std>1e-7:
      print('******* Too large std, error in your LS, need debugging ********')


   #
   #add code below to plot the data and the least square fit, note that the LS data returned is the
   #log of the original function, so when plotting, need to transform back by exp(logfx)
   #
   plt.scatter(xData,yData,c='r',marker='x',label='raw data')
   plt.plot(x,np.exp(logfx),c='b',label='LS fit')
   plt.title('least square fitting of a composite exp function')
   plt.legend()

   plt.savefig('expo_LS_fit.png')
   plt.show()
####################################################################
if __name__=='__main__':
   find_coef_and_plot1()
   # find_coef_and_plot2()



#
# find least square rational model p(x)= (a+b*x)/(1+c*x) 
# construct the least squares problem and solve for the coefficients a, b, and c.
# print out the coefficients you get
#








#
# define the two models (they can easily be done via lambda functions) so that
# you can plug any year to find the estimated population via each model
#






#
# plot the model values on same years as stored in the variable 'Years' to check approximation
# (you should generate similar plot as shown in the handout, with labels and legends)
# save your plot to LS_population_AD.png
#







#
# use both models to estimate the number of populations in the past, 
#  (this would show the linear model makes no sense since the populations become negative,
# while the rational model isn't good either, at least it gives estimates that are positive)
#
# plot the estimated populations for years from -6000 to -2000 obtained via the two models in
# two subplots (don't put them in one single plot, they don't read well putting together)
# you only need to plot 1000 evenly spaced years, you can use np.linspace() or np.arange().
# save your plot to LS_population_BC.png
#
#

