from math import sqrt
from numpy.random.mtrand import randint
import scipy as sp
import numpy as np
from scipy.linalg.decomp import hessenberg
import time
import math

def givens(x0, x1):
    if(np.abs(x1)<1e-6):
        x0 = 1
    else:
        if(np.abs(x1)>np.abs(x1)):
            tau = x0/x1
            x1 = 1/np.hypot(1, tau)
            x0 = x1*tau
        else:
            tau = x1/x0
            x0 = 1/np.hypot(1, tau)
            x1 = x0*tau
    return x0, x1

A = np.random.randint(100,255,size=(4, 4))
A = (np.float64(A)*((np.float64(A)).T))
# u0, uu0 = np.linalg.eig(A)
# v0, vv0 = np.linalg.eigh(A)
# print(uu0)
# print(vv0)
# print(A)
A = hessenberg(A)
print(A)
# print(A)
# u, uu = np.linalg.eig(A)
# v, vv = np.linalg.eigh(A)
# print(uu0)
# print(vv0)
m, n = A.shape
Q = np.float64(np.identity(n))
a = np.float64(np.copy(np.diag(A)))
a = np.insert(a, 0, np.float64(0))
b = np.float64(np.zeros(n+1))
for i in range(n-1):
    b[i+2] = A[i][i+1]

iter = 0
while m>1:
    if(iter>10000):
        break
    d = (a[m-1]-a[m])/2

    if(np.abs(d)<1e-6):
        mu = a[m]-np.abs(b[m])
    else:
        mu = a[m] - (b[m]*b[m])/(d+(np.sign(d)*np.hypot(d, b[m])))
    x = a[1]*a[1]-mu
    y = b[2]*a[2]
    for k in range(1, m):
        if m>2:
            c, s = givens(x, y)
        else:
            p = a[1]
            q = b[2]
            r = a[2]
            if(np.abs(p-r)<1e-6):
                c = 1/np.hypot(1,1)
                s = 1/np.hypot(1,1)
            else:
                theta = math.atan(2*q/(r-p))/2
                c = math.cos(theta)
                s = math.sin(theta)
        w = c*x-s*y
        d = a[k]-a[k+1]
        z = (2*c*b[k+1]+d*s)*s
        a[k] = a[k]-z
        a[k+1] = a[k+1]+z
        b[k+1] = d*c*s + (c*c-s*s)*b[k+1]
        x = b[k+1]
        if k>1:
            b[k]=w
        if k<m-1:
            y = -s*b[k+2]
            b[k+2] = c*b[k+2]
        G = np.array([[c,s],[-s,c]])
        Q[:,k-1:k+1] = Q[:,k-1:k+1]@G
    if(np.abs(b[m])<1e-20*(np.abs(a[m-1])+np.abs(a[m]))):
        m -=1
    # print(a)
    # print(b)
    iter+=1
eigen = np.linalg.eigh(A)
eigen2 = np.linalg.eig(A)
print(eigen[0])
print(eigen2[0])
print(a)

# c, s = givens(1000, 0)
# xxx = np.array([[c, s], [-s, c]])
# yyy = np.array([[1000],[0]])
# print(c, s)
# print(xxx@yyy)

# p = a[1]
# q = b[2]
# r = a[1]
# aaa = np.array([[p,q], [q,r]])
# print(aaa)
# if(np.abs(p-r)<1e-6):
#     c = 1/np.hypot(1,1)
#     s = 1/np.hypot(1,1)
# else:
#     theta = math.atan(2*q/(r-p))/2
#     c = math.cos(theta)
#     s = math.sin(theta)
# bbb = np.array([[c, -s], [s, c]])
# ccc = np.array([[c, s], [-s, c]])
# print((bbb@aaa@ccc))