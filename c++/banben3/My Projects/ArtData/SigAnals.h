#include <vector>
#include <algorithm>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
//#include "msp.h"
using namespace std;
/*
void probability(vector<float> vec,float* p)
{
	int count=sizeof(p)/sizeof(float);
	int vecsiz=vec.size();
	sort(vec.begin(),vec.end());
	float intval=(vec[vecsiz-1]-vec[0])/(float)(count-1);
	float h=1.0f/(float)(vecsiz-1);
	
	int k=0;
	for(int i=0;i<vecsiz;i++)
	{
		if(vec.at(i)<vec[0]+(k+1)*intval){p[k]+=h;}
		else{k++;p[k]+=h;}
	}
//	return p;
}

/*
void mcorpsd(complex x[],complex r[],int n,int lag,int iwindow,float t)
{
/*///////////////////////////////////////////////////////////////////////*/
/*   用Blackman-Tukey法（自相关法）对信号 作功率谱估计。
   Routine mcorpsd: To compute the power spectrum by auto-correlation
                     method (Blackman-Tukey method).
   Input Parameters:
     x : Array of complex data samples from 0 to n-1
     n   : Number of data samples
     mfre: Data number of power spectrum
     lag : the highest lag index to compute
   Output Parameters:
     r(m):Array of complex correlation from 0 to Lag-1
                                        in chapter 11*/
/*///////////////////////////////////////////////////////////*/
/*        float psdr[4096],psdi[4096];
        int mfre,k;
        float pi2,s,w,t1;
        mfre=4096;
        mcorre1(x,x,r,n,lag);
        pi2=8.*atan(1.);
        s=pi2/(float)(2*lag);
        for(k=0;k<lag;k++)
           {psdr[k]=r[k].real;
            psdi[k]=r[k].imag;
            if(iwindow==1)
               continue;
            w=0.54+0.46*cos(s*k);
            psdr[k]=psdr[k]*w;
            psdi[k]=psdi[k]*w;
            }
        for(k=1;k<lag;k++)
           {psdr[mfre-k]=psdr[k];
            psdi[mfre-k]=-psdi[k];
            }
        for(k=lag;k<=mfre-lag;k++)
           {psdr[k]=0.;
            psdi[k]=0.;
            }
        mrelfft(psdr,psdi,mfre,-1);
        for(k=0;k<mfre;k++)
            psdr[k]=psdr[k]*psdr[k]+psdi[k]*psdi[k];
        t1=t;
        mpsplot(psdr,psdi,mfre,t1);
 //       return;
}
*/
/*
void mcorre1(complex x[],complex y[],complex r[],int n,int lag)
{
---------------------------------------------------------------------
  直接按定义计算x(n),y(n) 的互相关函数 r(m)，若x=y ，则求出的是自相关，x,y,r 为复序列。
  Routine MCORRE1:To estimate the biased cross-correlation function
  of complex arrays x and y. If y=x,then it is auto-correlation.
  input parameters:
     x  :n dimensioned complex array.
     y  :n dimensioned complex array.
     n  :the dimension of x and y.
     lag:point numbers of correlation.
  output parameters:
     r  :lag dimensioned complex array, the correlation function is
         stored in r(0) to r(lag-1).
                                      in Chapter 1 and 11
---------------------------------------------------------------------
        int m,j,k;
        for(k=0;k<lag;k++)
	   {
	    m=n-1-k;
            r[k].real=0.0;
            r[k].imag=0.0;
            for(j=0;j<=m;j++)
	       {
		r[k].real+=y[j+k].real*x[j].real+y[j+k].imag*x[j].imag;
                r[k].imag+=y[j+k].imag*x[j].real-y[j+k].real*x[j].imag;
                }
	    r[k].real=r[k].real/n;
	    r[k].imag=r[k].imag/n;
             }
        return;
}
*/
/*
void mcorre2(complex x[],complex y[],int m,int n,int icorre)
{
---------------------------------------------------------------------
  用FFT实现相关函数快速估计。
  Routinue mcorre2: To Compute the Correlation  Function of x(i) and
  y(i) by DFT. x(i),y(i),i=0,...,m-1;But the dimension n of x,y must
  be >=2*m and be the power of 2 ; in chapter 11.
  If: icorre=0: For auto-correlation
      icorre=1: For cross-correlation
                                      in chapter 11
---------------------------------------------------------------------
        int i,s,k;
        complex z;
	s=n;
	do
	{
	  s=s/2.;
	  k=s-2;
	 }while(k>0);
	 if(k<0)exit(1);
	 for(i=m;i<n;i++)
	   {
	    x[i].real=0.;
	    x[i].imag=0.0;
            }
        msplfft(x,n,-1);
	if(icorre==1)
	  {
	      for(i=m;i<n;i++)
		{y[i].real=0.;
		 y[i].imag=0.0;
		 }
	     msplfft(y,n,-1);
	     for(k=0;k<n;k++)
		{z.real=x[k].real;z.imag=x[k].imag;
		 x[k].real=(z.real*y[k].real+z.imag*y[k].imag)/(float)(m);
		 x[k].imag=(z.real*y[k].imag-z.imag*y[k].real)/(float)(m);
		 }
	 }
	 else
        for(k=0;k<n;k++)
	   {
	    x[k].real=pow(mabs(x[k]),2)/(float)(m);
            x[k].imag=0.0;
	     }
	msplfft(x,n,1);
        return;
}
*/
/*
void mdecint(float x[],float h[],float y[],int nh,int ny,int m,
int l,int *k)
{
----------------------------------------------------------------------
 对给定数据 作 倍的抽样率转换
 Routine mdecint: Using eq. (9.4.33) to implement sampling rate
   conversion by L/M.
 Note: First call routine DEFIR3 to design lowpass  filter, the cutoff
       frequency Wp is given by equation (9.4.26) and the amplitude in
       bandpss should be L,that is,Hd(w)=L,   so we can obtain the
       impulse response  h(n), then call MDECINT to complete needed
       convesion.
  Input parameters:
   x(n):nx dimensioned real array,the data to be converted is stored
             in x(0) to x(n-1);
   h(n):nh dimensioned real array,impulse response is stored in h(0)
             to h(m-1) obtained by call DEFIR3 ;
   m   : factor to decrease sampling freq. (for decimation)
   l   : factor to increase sampling freq. (for interpolation)
 output parameters:
   y(n):ny dimensioned real array, y(n),n=k,...ny-1, have been
            converted data. Generally,ny=nx*L/M
                                      in Chapter 9
---------------------------------------------------------------------
        int my,mh,ih,ihl,ihh,ix,tk;
        float t;
        tk=nh/l;
        *k=(l==1)?(nh/m+1):(tk+1);
        for(my=*k;my<ny;my++)
           {
            y[my]=0.;
            for(mh=0;mh<tk;mh++)
               {
                ih=my*m/l;
                ihl=ih*l;
                ihh=my*m+mh*l-ihl;
                ix=ih-mh;
                t=(ix>=0)?x[ix]:0.0;
                y[my]+=h[ihh]*t;
                }
           }
}

double* FFT(double *data, int n, BOOL isInverse)
{

// 快速傅里叶变换
// data 长度为 (2 * 2^n), data 的偶位为实数部分, data 的奇位为虚数部分
// isInverse表示是否为逆变换
     int mmax, m, j, step, i;
     double temp;
     double theta, sin_htheta, sin_theta, pwr, wr, wi, tempr, tempi;
     n = 2 * (1 << n);
     int nn = n >> 1;
     // 长度为1的傅里叶变换, 位置交换过程
     j = 1;
     for(i = 1; i < n; i += 2)
     {
         if(j > i)
         {
             temp = data[j - 1];
             data[j - 1] = data[i - 1];
             data[i - 1] = temp;
             data[j] = temp;
             data[j] = data[i];
             data[i] = temp;
         }
         // 相反的二进制加法
         m = nn;
         while(m >= 2 && j > m)
         {
             j -= m;
             m >>= 1;
         }
         j += m;
     }
     // Danielson - Lanczos 引理应用
     mmax = 2;
     while(n > mmax)
     {
         step = mmax << 1;
         theta = DOUBLE_PI / mmax;
         if(isInverse)
         {
             theta = -theta;
         }
         sin_htheta = sin(0.5 * theta);
         sin_theta = sin(theta);
         pwr = -2.0 * sin_htheta * sin_htheta;
         wr = 1.0;
         wi = 0.0;
         for(m = 1; m < mmax; m += 2)
         {
             for(i = m; i <= n; i += step)
             {
                 j = i + mmax;
                 tempr = wr * data[j - 1] - wi * data[j];
                 tempi = wr * data[j] + wi * data[j - 1];
                 data[j - 1] = data[i - 1] - tempr;
                 data[j] = data[i] - tempi;
                 data[i - 1] += tempr;
                 data[i] += tempi;
             }
             sin_htheta = wr;
             wr = sin_htheta * pwr - wi * sin_theta + wr;
             wi = wi * pwr + sin_htheta * sin_theta + wi;
         }
         mmax = step;
     }
	 return data;
/ *    输入数据为data，data是一组复数，偶数位存储的是复数的实数部分，奇数位存储的是复数的虚数部分。data的长度与n相匹配。注意：这里的n并非是data的长度，data的实际长度为(2 * 2^n),存储了N = 2^n个复数。

    输出也存放在data中。

    以正向傅里叶变换为例，作为输入data中存储的是以delta为时间间隔时域函数的振幅抽样值。经过函数计算后data中存放输出，存储的是以1/(N * delta)为频率间隔频域像函数值。频率范围为0Hz,1/(N * delta),2/(N * delta) ... (N / 2 - 1) / N * delta, +/- 1 / delta, -(N / 2 - 1) / N * delta ... -2/(N * delta), -1/(N * delta)。注意这是一个中间大两边小的排列。
* /
}*/
/*
void mmvseps(complex x[],complex ef[],complex eb[],int n,
complex a[],int ip,int *ierror,float ts)
{
----------------------------------------------------------------------
   用最小方差法估计序列 的功率谱
   routine MMVSEPS: To complete the minimum variance spectral estimation.
   The Burg algorithm is used for the estimation of the AR parameters.

   Input parameters:
          n  : Number of data samples;
          ip : Order of autoregressive model;
          x  : Array of complex data samples, x(0) through x(n-1);
          ts : Sample interval in seconds (real)
   Output Parameters:
         ep  : Real variable representing driving noise variance;
          a  : Array of complex AR parameters a(0) to a(ip);
       psdr  : real array,power spectrum
    ierror=0 : No error
          =1 : Ep<=0 .

         ef  : complex work array,ef(0) to ef(n-1)
         eb  : complex work array,eb(0) to eb(n-1)
                                      in chapter 12

主函数
#include "mrelfft.c"
#include "mpsplot.c"
#include "marburg.c"
#include "mmvseps.c"
void main()
{
        FILE *fp;
        complex x[128],ef[128],eb[128],a[32];
        int n,ip,k,ierror;
        int *ierr;
        float ts;
        ierr=&ierror;
        n=128;ip=13;
        ts=1.;
        if((fp=fopen("test.dat","r"))==NULL)
        {printf("cannot open file\n");
              exit(0);
              }
        for(k=0;k<n;k++)
            fscanf(fp,"%f,%f\n",&x[k].real,&x[k].imag);
            fclose(fp);
        mmvseps(x,ef,eb,n,a,ip,ierr,ts);
        printf("     ierror=%d\n",ierror);
        printf("              k               a(k)  \n");
        for(k=0;k<=ip;k++)
        printf("    %d,    %f,%f\n",k,a[k].real,a[k].imag);
        }
----------------------------------------------------------------------
        complex sum;
        float psdr[512],psdi[512];
        int mfre,k,i;
        float ep,c;
        float *p_ep;
        p_ep=&ep;
        mfre=512;
        marburg(x,a,ef,eb,n,ip,p_ep,ierror);
          printf("    ep=%f\n",ep);
        if(*ierror!=0)
           return;
        a[0].real=1.;
        a[0].imag=0.;
        for(k=0;k<=ip;k++)
           {sum.real=0.;
            sum.imag=0.;
            for(i=0;i<=ip-k;i++)
               {c=(float)(ip+1-k-2*i);
                sum.real+=c*(a[k+i].real*a[i].real+
                             a[k+i].imag*a[i].imag);
                sum.imag+=c*(a[k+i].imag*a[i].real-
                             a[k+i].real*a[i].imag);
                }
            sum.real/=ep;
            sum.imag/=ep;
            psdr[k]=sum.real;
            psdi[k]=sum.imag;
            if(k==0)
               continue;
            psdr[mfre-k]=psdr[k];
            psdi[mfre-k]=-psdi[k];
            }
        for(k=ip+1;k<=mfre-ip-1;k++)
           {psdr[k]=0.;
            psdi[k]=0.;
            }
        mrelfft(psdr,psdi,mfre,-1);
        for(k=0;k<mfre;k++)
            if(psdr[k]<=0)
              {printf(" Stop at routine MMVSEPS \n");
               printf("  Power spectrum becomes infinite or negative!");
               return;
               }
        for(k=0;k<mfre;k++)
            psdr[k]=ts/psdr[k];
        mpsplot(psdr,psdi,mfre,ts);
        return;
}
*/
/*
void mperpsd(complex x[],int n,int nshift,int nsamp,int iwidow,float ts)
{
----------------------------------------------------------------------
 用Welch平均法对信号x(n) 作功率谱估计
 Routine mperpsd:To compute the averaged periodogram by Welch's method.
   Input Parameters:
     n      - Number of data samples
     nshift - Number of samples shift between segments
     nsamp  - Number of samples per segment (must be even)
     x      - Array of complex samples X(0) to X(N-1)
     iwidow - If =1,for rectangular window, not =1,for Hamming window.
   Output Parameters:
     nsection   - Number of segments averaged
     psd    - Real array of power spectral density estimation values
                                       in chapter 11
---------------------------------------------------------------------
        float w[128],psdr[4096],psdi[4096],work[4096];
        float pi2,tsv;
        int mfre,k,nsection,j,index;
        pi2=8.*atan(1.);
        tsv=0.0;
        mfre=4096;
        for(k=0;k<n;k++)
            w[k]=0.0;
        for(k=0;k<nsamp;k++)
           {
            if(iwidow==1)
                 continue;
            w[k]=0.538+0.462*cos(pi2*(-.5+(float)(k)/(float)(nsamp)));
            tsv+=w[k]*w[k];
            }
        nsection=(nshift==0)?(n/nsamp):((n-nsamp)/(nsamp-nshift) + 1);
        printf("   total segements=%d\n",nsection);
        for(k=0;k<mfre;k++)
            work[k]=0.;
        for(k=1;k<=nsection;k++)
           {
            printf("   k=%d\n",k);
            for(j=0;j<nsamp;j++)
               {
                index=j+(k-1)*(nsamp-nshift);
                psdr[j]=x[index].real;
                psdi[j]=x[index].imag;
                if(iwidow==1)
                   continue;
                psdr[j]=psdr[j]*w[j];
                psdi[j]=psdi[j]*w[j];
                }
            for(j=nsamp;j<mfre;j++)
               {
                psdr[j]=0.;
                psdi[j]=0.;
                }
            mrelfft(psdr,psdi,mfre,-1);
            for(j=0;j<mfre;j++)
                {
                 psdr[j]=psdr[j]*psdr[j]+psdi[j]*psdi[j];
                 psdr[j]=psdr[j]/(float)(nsamp);
                 work[j]=work[j]+psdr[j];
                 }
            }
/  *-------------------------------------------------------------------*  /
        tsv=tsv*nsection*ts;
        for(k=0;k<mfre;k++)
           {
            psdr[k]=work[k];
            if(iwidow==1)
               continue;
            psdr[k]=psdr[k]/tsv;
            }
        mpsplot(psdr,psdi,mfre,ts);
        return;
}
*/
/*
void mpsplot(float psdr[],float psdi[],int mfre,float ts)
{
---------------------------------------------------------------------
   在归一化频率轴上绘出归一化的功率谱曲线
   Routine mpsplot: To plot the normalized power spectum curve on the
   normalized frequency axis from -.5 to  +.5 .
        mfre : Points in frequency axis and must be the power of 2.
        ts   : Sample interval in seconds (real).
        psdr : Real array of power spectral density values.
        psdi : Real work array.
                                       in chapter 11,12
--------------------------------------------------------------------* /
        FILE *fp;
        char filename[30];
        int k,m2;
        float pmax,fs,faxis;
        m2=mfre/2;
        for(k=0;k<m2;k++)
           {psdi[k]=psdr[k];
            psdr[k]=psdr[k+m2];
            psdr[k+m2]=psdi[k];
            }
        pmax=psdr[0];
        for(k=1;k<mfre;k++)
            if(psdr[k]>pmax)
               pmax=psdr[k];
        for(k=0;k<mfre;k++)
           {psdr[k]=psdr[k]/pmax;
            if(psdr[k]<=0.0)
               psdr[k]=.000001;
            }
        fs=1./ts;
        fs=fs/(float)(mfre);
        printf("Please input filename:\n");
        scanf("%s",filename);
        if((fp=fopen(filename,"w"))==NULL)
           {printf("cannot open file\n");
            exit(0);
            }
        for(k=0;k<mfre;k++)
           {faxis=fs*(k-m2);
            fprintf(fp,"%f,%f\n",faxis,10.*log10(psdr[k]));
            }
        fclose(fp);
        return;
}
*/