import numpy as np
from numpy.linalg import qr
from scipy.linalg import hessenberg


def calculate_eigenvalue(M: np.ndarray):
  """Menghitung nilai eigen. M haruslah matriks persegi."""

  dim = M.shape[1]
  MH = hessenberg(M)

  for _ in range(dim):
    SHIFT = np.identity(dim) * np.diag(MH)[-1]

    q,r = qr(MH - SHIFT)
    MH = (r @ q) + SHIFT

  return np.sort(np.diag(MH))[::-1]
