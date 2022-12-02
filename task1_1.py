import numpy as np
import math

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

# print(generatorMatrix(4))
# print(parityCheckMatrix(generatorMatrix(4)))
d = np.random.randint(0,2,11)
G = generatorMatrix(4)
H = parityCheckMatrix(G)

lookup = generateSyndromes(H)

print(d)
c = encode(d,G)
print(c)
v = np.remainder(c+np.array([0,0,1,0,0,0,0,0,0,0,0,0,0,0,0]),2)

print(decode(H,v,lookup))
# for i in lookup:
#     print(i, lookup[i])

