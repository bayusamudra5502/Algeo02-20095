import numpy as np
import sklearn.preprocessing
# belum diimport, gatau gimanain:(


def build_decom(A: np.ndarray):
    l = A@(A.T)
    r = (A.T)@A
    
    #generate eigenvector with their corresponding eigenval
    l_eigval, l_eig = EigenV(l)
    r_eigval, r_eig = EigenV(r)

    #shaping matrix
    rows, cols = A.shape
    r_sigmum = np.sqrt(np.abs(r_eigval))
    l_sigmum = np.sqrt(np.abs(l_eigval))
    r_sort_pivot = np.argsort(-1*r_sigmum)
    l_sort_pivot = np.argsort(-1*l_sigmum)
    sigm = np.pad(np.diag(r_sigmum[r_sort_pivot]), ((0,rows),(0,cols)), mode='constant')[0:rows, 0:cols]

    # sorting right singular         
    r_singular = r_eig.T[r_sort_pivot]
    # sorting & correlate right singular with left singular & dinomalisasi
    l_singular = l_eig[:,l_sort_pivot]
    i = 0
    rank = 0
    for x in r_sigmum:
        if(abs(x)>np.finfo(float).eps):
            rank+=1
        if(abs(x)>np.finfo(float).eps and i<min(l_singular.shape[0],r_singular.shape[0])):
            l_singular[:,i] = (A@r_singular[i,:])*(1/x)
            i+=1
    l_singular = l_singular.T
    sklearn.preprocessing.normalize(l_singular, norm="l2", axis=1, copy=False)
    l_singular = l_singular.T
    return l_singular, sigm, r_singular, rank



A = np.random.randint(0,255,size=(10, 10))
A = build_decom(A)
# M = image_to_rgba("data/lena.png")
# R, G, B, A = inspectColor(M)
# R, G, B, A = compress_all(R, G, B, A, 90)
# M = np.uint8((np.dstack((R, G, B, A))))
# colorToImage(M)

    

