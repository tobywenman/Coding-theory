import numpy as np
import math
from matplotlib import pyplot as plt 

def generatorMatrix(p):
    """Create Generator matrix for hamming code"""

    #calculate n and k from p
    n = 2**(p)-1 
    k = n-p

    #Initalise P matrix
    P = np.zeros((k,p),int)

    #populate P matrix
    row = 0
    for i in range(1,n+1):
        binary = "{0:b}".format(i)
        binary =list("0"*(n-k-len(binary)) + binary)
        binary =  np.int_(binary)
        #remove rows with only 1 1 to allow systematic matrix
        if np.count_nonzero(binary) > 1:
            P[row] = binary
            row += 1
    #Return matrix and add identity 
    return np.concatenate((np.identity(k),P),axis=1)

def parityCheckMatrix(G):
    """Convert generator matrix into parity matrix"""
    p = G.shape[1]-G.shape[0]
    P = G[:,-p:]
    H = np.zeros((p,G.shape[1]))
    H[:,:G.shape[1]-p] = np.transpose(P)
    H[:,G.shape[1]-p:] = np.identity(p)
    return H

def encode(d,G):
    """Encode data to transmitted data"""
    return np.remainder(np.matmul(d,G),2)

def calcSyndrome(H,c):
    """Find sydrome for a recieved word"""
    Ht = np.transpose(H)
    return tuple(np.remainder(np.matmul(c,Ht),2))

def generateSyndromes(H):
    n = np.shape(H)[1]
    lookup = {}
    lookup[(0.0,0.0,0.0,0.0)] = np.zeros(n)
    for i in range(n):
        e = np.zeros(n)
        e[i] = 1
        lookup[calcSyndrome(H,e)] = e
    return lookup

def decode(H,c,lookup):
    syndrome = calcSyndrome(H,c)
    k = np.shape(H)[1]-np.shape(H)[0]
    e = lookup[syndrome]
    return np.remainder(c+e,2)[:k]

def generateError(p,a):
    n = 2**(p)-1
    e = np.zeros(n)
    for i in range(n):
        if np.random.random() < a:
            e[i] = 1
    return e

def simulate(p,tests,iter):
    G = generatorMatrix(p)
    H = parityCheckMatrix(G)
    n = 2**(p)-1 
    k = n-p
    lookup = generateSyndromes(H)
    results = np.zeros((2,len(tests)))
    results[0] = tests
    testNum = 0
    for i in tests:
        for j in range(iter):
            d = np.random.randint(0,2,k)
            c = encode(d,G)
            e = generateError(p,i)
            #print(e)
            v = np.remainder(c+e,2)
            corrected = decode(H,v,lookup)
            errors = 0

            for bit in range(len(d)):
                if d[bit] != corrected[bit]:
                    errors += 1
            results[1][testNum] += errors/iter/k
        testNum += 1
    return results
            

result = simulate(4,np.arange(0,0.2,0.01),1000)
print(result)
plt.title("BER vs Probability of error")
plt.xlabel("P")
plt.ylabel("BER")
plt.plot(result)
plt.show()