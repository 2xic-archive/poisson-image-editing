from nptyping import Array
import numpy as np
from scipy.sparse import spdiags
from scipy.sparse.linalg import spsolve

class poisson:
	"""
	This class describes the abstracts part of the poisson equation
	"""

	def __init__(self):
		self.EXPLICIT = 0
		self.IMPLICIT = 1 

		self.NEUMANN = 0
		self.DIRICHLET = 1

		self.mode_poisson = self.EXPLICIT
		self.mode_boundary = self.NEUMANN

		self.alpha = 0.25

	def set_boundary(self, mode):
		if mode == "Dirichlet":
			self.mode_boundary = self.DIRICHLET
		elif mode == "Neumann":
			self.mode_boundary = self.NEUMANN

	def set_mode(self, mode):
		if mode == "Dirichlet":
			self.mode_poisson = self.EXPLICIT
		elif mode == "Neumann":
			self.mode_poisson = self.IMPLICIT

	def set_alpha(self, value:float):
		"""
		Set the alpha value

		Parameters
		----------
		value : float
			The alhpa value
		"""		
		self.alpha = value

	def get_laplace_explicit(self, data: Array[float, float] = None) -> Array:
		"""
		Gets the laplace

		Parameters
		----------
		data : ndarray
			The data to get the laplace from
		"""
		if data is None:
			data = self.data
		laplace = data[0:-2, 1:-1] \
				  + data[2:, 1:-1] \
				  + data[1:-1, 0:-2] \
				  + data[1:-1, 2:] \
				  - 4 * data[1:-1, 1:-1]
		return laplace * self.alpha


	def get_laplace_implicit(self, data):
		"""
		Gets the laplace

		Parameters
		----------
		data : ndarray
			The data to get the laplace from
		"""
		shape = data.shape[0]

		upperdiag = np.concatenate(([0, 0], -self.alpha * np.ones(shape - 2)))
		upperdiag1 = np.concatenate(([0, 0], -self.alpha * np.ones(shape - 2)))

		centerdiag = np.concatenate(([1], (1 + 4 * self.alpha) * np.ones(shape - 2),
									 [1]))

		lowerdiag = np.concatenate((-self.alpha * np.ones(shape - 2), [0, 0]))
		lowerdiag1 = np.concatenate((-self.alpha * np.ones(shape - 2), [0, 0]))

		diags = np.array([upperdiag, upperdiag1, centerdiag, lowerdiag, lowerdiag1])

		A = spdiags(diags, [2, 1, 0, -1, -2], shape, shape).tocsc()

		return spsolve(A, data[:, :])

	def common_shape(self, data):
		"""
		Make sure the method get the correct shape

		Since explicit and implicit use diffrent array shapes we need to make sure they
		get a common shape returned as the function that they work with is shared

		Parameters
		----------
		data : ndarray
			The data to get a common shape for
		"""		
		if self.mode_poisson == self.EXPLICIT:
			return data[1:-1, 1:-1]
		elif self.mode_poisson == self.IMPLICIT:
			return data
		else:
			raise Exception(" not supported")

	def get_laplace(self, data):
		"""
		Gets the correct laplace based on mode

		Parameters
		----------
		data : ndarray
			The data to get the laplace from
		"""		
		if self.mode_poisson == self.EXPLICIT:
			return self.get_laplace_explicit(data)
		elif self.mode_poisson == self.IMPLICIT:
			return self.get_laplace_implicit(data)
		else:
			raise Exception("not supported")

	def apply_boundary(self, data):
		"""
		Apply the boundary

		Parameters
		----------
		data : ndarray
			The data 
		"""		
		if self.mode_boundary == self.NEUMANN:
			return self.neumann(data)
		elif self.mode_boundary == self.DIRICHLET:
			return self.diriclet(data)
		else:
			raise Exception("not supported")

	def solve(self, data, operator, h=lambda x=None, i=None: 0):
		"""
		Solve the poisson equation

		Parameters
		----------
		data : ndarray
			The data to work with
		operator : callable
			The function applied
		h : callable
			The h function

		"""
		if self.mode_poisson == self.EXPLICIT:
			if(len(data.shape) == 3):
				for i in range(3):#data.shape[-1]):
					data[1:-1, 1:-1, i] += operator(i) - h(i=i)
			else:
				data[1:-1, 1:-1] += operator() - h(data)
		elif self.mode_poisson == self.IMPLICIT:
			if(len(data.shape) == 3):
				for i in range(3):#data.shape[-1]):
					data[:, :, i] = operator(i=i) - h(i=i)
			else:
				data[:, :] = operator() - h(data)
		else:
			raise Exception("Not supported")
		return self.apply_boundary(data)

