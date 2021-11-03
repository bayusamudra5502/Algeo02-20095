import numpy as np
from upperhess import make_upper_hessenberg
from lib.qr.qr_factorization import qr_factorization

def calculate_eigenvalue(M: np.ndarray):
  """Menghitung nilai eigen. M haruslah matriks persegi."""
  # Error masih gede dan lemot

  dim = len(M)
  MH = make_upper_hessenberg(np.copy(M))
  MH = MH.astype(np.float128)

  for _ in range(np.min([dim, 50])):
    I = np.identity(dim) * np.diag(MH)[-1]
    q,r = qr_factorization(MH - I)

    MH = r @ q + I
  
  return np.sort(np.diag(MH))[::-1]
