import numpy as np
import sklearn.preprocessing


def build_decom(A):
    l = A@(A.T)
    r = (A.T)@A

    #generate eigenvector with their corresponding eigenval
    l_eigval, l_eig = np.linalg.eig(l)
    r_eigval, r_eig = np.linalg.eig(r)

    #shaping matrix
    rows, cols = A.shape
    r_sigmum = np.sqrt(np.abs(r_eigval))
    l_sigmum = np.sqrt(np.abs(l_eigval))
    r_sort_pivot = np.argsort(-1*r_sigmum)
    l_sort_pivot = np.argsort(-1*l_sigmum)
    sigm = np.pad(np.diag(r_sigmum[r_sort_pivot]), ((0,rows),(0,cols)), mode='constant')[0:rows, 0:cols]

    # sorting & normalizing right singular            
    r_singular = r_eig.T[r_sort_pivot]
    sklearn.preprocessing.normalize(r_singular, norm="l2", axis=1, copy=False)

    # sorting & correlate right singular with left singular & dinomalisasi
    l_singular = l_eig[:,l_sort_pivot]
    i = 0
    for x in r_sigmum:
        if(abs(x)>np.finfo(float).eps and i<min(l_singular.shape[0],r_singular.shape[0])):
            l_singular[:,i] = (A@r_singular[i,:])*(1/x)
            i+=1
    l_singular = l_singular.T
    sklearn.preprocessing.normalize(l_singular, norm="l2", axis=1, copy=False)
    l_singular = l_singular.T
    
    return l_singular, sigm, r_singular

    
    

