import numpy as np
import math
from matplotlib import pyplot as plt 
import task1_2

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

def encode(states,d,termBits):
    """Encode input data using states"""
    dataWithTermBits = np.concatenate((d,np.zeros(termBits,dtype="int")))
    c = np.zeros(len(dataWithTermBits)*2,dtype="int")
    state = 0
    for i in range(len(dataWithTermBits)):
        #Add bits to code word
        c[i*2:i*2+2] = getCodeword(states,state,dataWithTermBits[i]) 
        #set next state
        state = nextState(states,state,dataWithTermBits[i])
    return c

def hammingDist(a,b):
    """Calculate hamming distance"""
    dist = 0
    for i in range(len(a)):
        #check if bits match
        if a[i] != b[i] and a[i] != -1 and b[i] != -1:
            #count unmatched bits
            dist += 1
    return dist

def decode(states,v,termBits):
    """decode a convolutional code using Viterbi decoder"""
    #working list for the decoded path, path[decoded bit][state][weight,bit,previous]
    path = np.array([[[math.inf,-1,-1]]*8]*(len(v)//2))
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
                    path[i+1][nextState][2] = j

    for i in range(len(path[-1][1:])):
        path[-1][i+1][0] = math.inf 


    decoded = np.zeros(len(path[:]),dtype="int")

    #loop backwards through path variable to reconstruct data
    prevState = 0
    for i in range(len(path[:])-1,0,-1):
        
        decoded[i-1] = path[i][prevState][1]
        prevState = int(path[i][prevState][2])
    return decoded[:-termBits]

def generateError(c,p):
    e = np.zeros(len(c))
    for i in range(len(c)):
        if np.random.random() < p:
            e[i] = 1
    return np.remainder(e+c,2)

k = 800

dbs = np.linspace(-5,10,25)

results = np.zeros((3,len(dbs)))
results[0] = dbs
testNum = 0
for i in dbs:
    print(testNum)
    for j in range(500):

        #simulate channel and code
        d = np.random.randint(0,2,k)
        c = encode(states,d,4)
        v = task1_2.bpsk(i,c)
        corrected = decode(states,v,4)
        
        uncoded = task1_2.bpsk(i,d)

        #check for and count errors
        errors = 0
        uncodedErrors = 0
        for bit in range(len(d)):
            if d[bit] != corrected[bit]:
                errors += 1
            if d[bit] != uncoded[bit]:
                uncodedErrors += 1
        results[1][testNum] += errors/500/k
        results[2][testNum] += uncodedErrors/500/k
 
    testNum += 1

plt.title("BER vs Probability of error")
plt.xlabel("Eb/N0")
plt.ylabel("BER")
plt.yscale("log")
plt.plot(results[0],results[1],label="Convolutional code")
plt.plot(results[0],results[2],label="No code")

plt.legend()
plt.grid(which="minor",axis="both")

plt.show()
