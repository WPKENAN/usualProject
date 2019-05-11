import numpy as np

if __name__=="__main__":
    np.random.seed(0)
    samples = 1000;
    H=np.zeros((2,2,10));
    Y_all=np.random.rand(samples,2,10)+10;
    X_all=np.random.rand(samples,2,10)+5;
    V_all=np.random.rand(samples,2,10);

    #y0(0)=h00(0)*x0(0)+h01(0)*x1(0)+v0(0)
    y=np.zeros((samples,1));
    x=np.zeros((samples,2));
    v=np.zeros((samples,1));
    for i in range(2):
        for j in range(10):
            for k in range(samples):
                y[k,0]=Y_all[k,i,j];
                x[k,0]=X_all[k,0,j];
                x[k,1] = X_all[k, 1, j];
                v[k,0]=V_all[k,i,j];
            h=np.linalg.lstsq(x,y-v)[0]
            # print("[h{}1({}) h{}2({})]=".format(i,j,i,j),h);
            H[i,0,j]=h[0,0];
            H[i,1,j]=h[1,0];
    Y_received=np.zeros((samples,2,10));
    for i in range(samples):
        Y_received[i, 0, :] = H[0, 0] * X_all[i, 0, :] + H[0, 1] * X_all[i, 1, :] + V_all[i, 0, :];
        Y_received[i, 1, :] = H[1, 0] * X_all[i, 0, :] + H[1, 1] * X_all[i, 1, :] + V_all[i, 1, :];

    print("H00: ", list(H[0, 0, :]))
    print("H01: ", list(H[0, 1, :]))
    print("H10: ", list(H[1, 0, :]))
    print("H11: ", list(H[1, 1, :]))
    print("方差: {}".format(np.var(Y_received-Y_all)))
















