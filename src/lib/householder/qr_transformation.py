import numpy as np

def householder_matrix(A):
  """Menghitung matriks transformasi Householder."""

  x = A[:,0]

  e = np.identity(len(x))[0] * np.sqrt(x @ x)
  b = x - e
  n = b / np.sqrt(b @ np.transpose(b))

  return hmatrix_calc(len(x), n)

def hmatrix_calc(l,v):
  """Menghitung matrix transformasi householder matriks A ke matriks yang searah dengan E"""
  
  nd2 = v[np.newaxis,:]
  return np.identity(l) - 2 * (np.transpose(nd2) @ nd2)/ (nd2 @ np.transpose(nd2))

x = np.array([[1,-1,4],[1,4,-2],[1,4,2],[1,-1,0]])
print(householder_matrix(x) @ x)