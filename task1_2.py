import task1_1
import numpy as np
import math
from matplotlib import pyplot as plt 

def dbtoabs(db):
    return 10**(db/10)

def bpsk(p,SNR,c):
    n = 2**(p)-1
    e = np.zeros(n)
    variance = 1/dbtoabs(SNR)/2

    #change bit values to signal
    for i in range(n):
        if c[i] == 0:
            c[i] = -1

    #generate error and add to sent word
    for i in range(n):
        e[i] = np.random.normal(scale=math.sqrt(variance))
    c += e
    #implement hard decoding
    for i in range(n):
        if c[i] < 0:
            c[i] = 0
        else:
            c[i] = 1
    return c

if __name__=="__main__": 
    dbs = np.linspace(-10,5,50)
    result = task1_1.simulate(4,dbs,1000,bpsk,task1_1.encode,task1_1.decode)

    plt.title("BER vs Eb/N0")
    plt.xlabel("Eb/N0")
    plt.ylabel("BER")
    plt.yscale("log")
    plt.plot(result[0],result[1])

    plt.show()