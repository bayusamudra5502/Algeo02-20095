from numpy.core.fromnumeric import transpose
from transform import householder_matrix

import numpy as np

def satuan(x):
  return x / np.sqrt(x @ x)

def test_sifat_1():
  A = np.random.randint(0,255,size=(5,5))
  HA = householder_matrix(A)

  assert np.allclose(HA, transpose(HA))
  assert np.allclose(HA, np.linalg.inv(HA))

  vector = np.transpose(A)[0]

  assert np.allclose(np.identity(len(A))[0], satuan(HA @ vector))

def test_sifat_2():
  A = np.random.randint(0,255,size=(30,30))
  HA = householder_matrix(A)

  assert np.allclose(HA, transpose(HA))
  assert np.allclose(HA, np.linalg.inv(HA))

  vector = np.transpose(A)[0]

  assert np.allclose(np.identity(len(A))[0], satuan(HA @ vector))

def test_sifat_3():
  A = np.random.randint(0,255,size=(100,100))
  HA = householder_matrix(A)

  assert np.allclose(HA, transpose(HA))
  assert np.allclose(HA, np.linalg.inv(HA))

  vector = np.transpose(A)[0]

  assert np.allclose(np.identity(len(A))[0], satuan(HA @ vector))
