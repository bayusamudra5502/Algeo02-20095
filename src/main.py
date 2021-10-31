import numpy as np

arr1 = np.array([[1,5,3],[4,3,6],[7,8,9]])
arr2 = np.array([[1,0,0],[0,1,0],[0,0,1]])

arr3 = np.linalg.inv(arr1)

print(arr3)

print("Halo, Dunia")