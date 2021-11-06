import numpy as np
from numpy.linalg import qr
from scipy.linalg import hessenberg


def calculate_eigen(M: np.ndarray):
  """Menghitung nilai eigen. M haruslah matriks persegi."""

  dim = M.shape[1]
  MH = hessenberg(M)
  V = np.identity(dim)

  iteration = dim//2

  for _ in range(iteration):
    SHIFT = np.identity(dim) * np.diag(MH)[-1]

    q,r = qr(MH - SHIFT)
    MH = (r @ q) + SHIFT
    V = V @ q

  return np.sort(np.diag(MH))[::-1], V
