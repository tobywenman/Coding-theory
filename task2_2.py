import numpy as np
from matplotlib import pyplot as plt
import math
import task2_1 

def bec(p,c):
    """Create a binary erasure channel, where erasures are -1"""
    r = np.zeros(len(c))
    for i in range(len(c)):
        if np.random.random() < p:
            r[i] = -1
        else:
            r[i] = c[i]
    return r

if __name__=="__main__":
    k=800
    tests = np.linspace(0,0.3,25)
    results = task2_1.simulate(k,task2_1.states,tests,100,bec)
    plt.title("BER vs Probability of error")
    plt.xlabel("P")
    plt.ylabel("BER")
    plt.yscale("log")
    plt.xlim(max(results[0]), min(results[0]))
    plt.plot(results[0],results[1],label="Convolutional code")
    plt.plot(results[0],results[2],label="No code")

    plt.legend()
    plt.grid(which="minor",axis="both")

    plt.show()