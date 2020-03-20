
class poisson:
	def __init__(self):
		pass

	def get_laplance(self, data=None):
		if(data is None):
			data = self.data
		laplace = data[0:-2, 1:-1] \
				+ data[2:, 1:-1] \
				+ data[1:-1, 0:-2] \
				+ data[1:-1, 2:]   \
				- 4 * data[1:-1, 1:-1]
		return laplace