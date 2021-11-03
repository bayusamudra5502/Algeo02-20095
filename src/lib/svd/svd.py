import numpy as np
from numpy.core.fromnumeric import compress
import sklearn.preprocessing
from PIL import Image
from matplotlib import pyplot as PLT
import pandas as pd

def image_to_rgba(filePath):
    with Image.open(filePath) as im:
        return np.array(im.convert("RGBA"))

def inspectColor(Im):
    return Im[:,:,0], Im[:,:,1], Im[:,:,2], Im[:,:,3] 

def concatColor(R, G, B, A):
    return np.array([R, G, B, A])

def colorToImage(M):
    PLT.imshow(M)
    PLT.show()

def build_decom(A: np.ndarray):
    l = A@(A.T)
    r = (A.T)@A

    #generate eigenvector with their corresponding eigenval
    l_eigval, l_eig = np.linalg.eigh(l)
    r_eigval, r_eig = np.linalg.eigh(r)

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

def compress_to_k(A, k):
    u, sigm, v = build_decom(A)
    # rows, cols = A.shape
    # sigm = np.pad(np.diag(sigm), ((0,rows),(0,cols)), mode='constant')[0:rows, 0:cols]
    return (u[:,:k]@(sigm[:k, :k]@v[:k, :]))


# M = image_to_rgba("data/B.jpeg")
# R, G, B, A = inspectColor(M)
# r, c = R.shape
# print(r,c)
# R = compress_to_k(R,r//100)
# G = compress_to_k(G,r//100)
# B = compress_to_k(B,r//100)
# A = compress_to_k(A,r//100)


# M = np.uint8((np.dstack((R, G, B, A))))
# #print(M)
# colorToImage(M)


    

