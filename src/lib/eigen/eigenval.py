import numpy as np
from upperhess import make_upper_hessenberg

def calculate_eigenvalue(M: np.ndarray):
  """Menghitung nilai eigen. M haruslah matriks persegi."""

  MH = make_upper_hessenberg(M)

  