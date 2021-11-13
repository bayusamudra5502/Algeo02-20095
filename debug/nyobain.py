import numpy as np
import sklearn.preprocessing
from scipy.linalg.decomp import hessenberg
import math
from PIL import Image
import numpy as np
import io
import time
import cv2

def convertFileToArray(file):
  with Image.open(file) as im:
    return np.array(im.convert("RGBA"))

def convertArrayToIO(array: np.ndarray, mime:str="image/png"):
  im = Image.fromarray(array)
  f = io.BytesIO()

  if mime == "image/png":
    im.save(f, format="PNG")
  else:
    im = im.convert("RGB")
    im.save(f, "JPEG")

  f.seek(0)
  return f

def inspectColor(Im):
    return np.copy(np.int32(np.array(Im[:,:,0]))), \
            np.copy(np.int32(np.array(Im[:,:,1]))), \
            np.copy(np.int32(np.array(Im[:,:,2]))), \
            np.copy(np.int32(np.array(Im[:,:,3]))) 

def inspectcolor2(Im):
    return np.copy(np.array(Im[:,:,0])), np.copy(np.array(Im[:,:,1])), np.copy(np.array(Im[:,:,2])), np.copy(np.array(Im[:,:,3]))

def compress_to_k(A, k):
    # u, sigm, v, rank = build_decom(A)
    u, sigm, v = np.linalg.svd(A)
    rows, cols = A.shape
    sigm = np.pad(np.diag(sigm), ((0,rows),(0,cols)), mode='constant')[0:rows, 0:cols]
    m = np.linalg.matrix_rank(A)
    k = math.floor((k*m)/100)
    return (u[:,:k]@(sigm[:k, :k]@v[:k, :]))

def compress_all(R, G, B, A, k):
    start = time.time()
    R = compress_to_k(R, k)
    end = time.time()
    print(end-start)
    start = time.time()
    G = compress_to_k(G, k)
    end = time.time()
    print(end-start)
    start = time.time()
    B = compress_to_k(B, k)
    end = time.time()
    print(end-start)
    start = time.time()
    A = compress_to_k(A, k)
    end = time.time()
    print(end-start)
    return R, G, B, A

def compress_image(M, k):
    R, G, B, A = inspectColor(M)
    R, G, B, A = compress_all(R, G, B, A, k)
    M = np.uint8((np.dstack((R, G, B, A))))
    return M

def EigenV(mat, precision = 30):
    _, n = mat.shape
    # MAX_SECTION = n + 3

    # if updater != None:
    #     updater(1/MAX_SECTION)

    H, Q = hessenberg(mat, calc_q=True)
    sub = np.float64(np.copy(np.diag(H,-1)))
    diag = np.float64(np.copy(np.diag(H)))
    sub = np.insert(sub, n-1, 0)
    limit = precision

    # if updater != None:
    #     updater(2/MAX_SECTION)

    for i in range(n):
        # if updater != None and i % 10 == 0:
        #     updater((2+i)/MAX_SECTION)

        niter = 0
        while niter<limit:
            j = i
            while j+1!=n and  np.abs(sub[j]) > 1e-20*(np.abs(diag[j])+np.abs(diag[j+1])):
                j += 1
            if(j==i):
                break
            else:
                niter += 1
                g = (diag[i + 1]-diag[i])/(2*sub[i])
                r = np.hypot(g, 1)
                if(np.abs(g)<1e-9):
                    g = diag[j]-diag[i]+(sub[i]/(g+r))
                else:
                    g = diag[j]-diag[i]+(sub[i]/(g + np.sign(g)*r))

                # rotasi givens
                s = 1
                c = 1
                p = 0
                for k in range(j-1, i-1, -1):
                    f = s*sub[k]
                    b = c*sub[k]
                    if(np.abs(f) > np.abs(g)):
                        c = g/f
                        tau = np.hypot(c, 1)
                        sub[k+1] = f*tau
                        s = 1/tau
                        c *= s
                    else:
                        s = f/g
                        tau = np.hypot(s, 1)
                        sub[k+1] = g*tau
                        c = 1/tau
                        s *= c
                    g = diag[k+1]-p
                    r = 2*b*c+(diag[k]-g)*s
                    p = r*s
                    diag[k+1] = g+p
                    g = r*c-b
                    # eigenvector
                    Q[:,k:k+2] = (Q[:,k:k+2]).dot(np.array([[c,s],[-s,c]]))
                sub[i] = g
                sub[j] = 0
                diag[i] = diag[i]-p
    return diag, Q

def build_decom(A: np.ndarray):
    l = A@(A.T)
    r = (A.T)@A
    # if sendFeedback:
    #     state.sendUpdateState(gprocessd(1,channel), "Proses Perkalian Matriks Selesai")
    
    # #generate eigenvector with their corresponding eigenval
    # if sendFeedback:
    #     state.sendUpdateState(gprocessd(2,channel), "Menghitung Nilai Eigen")

    l_eigval, l_eig = EigenV(l)

    # if sendFeedback:
    #     state.sendUpdateState(gprocessd(13,channel), "Menghitung Nilai Eigen")
    
    r_eigval, r_eig = EigenV(r)

    # #shaping matrix
    # if sendFeedback:
    #     state.sendUpdateState(gprocessd(24,channel), "Membentuk Matriks SVD")

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
        # if sendFeedback and cnt % 50 == 0:
        #     state.sendUpdateState(gprocessd(25 + cnt/len(r_sigmum) * 10,channel), "Membentuk Matriks SVD")

        cnt += 1

        if(abs(x)>np.finfo(float).eps):
            rank+=1
        if(abs(x)>np.finfo(float).eps and i<min(l_singular.shape[0],r_singular.shape[0])):
            l_singular[:,i] = (A@r_singular[i,:])*(1/x)
            i+=1

    
    # if sendFeedback:
    #     state.sendUpdateState(gprocessd(36,channel), "Normalisasi Matriks")

    l_singular = l_singular.T
    sklearn.preprocessing.normalize(l_singular, norm="l2", axis=1, copy=False)
    l_singular = l_singular.T

    # if sendFeedback:
    #     state.sendUpdateState(gprocessd(37,channel), "SVD Selesai")

    return l_singular, sigm, r_singular, rank

# M = compress_image(M, 50)
# convertArrayToIO(M)
im = Image.open("data/D.png")
p = im.mode
# print(im.mode)
# M = np.array(im.getpalette())
# N = np.array(im.getchannel(1))
# print(M.shape)
# print(M)
# print(N)
# im = Image.Image.getdata(im)
# M = np.array(im.getpalette(),dtype=np.int32).reshape((256,3))
# u, v, w, t = build_decom(M)
# k = np.linalg.matrix_rank(M)
# # k = math.floor(50*k/100)
# M = np.uint8((u[:,:k]@(v[:k, :k]@w[:k, :])))
# print(M)
# print(M)
M = np.array(im.convert("RGBA"))
# R, G, B, A = inspectColor(M)
# R, G, B, A = compress_all(R, G, B, A, 50)
# M = np.uint8((np.dstack((R, G, B, A))))
# # x, y, z = M.shape
# # # M = M.reshape(x, y, 4)
im = Image.fromarray(M)
# # im.putpalette(M)
# im = im.convert("RGBA")
im = im.convert(p)
im.save("data/image.png")

# f.seek(0)
# print(im)
