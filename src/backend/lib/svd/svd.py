import numpy as np
import sklearn.preprocessing
from api.state import State

from lib.eigen.eigen import EigenV

def gprocessd(value, channel):
    return {
        "func": 1,
        "channel": channel,
        "value": value/37
    }

def updater(state:State, channel, start, end, sendUpdate):
    if sendUpdate:
        def update(value):
            state.sendUpdateState(
                gprocessd(start + value*(end-start), channel), 
                "Menghitung Eigenvalue")

        return update
    else:
        return None

def build_decom(A: np.ndarray, *, state:State=None, channel="W", sendFeedback=False):
    r = (A.T)@A
    if sendFeedback:
        state.sendUpdateState(gprocessd(1,channel), "Proses Perkalian Matriks Selesai")
    
    #generate eigenvector with their corresponding eigenval
    if sendFeedback:
        state.sendUpdateState(gprocessd(2,channel), "Menghitung Nilai Eigen")


    if sendFeedback:
        state.sendUpdateState(gprocessd(13,channel), "Menghitung Nilai Eigen")
    
    r_eigval, r_eig = EigenV(r, updater=updater(state, channel, 13, 23, sendFeedback))

    #shaping matrix
    if sendFeedback:
        state.sendUpdateState(gprocessd(24,channel), "Membentuk Matriks SVD")

    rows, cols = A.shape
    r_sigmum = np.sqrt(np.abs(r_eigval))
    r_sort_pivot = np.argsort(-1*r_sigmum)
    sigm = np.pad(np.diag(r_sigmum[r_sort_pivot]), 
        ((0,rows),(0,cols)), mode='constant')[0:rows, 0:cols]

    # sorting right singular         
    r_singular = r_eig.T[r_sort_pivot]
    # sorting & correlate right singular with left singular & dinomalisasi
    l_singular = np.zeros((rows, rows))

    cnt = 0
    i = 0

    for x in r_sigmum:
        if sendFeedback and cnt % 50 == 0:
            state.sendUpdateState(gprocessd(25 + cnt/len(r_sigmum) * 10,channel), "Membentuk Matriks SVD")

        cnt += 1
        if(abs(x)>1e-9 and i<min(l_singular.shape[0],r_singular.shape[0])):
            l_singular[i:,] = (A@r_singular[i,:])*(1/x)
            i+=1

    
    if sendFeedback:
        state.sendUpdateState(gprocessd(36,channel), "Normalisasi Matriks")

    sklearn.preprocessing.normalize(l_singular, norm="l2", axis=1, copy=False)
    l_singular = l_singular.T

    rank = np.linalg.matrix_rank(A)
    if sendFeedback:
        state.sendUpdateState(gprocessd(37,channel), "SVD Selesai")
    return l_singular, sigm, r_singular, rank
