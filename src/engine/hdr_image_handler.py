
import numpy as np
from engine import image_handler
from itertools import combinations
import scipy.io


"""
TODO : I now see that multiple solutions to the problem is mentioned in the project description	*awkward* will try them out
"""


# NOTE : THIS DOES NOT SEEM TO WORK 
#https://stackoverflow.com/questions/33559946/numpy-vs-mldivide-matlab-operator
def matlab_mdivide(A, b):
	num_vars = A.shape[1]
	rank = np.linalg.matrix_rank(A)
	sol = None
	if rank == num_vars:              
		sol = np.linalg.lstsq(A, b)[-1]    # not under-determined
	else:
		sol = np.zeros((num_vars, 1))  
		print("??")
		for nz in combinations(range(num_vars), rank):    # the variables not set to zero
			try: 
				sol[nz, :] = np.asarray(np.linalg.solve(A[:, nz], b))
				print(sol)
			except np.linalg.LinAlgError:     
				pass                    # picked bad variables, can't solve
	#	print(sol.shape, num_vars)
	return sol

# as defined in equation 3
def weigth_function(intensity):
	if(intensity <= 128):
		return intensity
	return 255 - intensity

class hdr_handler:
	def __init__(self):
		self.images = [
			image_handler.ImageHandler('../hdr-bilder/Adjuster/Adjuster_00064.png' ),
			image_handler.ImageHandler('../hdr-bilder/Adjuster/Adjuster_00128.png' ),
			image_handler.ImageHandler('../hdr-bilder/Adjuster/Adjuster_00256.png' ),
			image_handler.ImageHandler('../hdr-bilder/Adjuster/Adjuster_00512.png' )
		]
		for i in range(len(self.images)):
			self.images[i].data *= 255
#			self.images[i].data
			self.images[i].data = self.images[i].data.astype(np.uint8).astype(np.float64) #np.ceil(self.images[i].data)
#			assert(1 < self.images[i].data.max())

		# make sure we have all images in the correct interval between 0 and 255
		for i in range(len(self.images)):
			assert(1 < self.images[i].data.max())
		self.B = np.array([
			np.log(64),
			np.log(128),
			np.log(256),
			np.log(512)
		])#.reshape(1, 4)

		self.pixel_area = self.images[0].data.shape
		self.pixel_area = self.pixel_area[0] * self.pixel_area[1]
		self.l = 100 # is lamdba, the constant that determines the amount of smoothness
		
	
		self.Z = scipy.io.loadmat("./files/Z.mat")["Z"]
		#self.sample()

	def get_pixel(self, image, sample):
		results = np.zeros(sample.shape)
		#print(sample.shape)
		image_flat = image.flatten()
		for index, i in enumerate(sample.flatten()):
#			print(image_flat.shape)
#			print(i)
#			print(image_flat[int(i)], index)
			results[:, index] = image_flat[int(i)]
		#print(results.shape)
		return results


	def sample(self, size=100):
		sample_space = np.ceil(np.random.rand(1, size) * self.pixel_area)

		Z = np.zeros((size, len(self.images), 3))
		for index, image in enumerate(self.images):
			# rgb
			for channel in range(3):
			#	print(sample_space.shape)
			#	print(image.data.shape)
			#	print(Z.shape)
			#	print(self.get_pixel(image.data, sample_space).shape)
				Z[:, index, channel] = self.get_pixel(image.data, sample_space)#.reshape()
		import scipy.io
		scipy.io.savemat('./files/Z.mat', dict(Z=Z))
		exit(0)
		return Z

	def get_radiance(self):
		self.radiance = np.zeros((255, 3))
		for channel in range(3):
			g, lE =  self.gsolve(self.Z[:, :, channel], channel)
			self.radiance[:, channel] = g[:]

		return self.radiance

	def gsolve(self, Z, index):
		
#		print(Z)
#		exit(0)
		n = 256
		A = np.zeros((Z.shape[0] * Z.shape[1] + n + 1, n + Z.shape[0] ))
		b = np.zeros((A.shape[0], 1))

	#	print(Z.shape[0] * Z.shape[1] )
	#	print(A.shape)
	#	exit(0)
		k = 1
		for i in range(Z.shape[0]):
			for j in range(Z.shape[1]):
				Z_ij = int(Z[i, j])
				w_ij = weigth_function(Z_ij + 1)
				A[k, Z_ij + 1] = w_ij
				A[k, n + 1] = -w_ij

				b[k, 0] = w_ij * self.B[j]
				k += 1

		A[k, 129] = 1
		k += 1
		for i in range(0, n -2 ):
			A[k, i] = self.l * weigth_function(i + 1)
			A[k, i + 1] = -2 * self.l * weigth_function(i + 1)
			A[k, i + 2] = self.l * weigth_function(i + 1)
			k += 1

#		print(Z)
		A[k, 129] = 0
#		print(np.all(A == 0))
#		print(A[np.nonzero(A)].shape)
#		print(A[:100, :10])
#		exit(0)			
#		np.savetxt("filename_Z", Z, newline=" ")
#		np.savetxt("filename_A", A, newline=" ")
#		np.savetxt("filename_b", b, newline=" ")
#		print(A[np.nonzero(A)].shape)
#		x = matlab_mdivide(A,b)[-1]
#		print(A.shape)
#		print(b.shape)
		
		from scipy.optimize import nnls

		a_matlab = scipy.io.loadmat("./files/matlab_a {}.mat".format(index + 1))["A"]	
		b_matlab = scipy.io.loadmat("./files/matlab_b {}.mat".format(index + 1))["b"]	
		x_matlab = scipy.io.loadmat("./files/matlab_x {}.mat".format(index + 1))["x"]	
		print((b - b_matlab).sum())
		print((A - a_matlab).sum())
#		print(b_matlab)
		x = (nnls(A, b[:, 0]))[0]
		print((x_matlab - x).sum())
		exit(0)
#		exit(0)

		g = x[1:n]
		lE = x[n+1:x.shape[0]]
		return g, lE
	'''
	def get_pixel(self, i, j):
		# From matlab
		# %  Z(i,j) is the pixel values of pixel location number i in image j
		return self.images[j][i]
	'''

	def look_up_pixel(self, radiance, image):
		out_image = np.zeros((image.shape))
		for i in range(image.shape[0]):
			for j in range(image.shape[1]):
				out_image[i, j] = radiance[int(image[i, j]) - 1]
		return out_image
	'''
	Equation 6 from the paper
	'''
	def get_radiance_log(self, radiance):
		x = np.ones(self.images[0].data.shape)
		y = np.zeros(self.images[0].data.shape)

		for index, i in enumerate(self.images):
			g = i.data.copy()
			for rgb in range(3):
				g[:, :, rgb] = self.look_up_pixel(radiance[:, rgb], g[:, :, rgb])
			g -= self.B[index]
			f =  np.vectorize(weigth_function)
			wi = f(g.copy())
			x += wi * g
			y += wi
#		print(np.max(x/y))
		rad = (x/y)
		return rad #(x/y).clip(0, 255)

	def get_shutter_speed(self, j):
		#	From matlab: 
		#	is the log delta t, or log shutter speed, for image j
		return self.images[j].get_shutter()

#	def gsolve(self, image, B):
#		pass

	def solve(self):
		for img in self.images:
			self.gsolve(img)