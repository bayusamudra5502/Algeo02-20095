from lib.householder.transform import hmatrix_calc 
import numpy as np

def make_upper_hessenberg(A):
  """Membuat matriks persegi A menjadi matriks upper hessenberg"""
  result = np.copy(A)

  for i in range(len(A)-2):
    u = -result[i+1:,i]
    u[0] += np.sign(u[0]) * np.sqrt(u @ u)

    v = u/np.sqrt(u@u)

    M = hmatrix_calc(len(A)-i-1, v)

    result[i+1:,i+1:] = M @ result[i+1:,i+1:] @ M
    result[:i+1,i+1:] = result[:i+1,i+1:] @ M
    result[i+1:,:i+1] = M @ result[i+1:,:i+1]
   
  return result