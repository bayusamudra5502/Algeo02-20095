import numpy as np
import math
from lib.svd.svd import build_decom
from api.state import State
from threading import Thread

def inspectColor(Im):
    return np.copy(np.int32(np.array(Im[:,:,0]))), \
            np.copy(np.int32(np.array(Im[:,:,1]))), \
            np.copy(np.int32(np.array(Im[:,:,2]))), \
            np.copy(np.int32(np.array(Im[:,:,3]))) 

async def compress_to_k(A, k):
    u, sigm, v, rank = await build_decom(A)
    k = math.floor(rank*k/100)
    return (u[:,:k]@(sigm[:k, :k]@v[:k, :])), k

async def compress_to_k_by_cache(state: State, k, color):
    u, sigm, v, rank = state.getState("SVDDecomp")[color]
    k = math.floor(rank*k/100)
    compress = k/rank

    return (u[:,:k]@(sigm[:k, :k]@v[:k, :])), k, compress

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
    state.sendUpdateState({"value": state.counter_calc(0, startCounter, endCounter, 4), "func": 2},
        "Menghitung hasil kompresi warna merah")

    R = await compress_to_k_by_cache(state, k, "R")

    state.sendUpdateState({"value": state.counter_calc(1, startCounter, endCounter, 4), "func": 2},
        "Menghitung hasil kompresi warna hijau")

    G = await compress_to_k_by_cache(state, k, "G")

    state.sendUpdateState({"value": state.counter_calc(2, startCounter, endCounter, 4), "func": 2},
        "Menghitung hasil kompresi warna biru")

    B = await compress_to_k_by_cache(state, k, "B")

    state.sendUpdateState({"value": state.counter_calc(3, startCounter, endCounter, 4), "func": 2},
        "Menghitung hasil kompresi Alpha Channel")

    A = None

    if alpha:
        A = await compress_to_k_by_cache(state, k, "A")
    else:
        A = await compress_to_k_by_cache(state, 100, "A")
    
    state.sendUpdateState({"value": state.counter_calc(4, startCounter, endCounter, 4), "func": 2},
        "Proses kompresi berhasil")

    return R,G,B,A

async def compress_image_by_cache(s:State, k, *, startCounter=0, endCounter=1, alpha=False):
    R,G,B,A = await compress_all_by_cache(s,k,startCounter=startCounter, endCounter=endCounter, alpha=alpha)
    mat = np.uint8((np.dstack((R[0], G[0], B[0], A[0]))))

    compressLevel = (R[2] + G[2] + B[2] + A[2])/4

    return mat, compressLevel

def calculate_decom(M, cache, channel, state):
    u, sigm, v, rank = build_decom(M, state=state, channel=channel, sendFeedback=True)
    cache[channel] = (u, sigm, v, rank)


def build_decom_state(state:State):
    state.sendUpdateState({"func":0 , "progress": 1/20}, "Mempersiapkan prosess")
    state.setState("imageReady", False)

    R, G, B, A = inspectColor(state.getState("imageMatrix"))

    cache = {}

    Rth = Thread(target=calculate_decom, args=(R,cache,"R", state), daemon=True)
    Gth = Thread(target=calculate_decom, args=(G,cache,"G", state), daemon=True)
    Bth = Thread(target=calculate_decom, args=(B,cache,"B", state), daemon=True)
    Ath = Thread(target=calculate_decom, args=(A,cache,"A", state), daemon=True)

    state.sendUpdateState({"func":0, "progress": 2/20}, "Menjalankan Thread")
    Rth.start()
    Gth.start()
    Bth.start()
    Ath.start()

    Rth.join()
    Gth.join()
    Bth.join()
    Ath.join()
    state.sendUpdateState({"func":0, "progress": 20/20}, "Proses dekomposisi selesai")

    state.setState("SVDDecomp", cache)
    state.setState("imageReady", True)
    