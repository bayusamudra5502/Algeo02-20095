import numpy as np

def getNorm(x):
# Menghitung panjang vektor
    return np.sqrt(np.sum(np.square(x)))

def getColumn(m,i):
# Mengambil data colom ke-i
    return np.copy(m[:,i])

def getSubMatrix(m):
# Mengembalikan submatriks dari x
    return m[1:,1:]

def createMatrixIdentity(n):
# Mengembalikan matrix satuan berukuran n x n
    return np.identity(n)

def createVektor_e(n,col):
# Mengembalikan vektor e dengan jumlah elemen n dan elemen pertamanya bernilai 1
    x = np.identity(n)
    e = getColumn(x,col)
    return e

def calVektor_v(a,i):
# Mengembailkan vektor v
    return (a - getNorm(a) * createVektor_e(len(a),i))

def calMatrix_H(v):
# Mengembalikan matrix Housholder untuk vektor v
    I = createMatrixIdentity(len(v))
    t = (v.T @ v)/2
    u = v.reshape(len(v),1)
    H = I - (u @ u.T) / t
    return H

def qr_factorization(m):
    A = np.copy(m)
    H = createMatrixIdentity(len(m))
    for i in range((len(m) - 1)):
        a = getColumn(A,i)
        for j in range(i):
            a[j] = 0
        H_i = calMatrix_H((calVektor_v(a,i))) 
        H =  H_i @ H
        A = H_i @ A
    return H.T, A



# contoh aplikasinya
# m = np.array([[2.5,1.1,0.3],[2.2,1.9,0.4],[1.8,0.1,0.3]])
# Q, R = householder_transformation(m) 
# print(Q)
# print(R)

# print(Q @ R)
