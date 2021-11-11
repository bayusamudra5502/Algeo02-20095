import lib.svd.svd as svd 
import numpy as np
import pytest

@pytest.mark.asyncio
async def test_svd_1():
  A = np.random.randint(0,255,size=(50,50))
  u,s,vt,_ = await svd.build_decom(A)

  # Tes u dan vt
  uut = u @ np.transpose(u)
  vvt = vt @ np.transpose(vt)
  assert np.allclose(np.identity(len(uut)), uut)
  assert np.allclose(np.identity(len(vvt)), vvt)

  assert np.allclose(u @ s @ vt, A)

@pytest.mark.asyncio
async def test_svd_2():
  A = np.random.randint(0,255,size=(30,50))
  u, s, v = np.linalg.svd(A)
  ua,sa,va,_ = await svd.build_decom(A)
  sz = np.zeros((30,50))

  for i in range(len(s)):
    sz[i][i] = s[i]

  # Tes u dan vt
  uut = u @ np.transpose(u)
  vvt = v @ np.transpose(v)
  assert np.allclose(np.identity(len(uut)), uut)
  assert np.allclose(np.identity(len(vvt)), vvt)

  assert np.allclose(u @ sz @ v, A)
  assert np.allclose(ua @ sa @ va, A)

@pytest.mark.asyncio
async def test_svd_3():
  A = np.random.randint(0,255,size=(50,30))
  u,s,vt,_ = await svd.build_decom(A)

  # Tes u dan vt
  uut = u @ np.transpose(u)
  vvt = vt @ np.transpose(vt)
  assert np.allclose(np.identity(len(uut)), uut)
  assert np.allclose(np.identity(len(vvt)), vvt)

  assert np.allclose(u @ s @ vt, A)
  