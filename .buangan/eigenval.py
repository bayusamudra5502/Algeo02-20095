import numpy as np
from numpy.linalg import qr
from scipy.linalg import hessenberg
import time

def calculate_eigen(M):
  """Menghitung nilai eigen. M haruslah matriks persegi."""

  dim = M.shape[1]
  MH = hessenberg(M)
  V = np.identity(dim)

  iteration = 1000

  for _ in range(iteration):
    SHIFT = np.identity(dim) * np.diag(MH)[-1]

    q,r = qr(MH - SHIFT)
    MH = (r @ q) + SHIFT
    V =  V@q

  return np.diag(MH), V


A = np.random.randint(100,255,size=(4, 4))
A = (np.float64(A)@((np.float64(A)).T))
p = A
start = time.time()
xx, yy = calculate_eigen(A)
end = time.time()
print(end-start)
start = time.time()
o, q = np.linalg.eigh(p)
end = time.time()
print(xx)
print(o)
for i in range(4): print(np.divide(p@q[:,i], q[:,i]))
for i in range(4): print(np.divide(p@yy[i,:], yy[i,:]))
# print(np.diag(xx)@yy-p@yy)
print(end-start)