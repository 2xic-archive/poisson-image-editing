"""
Direkte løsning av Poisson ligningen
	-	finite difference er et nøkkelord her
	-	

https://en.wikipedia.org/wiki/Discrete_Poisson_equation
	-	denne er vel også relevant
"""
# should use scipy in future 
import numpy as np
from engine import image_handler
from copy import deepcopy


import numpy as np


# from https://gist.github.com/cbellei/8ab3ab8551b8dfc8b081c518ccd9ada9
## Tri Diagonal Matrix Algorithm(a.k.a Thomas algorithm) solver
def TDMAsolver(a, b, c, d):
	'''
	TDMA solver, a b c d can be NumPy array type or Python list type.
	refer to http://en.wikipedia.org/wiki/Tridiagonal_matrix_algorithm
	and to http://www.cfd-online.com/Wiki/Tridiagonal_matrix_algorithm_-_TDMA_(Thomas_algorithm)
	'''
	nf = len(d) # number of equations
	ac, bc, cc, dc = map(np.array, (a, b, c, d)) # copy arrays
	for it in range(1, nf):
		mc = ac[it-1]/bc[it-1]
		bc[it] = bc[it] - mc*cc[it-1] 
		dc[it] = dc[it] - mc*dc[it-1]
				
	xc = bc
	xc[-1] = dc[-1]/bc[-1]

	for il in range(nf-2, -1, -1):
		xc[il] = (dc[il]-cc[il]*xc[il+1])/bc[il]

	return xc

def create_d_base_matrix(size):
	D = np.diag(-np.ones(size), 1)
	D += np.diag(-np.ones(size), -1)
	np.fill_diagonal(D, 4)
	return D

def make_A(D, I):
	A = np.zeros((D.shape[0] ** 2,D.shape[0] ** 2))
	for i in range(D.shape[0]):
		A[D.shape[0] * i : D.shape[0] * (i+1), D.shape[0] * i : D.shape[0] * (i+1)] += D
#	for i in range(D.shape[0] - 1):
#	    A[3*(i+1):3*(i+D.shape[0] - 1), 3*i:3*(i+1)] += -I
#	    A[3*i:3*(i+1), 3*(i+1):3*(i+D.shape[0] - 1)] += -I
	return A

def process(U):
	u = U[1:-1,1:-1].T

	u_size = int(deepcopy(u.shape[0] - 1))
	u = u.flatten()

	D = (create_d_base_matrix(u_size))
	I = np.identity(u_size + 1)
	A = make_A(D, I)

	h = 0
	alpha = -(0.25 ** 2)
	alpha *= h

	b = np.zeros((u.shape))
	b += alpha
	b += u
	print(b.shape)
	return (np.linalg.solve(A, b))

from PIL import Image

if __name__ == "__main__":
	# test "image"

	# based of the wikipedia example
	U = np.arange(25).reshape((5,5))
	process(U)

	# test on image
	image = image_handler.ImageHandler("./files/test_images/lena.png", False)
	image.resize(3)

	data_image = process(image.data)
	new_size = image.data[1:-1,1:-1].shape

	image_data = Image.fromarray(np.uint8(255 * (np.fliplr(np.rot90(data_image.reshape(new_size), 3)))))
	image_data.show()
#	print(image.data.shape)




