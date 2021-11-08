import numpy as np
import scipy as sp
from scipy.linalg.decomp import hessenberg

A = np.random.randint(100,255,size=(4, 4))
A = (np.float64(A)@((np.float64(A)).T))
p, q = np.linalg.eig(A)
print(q)
A = hessenberg(A)
p, q = np.linalg.eig(A)
print(q)
