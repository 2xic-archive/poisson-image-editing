from PIL import Image
import numpy as np
from scipy import sparse
import numpy as np
from engine import image_handler
from copy import deepcopy
from engine import poisson
import numpy as np
import scipy

"""
http://www.cryptosystem.org/archives/2009/09/using-matlab-for-numerical-solutions-to-the-discrete-poisson-equation/
	- "Let's say you've got a 2D image (or matrix) of the Laplacian of some function, and you want to solve for the function. "	
		-	Okay so I guess the idea is that the input should actually be the laplace schema output
https://en.wikipedia.org/wiki/Discrete_Poisson_equation

https://www.math.uci.edu/~chenlong/226/FDMcode.pdf
"""

def lap_matrix(X):
	nx, ny = X[1:-1,1:-1].shape[:2]
	N  = nx*ny
	main_diag = np.ones(N)*-4.0
	side_diag = np.ones(N-1)
	side_diag[np.arange(1,N)%4==0] = 0
	up_down_diag = np.ones(N-3)
	diagonals = [main_diag,side_diag,side_diag,up_down_diag,up_down_diag]
	laplacian = sparse.diags(diagonals, [0, -1, 1,nx,-nx], format="csr")

	m = X.shape[0]
	n = X.shape[1]
	b = -X[1:(m-1),1:(n-1)].reshape((m-2) * (n-2),1);
	print(laplacian.shape)
	print(b.shape)
	u =	 (scipy.linalg.solve_triangular(laplacian.toarray(), b, check_finite=False))
	u = u.reshape((m - 2, n - 2))
	return u


if __name__ == "__main__":
	image = image_handler.ImageHandler("./files/test_images/lena.png", False)
	Image.fromarray(np.uint8( 255 * (image.data))).show()

	X = np.zeros((image.data.shape))
	X[1:-1,1:-1] =  poisson.poisson().get_laplace_explicit(image.data, alpha=False)	
	Image.fromarray(np.uint8( 255 * (X))).show()

	response = lap_matrix(X)
	Image.fromarray(np.uint8( 255 * (response))).show()

#		image.data[1:-1,1:-1] += 0.8 * response
#	Image.fromarray(np.uint8( 255 * (image.data))).show()