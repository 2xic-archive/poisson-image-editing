from nptyping import Array

class Boundary:
	"""
	This class describes the boundary conditions
	"""

	def __init__(self, u0=None):
		#self.data = None
		self.u0 = u0

	def set_u0(self, data):
		"""
		Sets the u 0.

		Used with diriclet

		Parameters
		----------
		data : ndarray
			the original image
		"""
		self.u0 = data

	def neumann(self, data: Array[float, float] = None):
		"""
		Applies a neumann boundary

		Parameters
		----------
		data : ndarray
			The data to preform the boundary on

		Returns
		-------
		ndarray
			The data with a applied boundary
		"""
		if data is None:
			data = self.data

		# Neumann randbetingelse
		data[:, 0] = data[:, 1]
		data[:, -1] = data[:, -2]
		data[0, :] = data[1, :]
		data[-1, :] = data[-2, :]
		return data.clip(0, 1)

	def diriclet(self, data: Array[float, float] = None, mask=None):
		"""
		Applies a diriclet boundary
	
		Parameters
		----------
		data : ndarray
			The data to preform the boundary on
		mask : ndarray
			if you are using a mask for the boundary

		Returns
		-------
		ndarray
			The data with a applied boundary
		"""
		if(mask is None):
			data[:, 0] = self.data_copy[:, 1]
			data[:, -1] = self.data_copy[:, -2]
			data[0, :] =  self.data_copy[1, :]
			data[-1, :] =  self.data_copy[-2, :]
		else:
			#data[~mask.astype(bool)] = self.data_copy[~mask.astype(bool)] 
			data[~mask.astype(bool)] = self.data_copy[~mask.astype(bool)] 
			
		return data.clip(0, 1)
