from PIL import Image
from matplotlib import pyplot as PLT
import numpy as np
import math
# belum diimport, gatau gimanain:(

def image_to_rgba(filePath):
    with Image.open(filePath) as im:
        return np.array(im.convert("RGBA"))

def inspectColor(Im):
    return np.int32(np.array(Im[:,:,0])), np.int32(np.array(Im[:,:,1])), np.int32(np.array(Im[:,:,2])), np.int32(np.array(Im[:,:,3])) 


def colorToImage(M):
    PLT.imshow(M)
    PLT.show()

def compress_to_k(A, k):
    u, sigm, v, rank = build_decom(A)
    k = math.floor(rank*k/100)
    return (u[:,:k]@(sigm[:k, :k]@v[:k, :]))

def compress_all(R, G, B, A, k):
    R = compress_to_k(R, k)
    G = compress_to_k(G, k)
    B = compress_to_k(B, k)
    A = compress_to_k(A, k)
    return R, G, B, A

def compress_image(filePath, k):
    M = image_to_rgba(filePath)
    R, G, B, A = inspectColor(M)
    R, G, B, A = compress_all(R, G, B, A, k)
    M = np.uint8((np.dstack((R, G, B, A))))
    colorToImage(M)