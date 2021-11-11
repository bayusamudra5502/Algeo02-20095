import numpy as np
from api.state import State
from scipy.linalg.decomp import hessenberg

async def EigenV(mat:np.ndarray, precision = 30, *, sendProgress=False,state:State=None, startCounter=0, endCounter=1, channel="WARNA"):
    _, n = mat.shape
    totalProses = 1 + n

    if sendProgress:
        await state.sendUpdateState(startCounter, f"[{channel}] Memulai perhitungan matriks hessenberg")

    H, Q = hessenberg(mat, calc_q=True)

    if sendProgress:
        await state.sendUpdateState(startCounter + (1/totalProses*(endCounter-startCounter)), f"[{channel}] Mempersiapkan pehitungan Eigenvalue")

    sub = np.float64(np.copy(np.diag(H,-1)))
    diag = np.float64(np.copy(np.diag(H)))
    sub = np.insert(sub, n-1, 0)
    limit = precision

    for i in range(n):
        if sendProgress and i % 50 == 0:
            await state.sendUpdateState(startCounter + (1+i/totalProses*(endCounter-startCounter)), f"[{channel}] Menghitung Eigenvalue ({i}/{n})")

        niter = 0
        while niter<limit:
            j = i
            while j+1!=n and  np.abs(sub[j]) > 1e-20*(np.abs(diag[j])+np.abs(diag[j+1])):
                j += 1
            if(j==i):
                break
            else:
                niter += 1
                g = (diag[i + 1]-diag[i])/(2*sub[i])
                r = np.hypot(g, 1)
                if(np.abs(g)<1e-9):
                    g = diag[j]-diag[i]+(sub[i]/(g+r))
                else:
                    g = diag[j]-diag[i]+(sub[i]/(g + np.sign(g)*r))

                # rotasi givens
                s = 1
                c = 1
                p = 0
                for k in range(j-1, i-1, -1):
                    f = s*sub[k]
                    b = c*sub[k]
                    if(np.abs(f) > np.abs(g)):
                        c = g/f
                        tau = np.hypot(c, 1)
                        sub[k+1] = f*tau
                        s = 1/tau
                        c *= s
                    else:
                        s = f/g
                        tau = np.hypot(s, 1)
                        sub[k+1] = g*tau
                        c = 1/tau
                        s *= c
                    g = diag[k+1]-p
                    r = 2*b*c+(diag[k]-g)*s
                    p = r*s
                    diag[k+1] = g+p
                    g = r*c-b
                    # eigenvector
                    Q[:,k:k+2] = (Q[:,k:k+2]).dot(np.array([[c,s],[-s,c]]))
                sub[i] = g
                sub[j] = 0
                diag[i] = diag[i]-p
    return diag, Q
