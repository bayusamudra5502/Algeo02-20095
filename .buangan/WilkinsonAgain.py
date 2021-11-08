from math import sqrt
from numpy.random.mtrand import randint
import scipy as sp
import numpy as np
from scipy.linalg.decomp import eig, hessenberg
import time
import math

A = np.random.randint(100,255,size=(4, 4))
A = (np.float64(A)*((np.float64(A)).T))
# u0, uu0 = np.linalg.eig(A)
# v0, vv0 = np.linalg.eigh(A)
# print(uu0)
# print(vv0)
# print(A)
# A = hessenberg(A)
rows, n = A.shape
e = np.float64(np.zeros(n+1))
d = np.float64(np.zeros(n+1))
# z = np.zeros((n+1, n+1))
# for i in range(n):
#     for j in range(n):
#         z[i+1][j+1] = A[i][j]
# # print(z)
# for i in range(n, 1, -1):
#     if(i>1): l = i-2
#     f = z[i][i-1]
#     g = 0
#     for k in range(1, l+1):
#         g = g+z[i][k]*z[i][k]
#         h = g+f*f
#         if(np.abs(g-1e-20)<1e-12):
#             e[i] = f
#             h = 0
#             d[i] = h
#             break
#         l = l+1
#         if(f>0 or np.abs(f)<1e-9):
#             e[i] = -np.sqrt(h)
#             h = -np.sqrt(h)
#         else:
#             e[i] = np.sqrt(h)
#             h = np.sqrt(h)
#         h = h-f*g
#         if i>1:
#             z[i][i-1] = f-g
#         f = 0
#         for j in range(1, l+1):
#             z[j][i] = z[i][j]/h
#             g = 0
#             for k in range(1, j+1):
#                 g = g+z[j][k]*z[i][k]
#             for k in range(j+1, l+1):
#                 g = g+z[k][j]*z[i][k]
#             e[j] = g/h
#             f = f+g*z[j][i]
#         hh = f/(2*h)
#         for j in range(1, l+1):
#             f = z[i][j]
#             g = e[j]-hh*f
#             e[j] = g
#             for k in range(1, j+1):
#                 z[j][k]=z[j][k]-f*e[k]-g*z[i][k]
# d[1]=e[1] = 0
# for i in range(1,n+1):
#     l = i-1
#     if(np.abs(d[i])>1e-7 and l>0):
#         for j in range(1, l+1):
#             g = 0
#             for k in range(1, l+1):
#                 g = g+z[i][k]*z[k][j]
#             for k in range(1, l+1):
#                 z[k][j] = z[k][j]-g*z[k][i]
#         d[i] = z[i][i]
#         z[i][i] = 1
#         for j in range(1, l+1):
#             z[i][j] =0
#             z[j][i] = 0
# print(A)
# print(z[1:,1:])
A = hessenberg(A)
# print(A)
# u, uu = np.linalg.eig(A)
# v, vv = np.linalg.eigh(A)
# print(uu0)
# print(vv0)
d = np.float64(np.copy(np.diag(A)))
d = np.insert(d, 0, np.float64(0))
print(A)
for i in range(n-1):
    e[i+1] = A[i][i+1]
e[n] = 0
# print(e)
# k = n-1
for j in range(1, n+1):
    its = 0
    for m in range(j, n):
        while(not(np.abs(e[m])<1e-3*(np.abs(d[m])+np.abs(d[m+1])))):
            u = d[j]
            if(m!=j):
                # if(its == 30) 
                its = its+1
                q = (d[j+1]-u)/(2*e[j])
                t = np.hypot(1, q)
                if(np.abs(q)<1e-8):
                    q = d[m]-u+e[j]/(q+t)
                else:
                    q = d[m]-u+e[j]/(q+np.sign(q)*t)
                u = 0
                s = 1
                c = 1
                for i in range(m-1, j-1,-1):
                    p = s*e[i]
                    h = c*e[i]
                    if(np.abs(p)>=np.abs(q)):
                        c = q/p
                        t = np.hypot(c, 1)
                        e[i+1] = p*t
                        s = 1/t
                        c = c*s
                    else:
                        s = p/q
                        t = np.hypot(s, 1)
                        e[i+1] = q*t
                        c = 1/t
                        s = s*c
                    q = d[i+1]-u
                    t = (d[i]-q)*s+2*c*h
                    u = s*t
                    d[i+1]=q+u
                    q = c*t-h
                d[j] = d[j]-u
                e[j] = q
                e[m] = 0
    m = n
eigen = np.linalg.eigh(A)
eigen2 = np.linalg.eig(A)
print(eigen[0])
print(eigen2[0])
print(d)
# d = d[1:]
# x = eigen2[0]*np.identity(n)
# print(d)
# print(np.linalg.det(A-d)-np.prod(eigen2[0]))

