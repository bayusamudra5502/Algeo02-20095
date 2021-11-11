import numpy as np
import sklearn.preprocessing
from api.state import State

from lib.eigen.eigen import EigenV

def counter_calc(number, start, end, cnt):
    return start+ number/cnt * (end-start)

async def build_decom(A: np.ndarray,*, sendProgress=False, state:State=None, startCounter=0, endCounter=37, channel="WARNA"):
    if sendProgress:
        await state.sendUpdateState(counter_calc(1, startCounter, endCounter,38),
            F"[{channel}] Memulai Perhitungan Perkalian Matriks A @ A.T")

    l = A@(A.T)

    if sendProgress:
        await state.sendUpdateState(counter_calc(2, startCounter, endCounter,38),
        f"[{channel}] Memulai Perhitungan Perkalian Matriks A.T @ A")

    r = (A.T)@A
    
    #generate eigenvector with their corresponding eigenval
    if sendProgress:
        await state.sendUpdateState(counter_calc(3, startCounter, endCounter,38),
            f"[{channel}] Memulai Perhitungan Eigenvector L")

    l_eigval, l_eig = await EigenV(l,sendProgress=sendProgress,state=state, 
                startCounter=counter_calc(3, startCounter, endCounter,38), 
                endCounter=counter_calc(13, startCounter, endCounter,38), 
                channel=channel)

    if sendProgress:
        await state.sendUpdateState(counter_calc(14, startCounter, endCounter,38),
            f"[{channel}] Memulai Perhitungan Eigenvector R")

    r_eigval, r_eig = await EigenV(r,sendProgress=sendProgress,
        state=state, startCounter=counter_calc(14, startCounter, endCounter,38), 
        endCounter=counter_calc(24, startCounter, endCounter,37),
         channel=channel)

    if sendProgress:
        await state.sendUpdateState(counter_calc(25, startCounter, endCounter,38),
            f"[{channel}] Memulai Perhitungan SVD")

    #shaping matrix
    rows, cols = A.shape
    r_sigmum = np.sqrt(np.abs(r_eigval))
    l_sigmum = np.sqrt(np.abs(l_eigval))
    r_sort_pivot = np.argsort(-1*r_sigmum)
    l_sort_pivot = np.argsort(-1*l_sigmum)
    sigm = np.pad(np.diag(r_sigmum[r_sort_pivot]), 
        ((0,rows),(0,cols)), mode='constant')[0:rows, 0:cols]

    # sorting right singular         
    r_singular = r_eig.T[r_sort_pivot]
    # sorting & correlate right singular with left singular & dinomalisasi
    l_singular = l_eig[:,l_sort_pivot]

    cnt = 0
    i = 0
    rank = 0

    for x in r_sigmum:
        cnt += 1
        if sendProgress and cnt % 25 == 0:
            await state.sendUpdateState(
                counter_calc(26 + 10*(cnt/len(r_sigmum)), startCounter, endCounter,38),
                f"[{channel}] Mencari nilai Singular L")

        if(abs(x)>np.finfo(float).eps):
            rank+=1
        if(abs(x)>np.finfo(float).eps and i<min(l_singular.shape[0],r_singular.shape[0])):
            l_singular[:,i] = (A@r_singular[i,:])*(1/x)
            i+=1
    
    if sendProgress:
        await state.sendUpdateState(counter_calc(37, startCounter, endCounter,38),
        f"[{channel}] Menormalisasi Singular L")
    
    l_singular = l_singular.T
    sklearn.preprocessing.normalize(l_singular, norm="l2", axis=1, copy=False)
    l_singular = l_singular.T

    if sendProgress:
        await state.sendUpdateState(counter_calc(38, startCounter, endCounter,38),
        f"[{channel}] Proses dekomposisi selesai")

    return l_singular, sigm, r_singular, rank
