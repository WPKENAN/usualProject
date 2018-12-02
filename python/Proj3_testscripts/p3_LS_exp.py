## module least square fitting 

import numpy as np
import scipy.linalg as linalg  

#-------------------------------------------------------------------
def least_square_exp(xData, yData, f1, f2, f3, f4,  x, showcoeff=False):
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
   A = np.empty((n, 4))
   #add code to add contents to A (you only need to construct the 4 columns of A)




   #
   ##add code to call the lstsq() function to solve for the least square solution (the coefficient vector c)
   #
   c, resid, rank, sigma = 


   if showcoeff:
      print("  LS fitting coefficients={} ".format(c))

   return  eval_LS_fit(c, x, f1, f2, f3, f4),  stDev(c, xData,  np.log(yData), f1, f2, f3, f4),  c


def  eval_LS_fit(c, x, f1, f2, f3, f4):
   ''' evaluate the LS fit using the computed coefficients stored in c,   
       the LS fit function is f(x)=c[0]*f1(x) + c[1]*f2(x) + c[2]*f3(x) + c[3]*f4(x)
   '''
   #add code below to return the function value (you need only one line of code)




#you don't need to worry about stDev(), it is coded below already.
def  stDev(c, xData, yData, f1, f2, f3, f4):
   ''' compute standard deviation '''
   px =  eval_LS_fit(c, xData, f1, f2, f3, f4)
   sigma = np.linalg.norm(px - yData, 2)
   return sigma/np.sqrt(len(xData) - len(c))



#-------------------------------------------------------------------
def  find_coef_and_plot():

   import matplotlib.pyplot as plt

   # read in data from the file EXP_LS_data_pert.txt
   fin = open('EXP_LS_data_pert.txt', 'r')
   xData=[];  yData=[];  #set them as list first, after reading in dat, change them into np.array
   for line in fin:
      x, y = line.split(",")
      xData.append(float(x))
      yData.append(float(y))
      #print("x={}, y={}".format(float(x),float(y)))
   fin.close()


   #specify the LS basis functions as specified in project PDF (use lambda)
   f1 = 
   f2 = 
   f3 = 
   f4 = 


   #assign the x so that the LS fit will be evaluated on this x for plotting
   x = np.linspace(min(xData), max(xData), 2*len(xData)) 


   #add code to call least_square_exp() to solve for the coefficients and get LS function values,
   #store the LS fit values in logfx 
   logfx, std, coef = 

   print("\n  LS coefficients found ={}".format(coef))
   print("\n  LS fitting deviation ={}".format(std))
   if std>1e-7: 
      print('******* Too large std, error in your LS, need debugging ********')


   #
   #add code below to plot the data and the least square fit, note that the LS data returned is the 
   #log of the original function, so when plotting, need to transform back by exp(logfx)
   #




   plt.savefig('expo_LS_fit.png')
   plt.show()   

####################################################################
if __name__=='__main__':
   find_coef_and_plot()

    





