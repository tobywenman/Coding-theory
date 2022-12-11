import numpy as np
from matplotlib import pyplot as plt
import math
import task2_1 

def bec(p,c):
    r = np.zeros(len(c))
    for i in range(len(c)):
        if np.random.random() < p:
            r[i] = -1
        else:
            r[i] = c[i]
    return r