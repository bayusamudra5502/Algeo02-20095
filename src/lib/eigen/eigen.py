from math import isclose, sqrt
from numpy.random.mtrand import randint
import scipy as sp
import numpy as np
from scipy.linalg.decomp import hessenberg
import time
import math

def EigenV(mat, precision = 30):
    m, n = mat.shape
    H, Q = hessenberg(mat, calc_q=True)
    sub = np.float64(np.copy(np.diag(H,-1)))
    diag = np.float64(np.copy(np.diag(H)))
    sub = np.insert(sub, n-1, 0)
    limit = precision
    for i in range(n):
        niter = 0
        while niter<limit:
            j = i
            while j+1!=n and  np.abs(sub[j]) > 1e-20*(np.abs(diag[j])+np.abs(diag[j+1])):
                j += 1
            if(j==i):
                break
            else:
                niter += 1
                g = (diag[i + 1]-diag[i])/(2*sub[i])
                r = np.hypot(g, 1)
                if(np.abs(g)<1e-9):
                    g = diag[j]-diag[i]+(sub[i]/(g+r))
                else:
                    g = diag[j]-diag[i]+(sub[i]/(g + np.sign(g)*r))

                # rotasi givens
                s = 1
                c = 1
                p = 0
                for k in range(j-1, i-1, -1):
                    f = s*sub[k]
                    b = c*sub[k]
                    if(np.abs(f) > np.abs(g)):
                        c = g/f
                        tau = np.hypot(c, 1)
                        sub[k+1] = f*tau
                        s = 1/tau
                        c *= s
                    else:
                        s = f/g
                        tau = np.hypot(s, 1)
                        sub[k+1] = g*tau
                        c = 1/tau
                        s *= c
                    g = diag[k+1]-p
                    r = 2*b*c+(diag[k]-g)*s
                    p = r*s
                    diag[k+1] = g+p
                    g = r*c-b
                    # eigenvector
                    Q[:,k:k+2] = (Q[:,k:k+2]).dot(np.array([[c,s],[-s,c]]))
                sub[i] = g
                sub[j] = 0
                diag[i] = diag[i]-p
    return diag, Q


# TESTING MODUL
# A = np.random.randint(0,255,size=(100, 100))
# A = (np.float64(A)@((np.float64(A)).T))
# rows = A.shape[0]
# start = time.time()
# pp, qq = EigenV(A)
# end = time.time()
# print("waktu: ", end-start)
# sama = True
# for i in range(rows):
#     if(not(np.allclose(np.abs(A@qq[:,i]-pp[i]*qq[:,i]).astype(int),np.zeros(rows)))):
#         print(A@qq[:,i]-pp[i]*qq[:,i])
#         sama = False
#         print("Yahh, ada yang beda,, ^ itu ketidaktelitiannya ya")
#         break
# if(sama):
#     print("Wow, sama semua!")

# TESTING NORM
# A = np.random.randint(0,255,size=(100, 100))
# A = (np.float64(A)@((np.float64(A)).T))
# pp, qq = EigenV(A)
# for i in range(A.shape[0]):
#     print(np.linalg.norm(qq[:,i]))