import numpy as np
import math

def generatorMatrix(p):
    n = 2**(p)-1
    k = n-p
    P = np.zeros((k,p),int)

    row = 0
    for i in range(1,n+1):
        binary = "{0:b}".format(i)
        binary =list("0"*(n-k-len(binary)) + binary)
        binary =  np.int_(binary)
        if np.count_nonzero(binary) > 1:
            P[row] = binary
            row += 1
    return np.concatenate((np.identity(k),P),axis=1)

    


print(generatorMatrix(3))