from math import sqrt
from numpy.random.mtrand import randint
import scipy as sp
import numpy as np
from scipy.linalg.decomp import hessenberg
import time
import math

def Givens(p, q):
    if(np.abs(q)<1e-5):
        c = 1
        s = 0
    else:
        if(np.abs(p)>np.abs(q)):
            tau = -p/q
            s = 1/np.sqrt(1+tau*tau)
            c = s*tau
        else:
            tau = -q/p
            c = 1/np.sqrt(1+tau*tau)
            s = c*tau
    return c, s

pp = np.random.randint(1,4,size=(4, 4))
pp = (np.float64(pp)@((np.float64(pp)).T))
pp = hessenberg(pp)
a = np.float64(np.diag(pp))
a.flags['WRITEABLE'] = True
m = n = a.shape[0]-1
n+=1
b = np.float64(np.zeros(n))
for i in range(1, n):
    b[i] = pp[i][i-1]

Q = np.identity(n)
cnt = 0
while m > 0:
    d =  (a[m-1]-a[m])/2
    if(np.abs(d)<1e-5):
        s = a[m]-np.abs(b[m])
    else:
        s = a[m]-(b[m]*b[m])/(d+np.sign(d)*np.hypot(d, b[m]))
    x = a[0]-s
    y = b[1]
    for k in range(m):
        if m>2:
            c, s = Givens(x, y)
        else:
            tt = a[k]
            uu = b[k+1]
            vv = a[k+1]
            if(np.abs(uu)<1e-8):
                s = 0
                c = 1
            else:
                deg = math.atan(-4*uu/(tt-vv))/2
                s = math.sin(deg)
                c = math.cos(deg)
                print(c, s)
        w = c*x-s*y
        d = a[k]-a[k+1]
        z = (2*c*b[k+1]+d*s)*s
        # print(b[k+1])
        a[k] = a[k]-z
        a[k+1] = a[k+1] +z
        b[k+1] = d*c*s+(c*c-s*s)*b[k+1]
        x = b[k+1]
        if k>0:
            b[k] = w
        if k<m-2:
            y = -s*b[k+2]
            b[k+2] = c*b[k+2]
        xx = np.zeros((2,2))
        xx[0][0] = c
        xx[0][1] = s
        xx[1][0] = -s
        xx[1][1] = c
        # print(xx)
        Q[:,k:k+2] = Q[:,k:k+2]@xx
    print(b[m])
    print(np.abs(a[m-1])+np.abs(a[m]))
    if np.abs(b[m])<(1e-100*(np.abs(a[m-1])+np.abs(a[m]))):
        # print(a)
        m = m-1
    print(m)

print(Q)
mm, zz = np.linalg.eigh(pp)
print(mm)
print(a)

