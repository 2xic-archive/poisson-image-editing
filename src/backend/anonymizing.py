import os
from engine import image_handler, poisson
from backend import blurring

from gui.general import get_path


def get_mask(path):
	"""
	Get the mask to blur a face


	Parameters
	----------
	path : str
		path to the image file to anonymize
	"""	
	from cv2 import CascadeClassifier, imread, cvtColor, COLOR_BGR2GRAY
	face_cascade = CascadeClassifier(get_path(__file__) + '../files/haarcascade_frontalface_default.xml')
	img = imread(path)
	gray = cvtColor(img, COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.1, 4)
	for (x, y, w, h) in faces:
		return x, x + w, y, y + h


class anonymous(image_handler.ImageHandler, poisson.poisson):
	"""
	This class describes a anymous image.

	This contains all the functions needed to anonymize a image over multiple iterations

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
		self.alpha = 0.1
		self.mask = get_mask(path)
		self.u0 = self.data.copy()

	def iteration(self):
		"""
		Does one iteration of the method.

		"""
		blur = blurring.blur(None)
		blur.set_data(self.data.copy()[self.mask[0]:self.mask[1], self.mask[2]:self.mask[3]])
		self.data[self.mask[0]:self.mask[1], self.mask[2]:self.mask[3]] = blur.iteration()

	def fit(self,epochs):
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
