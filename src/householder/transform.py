import numpy as np

def householder_matrix(A):
  """Menghitung matriks transformasi Householder."""

  x = np.transpose(A)[0]

  # Vektor umum satuan
  e = np.identity(len(x))[0] * np.sqrt(x @ x)

  b = x - e

  # Vektor pencerminan
  n = b / np.sqrt(b @ np.transpose(b))
  
  nd2 = n[np.newaxis,:]

  return np.identity(len(x)) - 2 * (np.transpose(nd2) @ nd2)

