from math import sqrt
from numpy.random.mtrand import randint
import scipy as sp
import numpy as np
from scipy.linalg.decomp import hessenberg
import time
import math

def givens_factors(x,y):
    h = np.sqrt(np.square(x)+np.square(y))
    return np.array([x,y])/h

Q = np.identity(4)
def qr_step_wilkinson(A):
    
    def shift(mat):
        [[am1,bm1],[bm1,am]] = mat[-2:,-2:]
        delta = (am1-am)/2
        s = max(np.sign(delta),1)
        return am-s*bm1*bm1/(np.abs(delta) + np.sqrt(delta*delta + bm1*bm1))
        
    
    givensfactors = []
    mu = shift(A)
    A -= np.diag(np.ones(A.shape[0])*mu)
    
    # R = G^T_n-1 ... G^T_1 * A  where G^T is the transpose of the givens matrix
    for i in range(len(A)-1):
        c,s = givens_factors(A[i,i],A[i+1,i])
        givensfactors.append([c,s])
        # j = i
        # Q[:,j:j+2] = (Q[:,j:j+2]).dot(np.array([[c,s],[-s,c]]))
        # Q[j:j+2,:] = np.array([[c,s],[-s,c]]).dot((Q[j:j+2,:]))
        A[i:i+2,i:] = np.array([[c,s],[-s,c]]).dot(A[i:i+2,i:])

    # print(Q)
    # A_k+1 = R * G_1 ... G_n-1
    for i,(c,s) in enumerate(givensfactors):
        # j = 4-len(A) + i
        # # j = i
        # Q[:,j:j+2] = (Q[:,j:j+2]).dot(np.array([[c,-s],[s,c]]))
        A[:i+2, i:i+2] = A[:i+2,i:i+2].dot(np.array([[c,-s],[s,c]]))
        # Q[:,j:j+2] = (Q[:,j:j+2]).dot(np.array([[c,-s],[s,c]]))

    A += np.diag(np.ones(A.shape[0])*mu)

    # print(A)
    return A
    
# def qr_step(A):
#     givensfactors = []

#     # R = G^T_n-1 ... G^T_1 * A  where G^T is the transpose of the givens matrix
#     for i in range(len(A)-1):
#         c,s = givens_factors(A[i,i],A[i+1,i])
#         givensfactors.append([c,s])
#         A[i:i+2,i:] = np.array([[c,s],[-s,c]]).dot(A[i:i+2,i:])

#     # A_k+1 = R * G_1 ... G_n-1
#     for i,(c,s) in enumerate(givensfactors):
#         A[:i+2, i:i+2] = A[:i+2,i:i+2].dot(np.array([[c,-s],[s,c]]))
#     # print(A)
#     return A


def qr(mat, qr_iteration=qr_step_wilkinson):
    mat = np.copy(mat)
    
    m,n = mat.shape
    niter = 0
    mxm1 = []
    diag = []
    diagonal = np.zeros(m)
    while True:
        
        mat = qr_iteration(mat)
        mxm1.append(np.abs(mat[m-1,m-2]))
        diagonal[0:m] = np.diag(mat)
        diag.append(np.asarray(list(diagonal)))
        niter += 1
        # print(mat)
        if mxm1[-1] < 1e-12:
            yield niter,mat,mxm1,diag
            mxm1 = []
            diag = []
            # print(mat)
            mat = mat[:-1,:-1]
            m,n = mat.shape
            if m < 2:
                yield 0,mat,[],[]
                return
            niter = 0


def driver(mat,qr_iteration=qr_step_wilkinson):
    H = hessenberg(mat)
    evals = []
    ntotal = 0
    mxm1s = []
    diags = []
    for niter,T,mxm1,diag in qr(H,qr_iteration=qr_iteration):
        evals.append(T[-1,-1])
        ntotal += niter
        mxm1s.extend(mxm1)
        diags.extend(diag)
    return evals,[list(range(ntotal)),mxm1s],np.asarray(diags)

p = np.random.randint(100,255,size=(1000, 1000))
p = (np.float64(p)@((np.float64(p)).T))
# # p = hessenberg(p)
start = time.time()
# # eigen = np.linalg.eigh(p)
eigen2 = np.linalg.eigh(p)
# print(eigen2[1])
end = time.time()
# print("bawaan python: \n", sorted(eigen2[0]))
print("waktu: ", end-start)
start = time.time()

evals,semiology,diags = driver(p,qr_iteration=qr_step_wilkinson)

end = time.time()
# print("punya kita: \n", sorted(diags[-1,:]))
print("waktu: ", end-start)
# print(evals)
# print(semiology)
print("sama?:", np.allclose(sorted(diags[-1,:]), sorted(eigen2[0])))
# v = eigen2[1]
# print(np.divide((p@v[:,0]), v[:,0]))
# print(v)
# print(Q)
# print(np.divide((p@Q[0,:]), Q[0,:]))
# print(np.divide((p@Q[:,0]), Q[:,0]))

# print(eigen2[0])
# print(evals)