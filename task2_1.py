import numpy as np
import math

states = (((0,0),(1,1),(0,4)),
          ((1,1),(0,0),(0,4)),
          ((1,0),(0,1),(1,5)),
          ((0,1),(1,0),(1,5)),
          ((0,1),(1,0),(2,6)),
          ((1,0),(0,1),(2,6)),
          ((1,1),(0,0),(3,7)),
          ((0,0),(1,1),(3,7)))

def nextState(states,prev,input):
    return states[prev][2][input]

def getCodeword(states,prev,input):
    return states[prev][input]

def encode(states,d):
    c = np.zeros(len(d)*2,dtype="int")
    state = 0
    for i in range(len(d)):
        c[i*2:i*2+2] = getCodeword(states,state,d[i])
        state = nextState(states,state,d[i])
    return c

k = 800
termBits = 3

d = np.random.randint(0,2,k+termBits)

d[-3:] = 0,0,0

print(d)
print()
c = encode(states,d)
