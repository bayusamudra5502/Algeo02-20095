from math import sqrt
from numpy.random.mtrand import randint
import scipy as sp
import numpy as np
from scipy.linalg.decomp import hessenberg
import time
import math


def Set_Zeros(A):
    n = A.shape[1]
    Infinity_Norm = 0
    Infinity_Norm = np.abs(A[0][0]) if (np.abs(A[0][0])>Infinity_Norm) else Infinity_Norm
    for i in range(n-1):
        if(np.abs(A[i][i+1])<(np.abs(A[i][i])+np.abs(A[i+1][i+1]))*1e-12):
            A[i][i+1] = 0
        Infinity_Norm = np.abs(A[i][i+1]) if (np.abs(A[i][i+1])>Infinity_Norm) else Infinity_Norm
        Infinity_Norm = np.abs(A[i+1][i+1]) if (np.abs(A[i+1][i+1])>Infinity_Norm) else Infinity_Norm
    for i in range(n):
        if(np.abs(A[i][i])< Infinity_Norm*1e-12):
            A[i][i] = 0
    return A


def Searching_For_Diagonal_Matrix(A):
    n = A.shape[1]
    i = n-1
    for k in range(n-1, 0, -1):
        if(np.abs(A[k-1][k])>1e-5):
            break
        i-=1
    if(i==0):
        return True, -1,-1
    k1 = i
    while i>0:
        if(np.abs(A[i-1][i])<1e-5):
            break
        i-=1
    k2 = i
    # print(k1, k2)
    return False, k1, k2

def Givens(x0, x1):
    if(np.abs(x1)<1e-9):
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

def If_Diagonal_Zero(A,k,p,q):
    m, n = A.shape
    min = p
    max = n-q-1
    for t in range(k+1, max+1):
        a = A[k][t]
        b = A[t][t]
        x0 = a
        x1 = b
        x0, x1 =Givens(x0, x1)
        A[k][t] = x0*a+x1*b
        A[t][t] = -x1*a+x0*b
        if(t<max):
            a = A[k][t+1]
            b = A[t][t+1]
            A[k][t+1] = x0*a+x1*b
            A[t][t+1] = -x1*a+x0*b
    return A
        
def Wilkinson_Step(A):
    m, n = A.shape
    min = p
    max = n-q-1
    Alpha =A[max][max] * A[max][max] + A[max - 1][max] * A[max - 1][max]
    if(max-min>1):
        Delta = A[max - 1][max - 1] * A[max - 1][max - 1] + A[max - 2][max - 1] * A[max - 2][max - 1]
    elif (max==min+1):
        Delta = A[max - 1][max - 1] * A[max - 1][max - 1]
    else:
        return A
    Delta = (Delta-Alpha)/2
    Beta = A[max-1][max-1]*A[max-1][max]
    if(Delta>=0):
        Miu = Delta+np.hypot(Delta, Beta)
    else:
        Miu = Delta-np.hypot(Delta, Beta)
    Miu = Alpha-Beta*Beta/Miu
    y = A[min][min]*A[min][min]-Miu
    z = A[min][min]*A[min][min+1]
    for k in range(1, max-min+1):
        G0 = y
        G1 = z
        G0, G1 = Givens(G0, G1)
        c = G0
        s = -G1
        if(k>1):
            A[min+k-2][min+k-1] = c*y-s*z
        y = c * A[min + k - 1][min + k - 1] - s * A[min + k - 1][min + k]
        z = -s * A[min + k][min + k]
        A[min + k - 1][min + k] = s * A[min + k - 1][min + k - 1] + c * A[min + k - 1][min + k]
        A[min + k][min + k] *= c

        G0 = y
        G1 = z
        G0, G1 = Givens(G0, G1)
        c = G0
        s = -G1
        A[min+k-1][min+k-1] = c*y-s*z
        if (k < max - min):
            y = c * A[min + k - 1][min + k] - s * A[min + k][min + k]
            z = -s * A[min + k][min + k + 1]
            A[min + k][min + k + 1] *= c
            A[min + k][min + k] = s * A[min + k - 1][min + k] + c * A[min + k][min + k]
        else:
            a = A[min + k - 1][min + k]
            b = A[min + k][min + k]
            A[min + k - 1][min + k] = c * a - s * b
            A[min + k][min + k] = s * a + c * b
    return A

A = np.random.randint(100,255,size=(1000, 1000))
A = (np.float64(A)@((np.float64(A)).T))
A = hessenberg(A)
m, n = A.shape
q = 0
p = n
start = time.time()
while True:
    A = Set_Zeros(A)
    boo, k1, k2 = Searching_For_Diagonal_Matrix(A)
    if boo:
        break
    p = k2
    q = n-k1-1
    min = p
    max = n - q - 1
    flag = False
    for k in range(max-1, min-1, -1):
        if (np.abs(A[k][k])<1e-7):
            flag = True
            A = If_Diagonal_Zero(A, k, p, q)
            break
    if flag:
        continue
    A = Wilkinson_Step(A)
    # print(A)
    # print(p, q)
end = time.time()
print(end-start)
start = time.time()
o, q = np.linalg.eig(A)
end = time.time()
print(np.diag(A), o)
print(end-start)


