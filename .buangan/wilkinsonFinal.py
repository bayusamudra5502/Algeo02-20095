from math import isclose, sqrt
from numpy.random.mtrand import randint
import scipy as sp
import numpy as np
from scipy.linalg.decomp import hessenberg
import time
import math

# def Eig(A):
#     # A Matrix simetrik dan persegi
#     # Ubah ke bentuk tridiagonal
#     A = hessenberg(A)
#     m, n = A.shape
#     # simpan diagonal dan subdiagonal dalam array
#     diag = np.float64(np.copy(np.diag(A)))
#     sub_diag = np.float64(np.zeros(n))
#     for i in range(n-1):
#         sub_diag[i] = A[i][i+1]
#     sub_diag[n-1] = 0
#     limits = 30
#     Q = np.identity(n)



A = np.random.randint(0,255,size=(4, 4))
A = (np.float64(A)@((np.float64(A)).T))
ppp = np.copy(A)
rows, n = A.shape
A, QQ = hessenberg(A,calc_q=True)
e = np.float64(np.zeros(n))
d = np.float64(np.zeros(n))
d = np.float64(np.copy(np.diag(A)))
for i in range(n-1):
    e[i] = A[i][i+1]
n = len(d)
e[n-1] = 0
iterlim = 2 * 15
z = np.identity(n)
# o = np.identity(n)
start = time.time()
for l in range(n):
    # print(l)
    j = 0
    while 1:
        m = l
        while 1:
            # look for a small subdiagonal element
            if m + 1 == n:
                break
            if np.abs(e[m]) <= 1e-20 * (np.abs(d[m]) + np.abs(d[m + 1])):
                break
            m = m + 1
        if m == l:
            break

        if j >= iterlim:
            raise RuntimeError("tridiag_eigen: no convergence to an eigenvalue after %d iterations" % iterlim)

        j += 1

        # form shift

        p = d[l]
        g = (d[l + 1] - p) / (2 * e[l])
        r = np.hypot(g, 1)

        if g < 0:
            s = g - r
        else:
            s = g + r

        g = d[m] - p + e[l] / s

        s, c, p = 1, 1, 0

        for i in range(m - 1, l - 1, -1):
            f = s * e[i]
            b = c * e[i]
            if np.abs(f) > np.abs(g):             # this here is a slight improvement also used in gaussq.f or acm algorithm 726.
                c = g / f
                r = np.hypot(c, 1)
                e[i + 1] = f * r
                s = 1 / r
                c = c * s
            else:
                s = f / g
                r = np.hypot(s, 1)
                e[i + 1] = g * r
                c = 1 / r
                s = s * c
            g = d[i + 1] - p
            r = (d[i] - g) * s + 2 * c * b
            p = s * r
            d[i + 1] = g + p
            g = c * r - b

                # calculate eigenvectors
            # print(z)
            # print(o)
            # for w in range(o.shape[0]):
            #     f = o[w,i+1]
            #     o[w,i+1] = s * o[w,i] + c * f
            #     o[w,i  ] = c * o[w,i] - s * f
            # print(o)
            # if(j<n-1): 
            z[:,i:i+2] = (z[:,i:i+2]).dot(np.array([[c,s],[-s,c]]))
            # else: z[:,j] = c * z[:,i] - s * z[:,i+1]
            # print(z)

        d[l] = d[l] - p
        e[l] = g
        e[m] = 0
end = time.time()
print(end-start)
# for ii in range(1, n):
#     # sort eigenvalues and eigenvectors (bubble-sort)
#     i = ii - 1
#     k = i
#     p = d[i]
#     for j in range(ii, n):
#         if d[j] >= p:
#             continue
#         k = j
#         p = d[k]
#     if k == i:
#         continue
#     d[k] = d[i]
#     d[i] = p

#     for w in range(z.rows):
#         p = z[w,i]
#         z[w,i] = z[w,k]
#         z[w,k] = p
# z = z.T[np.argsort(d)].T
# d = np.sort(d)
# # start = time.time()
# # eigen = np.linalg.eig(A)
# # end = time.time()
# # print(end-start)
# # v = eigen[0]
# # w = eigen[1]
# # # print(v)
# # w = w.T[np.argsort(v)]
# # v = np.sort(v)
# # print(eigen[0])
# # print(eigen[1])
# # print(d)
# # print(z)
# # print(w)
z=QQ@z
for i in range(n):
    if(not(np.allclose(np.abs(ppp@z[:,i]-d[i]*z[:,i]),np.zeros(n)))):
        print(ppp@z[:,i]-d[i]*z[:,i])
        
# print(np.isclose(v, d))
# print(np.isclose(w, z))