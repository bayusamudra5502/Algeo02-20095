contoh aplikasinya
m = np.array([[2.5,1.1,0.3],[2.2,1.9,0.4],[1.8,0.1,0.3]])
Q, R = householder_transformation(m) 
print(Q)
print(R)

print(Q @ R)