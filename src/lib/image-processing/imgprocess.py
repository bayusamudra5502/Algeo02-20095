import numpy as np
import math
from lib.svd.svd import build_decom
from api.state import State

def inspectColor(Im):
    return np.int32(np.array(Im[:,:,0])), np.int32(np.array(Im[:,:,1])), np.int32(np.array(Im[:,:,2])), np.int32(np.array(Im[:,:,3])) 

async def compress_to_k(A, k):
    u, sigm, v, rank = await build_decom(A)
    k = math.floor(rank*k/100)
    return (u[:,:k]@(sigm[:k, :k]@v[:k, :])), k

async def compress_to_k_by_cache(state: State, k, color):
    u, sigm, v, rank = state.getState("SVDDecomp")[color]
    k = math.floor(rank*k/100)
    return (u[:,:k]@(sigm[:k, :k]@v[:k, :])), k

def compress_all(R, G, B, A, k):
    R = compress_to_k(R, k)
    G = compress_to_k(G, k)
    B = compress_to_k(B, k)
    A = compress_to_k(A, k)
    return R, G, B, A

async def compress_image(M, k):
    R, G, B, A = inspectColor(M)
    R, G, B, A = compress_all(R, G, B, A, k)
    M = np.uint8((np.dstack((R, G, B, A))))

async def compress_all_by_cache(state: State, k,alpha: bool= False, *, startCounter=0, endCounter=1):
    await state.sendUpdateState(state.counter_calc(0, startCounter, endCounter, 4),
        "Menghitung hasil kompresi warna merah")

    R = await compress_to_k_by_cache(state, k, "R")

    await state.sendUpdateState(state.counter_calc(1, startCounter, endCounter, 4),
        "Menghitung hasil kompresi warna hijau")

    G = await compress_to_k_by_cache(state, k, "G")

    await state.sendUpdateState(state.counter_calc(2, startCounter, endCounter, 4),
        "Menghitung hasil kompresi warna biru")

    B = await compress_to_k_by_cache(state, k, "B")

    await state.sendUpdateState(state.counter_calc(3, startCounter, endCounter, 4),
        "Menghitung hasil kompresi Alpha Channel")

    A = None

    if alpha:
        A = await compress_to_k_by_cache(state, k, "A")
    else:
        A = await compress_to_k_by_cache(state, 100, "A")
    
    await state.sendUpdateState(state.counter_calc(4, startCounter, endCounter, 4),
        "Proses kompresi berhasil")

    return R,G,B,A

async def compress_all_by_cache(s:State, k, *, startCounter=0, endCounter=1):
    R,G,B,A = await compress_all_by_cache(s,k,startCounter=startCounter, endCounter=endCounter)
    return np.uint8((np.dstack((R, G, B, A))))

async def build_decom_state(state:State, *, startCounter=0, endCounter=1):
    state.setState("imageReady", False)
    await state.sendUpdateState(state.counter_calc(0, startCounter, endCounter, 42),
        "Memecah warna matriks")
    R, G, B, A = inspectColor(state.getState("imageMatrix"))

    cache = {}

    await state.sendUpdateState(state.counter_calc(1, startCounter, endCounter, 42),
        "Memulai melakukan dekomposisi SVD untuk warna merah")

    u, sigm, v, rank = await build_decom(R, sendProgress=True, state=state, 
        startCounter=state.counter_calc(1, startCounter, endCounter, 42), 
        endCounter=state.counter_calc(11, startCounter, endCounter, 42))

    cache["R"] = (u, sigm, v, rank)

    await state.sendUpdateState(state.counter_calc(11, startCounter, endCounter, 42),
        "Memulai melakukan dekomposisi SVD untuk warna hijau")

    u, sigm, v, rank = await build_decom(G, sendProgress=True, state=state, 
        startCounter=state.counter_calc(11, startCounter, endCounter, 42), 
        endCounter=state.counter_calc(21, startCounter, endCounter, 42))

    cache["G"] = (u, sigm, v, rank)

    await state.sendUpdateState(state.counter_calc(21, startCounter, endCounter, 42),
        "Memulai melakukan dekomposisi SVD untuk warna biru")

    u, sigm, v, rank = await build_decom(B, sendProgress=True, state=state, 
        startCounter=state.counter_calc(21, startCounter, endCounter, 42), 
        endCounter=state.counter_calc(31, startCounter, endCounter, 42))

    cache["B"] = (u, sigm, v, rank)

    await state.sendUpdateState(state.counter_calc(31, startCounter, endCounter, 42),
        "Memulai melakukan dekomposisi SVD untuk Alpha Channel")

    u, sigm, v, rank = await build_decom(A, sendProgress=True, state=state, 
        startCounter=state.counter_calc(31, startCounter, endCounter, 42), 
        endCounter=state.counter_calc(41, startCounter, endCounter, 42))

    cache["A"] = (u, sigm, v, rank)

    state.setState("SVDDecomp", cache)
    state.setState("imageReady", True)
    
    await state.sendUpdateState(state.counter_calc(42, startCounter, endCounter, 42), 
        "Hasil dekomposisi RGBA tersimpan")
