import numpy as np
import math

#variable holding the structure of the state machine (codeword bits for 0 input,codeword bits for 1 input,(state for 0, state for 1))
states = (((0,0),(1,1),(0,4)),
          ((1,1),(0,0),(0,4)),
          ((1,0),(0,1),(1,5)),
          ((0,1),(1,0),(1,5)),
          ((0,1),(1,0),(2,6)),
          ((1,0),(0,1),(2,6)),
          ((1,1),(0,0),(3,7)),
          ((0,0),(1,1),(3,7)))

def nextState(states,prev,input):
    """Return next state from state machine"""
    return states[prev][2][input]

def getCodeword(states,prev,input):
    """Return the bits added to the codeword"""
    return states[prev][input]

def encode(states,d):
    """Encode input data using states"""
    c = np.zeros(len(d)*2,dtype="int")
    state = 0
    for i in range(len(d)):
        #Add bits to code word
        c[i*2:i*2+2] = getCodeword(states,state,d[i]) 
        #set next state
        state = nextState(states,state,d[i])
    return c

def hammingDist(a,b):
    """Calculate hamming distance"""
    dist = 0
    for i in range(len(a)):
        #check if bits match
        if a[i] != b[i]:
            #count unmatched bits
            dist += 1
    return dist

def decode(states,v):
    """decode a convolutional code using Viterbi decoder"""
    #working list for the decoded path, path[decoded bit][state][weight,bit]
    path = np.array([[[math.inf,-1]]*8]*(len(v)//2))
    path[0][0][0] = 0

    #iterate through all bits
    for i in range(len(v)//2-1):

        #iterate through all states
        for j in range(8):

            #test both branches for 0 or 1 bit
            for k in [0,1]:

                #calculate extra hamming weight for current test
                weight = hammingDist(v[i*2:i*2+2],states[j][k])
                #lookup state relating to the tested bit
                nextState = states[j][2][k]

                #check if current test is better than previous weight
                if weight+path[i][j][0] < path[i+1][nextState][0]:
                    #update path variable
                    path[i+1][nextState][0] = weight+path[i][j][0]
                    path[i+1][nextState][1] = k

    decoded = np.zeros(len(path[:]),dtype=int)

    #loop backwards through path variable to reconstruct data
    for i in range(len(path[:])-1,0,-1):
        minWeight = math.inf
        for j in range(8):
            if path[i][j][0] < minWeight:
                minWeight = path[i][j][0]
                decoded[i-1] = path[i][j][1]
    return decoded


k = 800
termBits = 3

d = np.random.randint(0,2,k+termBits)

d[-3:] = 0,0,0

c = encode(states,d)

decoded = decode(states,c)
print(hammingDist(decoded,d))