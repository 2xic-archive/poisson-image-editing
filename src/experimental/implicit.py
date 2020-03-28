from scipy.sparse import spdiags            # støtte for glisne ('sparse') matriser
from scipy.sparse.linalg import spsolve
import numpy as np

from engine import poisson, boundary, image_handler

class blur(image_handler.ImageHandler, poisson.poisson, boundary.Boundary):
	"""
	This class describes a blured image.

	This contains all the functions needed to blur a image over multiple iterations

	Parameters
	----------
	path : str
		path to a image file
	color : bool
		if the image should be shown with colors
	"""
	def __init__(self, path, color=False):
		image_handler.ImageHandler.__init__(self, path, color)
		poisson.poisson.__init__(self)
		boundary.Boundary.__init__(self)
		self.alpha: float = 0.25
		self.lambda_size: float = 0
		#self.data_copy = self.data.copy()

	def set_lambda_size(self, lambda_size) -> None:
		"""
		Sets the lambda fro data attachment

		Parameters
		----------
		lambda_size : float
			The lambda parameter
		"""
		self.lambda_size = lambda_size
		
	def iteration(self):
		"""
		Does one iteration of the method.

		'''
			Notes

			(a - b)/t = 1/x^2 (q + w + e + r - 4 * a) - h
			
			solve for b

			https://www.wolframalpha.com/input/?i=%28a+-+b%29%2Ft+%3D+1%2Fx%5E2+%28q+%2B+w+%2B+e+%2B+r+-+4+*+a%29+-+h%2C+solve+for+b
			
			a = u^{n+1}
			
			b = (a + 4t + x^2) - t(-hx^2 + q + r + w+ e)/x^2

			(notes are on overleaf for now)
		'''

		"""

		laplace = self.get_laplace()
		old = self.data.copy()		

		# Systemmatrisen
		j = self.data.shape[1]
		i = self.data.shape[0]

		# we need 2 diagonals for i and j 
		upperdiag = np.concatenate(([0, 0], -self.alpha * np.ones(j - 2)))
		upperdiag1 = np.concatenate(([0, 0], -self.alpha * np.ones(i - 2)))

		centerdiag = np.concatenate(([1], (1 + 4 * self.alpha) * np.ones(j - 2),
		                             [1]))

		# we need 2 diagonals for i and j
		lowerdiag = np.concatenate((-self.alpha * np.ones(j - 2), [0, 0]))
		lowerdiag1 = np.concatenate((-self.alpha * np.ones(i - 2), [0, 0]))

		diags = np.array([upperdiag, upperdiag1, centerdiag, lowerdiag, lowerdiag1])
		A = spdiags(diags, [2, 1, 0, -1, -2], j, j).tocsc()

		print(A.shape)
		self.data[:, :] = spsolve(A, self.data[:, :])
		self.data = self.data.clip(0, 1)
		self.data = self.neumann(self.data)
		self.data = self.data.clip(0, 1)

		return self.data
		
	def fit(self, epochs):
		"""
		Makes multiple iterations of the method

		Calls iteration as many times as spesifed in by the parameter epochs

		Parameters
		----------
		epochs : int
			The iteration count
		"""
		for i in range(epochs):
			self.iteration()
		return self



