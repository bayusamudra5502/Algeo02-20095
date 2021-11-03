from qr_factorization import qr_factorization
import numpy as np

def test_qr_1():
  A = np.random.randint(0,255,size=(50,50))

  q,r = qr_factorization(A)

  assert np.allclose(A, q @ r)

def test_qr_2():
  A = np.random.randint(0,255,size=(30,50))

  q,r = qr_factorization(A)

  assert np.allclose(A, q @ r)