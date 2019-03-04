#include "math.h"
#include "mex.h"   //--This one is required

void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[]){
    int *b=(int*)malloc(sizeof(int)*100);
    #pragma omp parallel for
    for(int i=0;i<(int)100;i++){
    	int b[i]=i*i;
    }
    return b
}