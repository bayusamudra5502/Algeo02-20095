import numpy as np
def simultaneous_power_iteration(A, k):
    n, m = A.shape
    Q = np.random.rand(n, k)
    Q, _ = np.linalg.qr(Q)
    Q_prev = Q
 
    for i in range(1000):
        Z = A.dot(Q)
        Q, R = np.linalg.qr(Z)

        # can use other stopping criteria as well 
        err = ((Q - Q_prev) ** 2).sum()
        # if i % 10 == 0:
            # print(i, err)

        Q_prev = Q
        if err < 1e-3:
            break

    return np.diag(R), Q

A = np.random.randint(0,255,size=(1000,1000))
A = A.dot(A.T)
p, q = np.linalg.eig(A)
r, s = simultaneous_power_iteration(A, 1000)
print(p)
print(q)
print(r)
print(s)
