import numpy as np

if __name__=="__main__":
    a=np.array([[1,3,4],[3,1,4],[4,4,4]])
    print(a)
    # cov=np.cov(a)
    eig_val, eig_vec = np.linalg.eig(a)
    print(eig_val)
    print(eig_vec)