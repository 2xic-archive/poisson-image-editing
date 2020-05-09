from nptyping import Array
import numpy as np
from scipy.sparse import spdiags
from scipy.sparse.linalg import spsolve

class poisson(object):
	"""
	This class describes the abstracts part of the poisson equation
	"""

	def __init__(self):#, mode_boundary=1, mode_poisson=0):
		self.EXPLICIT = 0
		self.IMPLICIT = 1 

		self.NEUMANN = 0
		self.DIRICHLET = 1

		self._mode_poisson = self.EXPLICIT
		self._mode_boundary =  self.DIRICHLET
		self.alpha = 0.25

	@property
	def boundary(self):
		return self._mode_boundary

	@property
	def mode_boundary(self):
		return self._mode_boundary

	@mode_boundary.setter
	def mode_boundary(self, mode):
		'setting'
		self.set_boundary(mode)

	@property
	def mode_poisson(self):
		'getting'
		#print('Getting value {}'.format(self._mode_poisson)) 
		return self._mode_poisson

	@mode_poisson.setter
	def mode_poisson(self, mode):
		'setting'
		#print('Setting value to ' +str(mode) ) 
		#print("in", mode)
#		self.set_mode(mode)
		if mode == "Explicit" or mode == self.EXPLICIT:
			self._mode_poisson = self.EXPLICIT
		elif mode == "Implicit" or mode == self.IMPLICIT:
			self._mode_poisson = self.IMPLICIT
		else:
			raise Exception("Illegal mode ({})".format(mode))

	def set_boundary(self, mode):
		if (type(mode) == str and mode.lower() == "Dirichlet".lower()) or mode == self.DIRICHLET:
			self._mode_boundary = self.DIRICHLET
		elif (type(mode) == str and mode.lower() == "Neumann".lower()) or mode == self.NEUMANN:
			self._mode_boundary = self.NEUMANN
		else:
			raise Exception("Illegal boundary ({})".format(mode))

	def set_mode(self, mode):
		print("In 2 ", mode)
		if mode == "Explicit" or mode == self.EXPLICIT:
			self._mode_poisson = self.EXPLICIT
			print("me")
		elif mode == "Implicit" or mode == self.IMPLICIT:
			self._mode_poisson = self.IMPLICIT
		else:
			raise Exception("Illegal mode ({})".format(mode))
		print("out", self._mode_poisson, self.mode_poisson)

	def __str__(self):
		return ("Neumann" if self.mode_boundary == self.NEUMANN else "Diriclet") + \
		" with " + \
		("Explicit" if self.mode_poisson == self.EXPLICIT else "Implicit") 
		
	def __repr__(self):
		return self.__str__()

	def set_alpha(self, value:float):
		"""
		Set the alpha value

		Parameters
		----------
		value : float
			The alhpa value
		"""		
		self.alpha = value

	def get_laplace_explicit(self, data: Array[float, float] = None, alpha:bool = True) -> Array:
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
		if not alpha:
			return laplace
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
		self.alpha = 1

		upperdiag = np.concatenate(([0, 0], -self.alpha * np.ones(shape - 2)))
		upperdiag1 = np.concatenate(([0, 0], -self.alpha * np.ones(shape - 2)))

		centerdiag = np.concatenate(([1], (1 + 4 * self.alpha) * np.ones(shape - 2),
									 [1]))

		lowerdiag = np.concatenate((-self.alpha * np.ones(shape - 2), [0, 0]))
		lowerdiag1 = np.concatenate((-self.alpha * np.ones(shape - 2), [0, 0]))

		diags = np.array([upperdiag, upperdiag1, centerdiag, lowerdiag, lowerdiag1])

		A = spdiags(diags, [2, 1, 0, -1, -2], shape, shape).tocsc()
		print(A.shape)

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

	def get_laplace(self, data, alpha=True):
		"""
		Gets the correct laplace based on mode

		Parameters
		----------
		data : ndarray
			The data to get the laplace from
		"""		
		if self.mode_poisson == self.EXPLICIT:
			return self.get_laplace_explicit(data, alpha)
		elif self.mode_poisson == self.IMPLICIT:
			#return self.get_laplace_implicit(data)
			j = self.get_laplace_implicit(data)
			T = data.copy()
			for j in range(j.shape[0]):
				j[n + 1, :] = T
		else:
			raise Exception("not supported")

	def apply_boundary(self, data) -> Array:
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
			#print("Diriclet")
			return self.diriclet(data)
		else:
			raise Exception("not supported")

	def solve(self, data, operator, h=lambda x=None, i=None: 0, apply_boundary=True) -> Array:
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
			resultat = data.copy()
			if(len(data.shape) == 3):
				for i in range(3):
					resultat[1:-1, 1:-1, i] = resultat[1:-1, 1:-1, i] +  self.alpha * (operator(i) - h(i=i))
			else:
				resultat[1:-1, 1:-1] = resultat[1:-1, 1:-1] + self.alpha * (operator()- h(None))
		elif self.mode_poisson == self.IMPLICIT:
			if(len(data.shape) == 3):
				for i in range(3):#data.shape[-1]):
					data[:, :, i] = operator(i=i) - h(i=i)
			else:
				data[:, :] = operator() - h(data)
		else:
			raise Exception("Not supported")

		if apply_boundary:
			return self.apply_boundary(resultat).clip(0, 1)
		else:
			return resultat.clip(0, 1)


