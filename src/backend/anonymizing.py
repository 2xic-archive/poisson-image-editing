import os
from engine import image_handler, poisson
from backend import blurring

from engine.image_handler import ImageHandler
import numpy as np
from engine import boundary
from nptyping import Array

def get_mask(path: str) -> list:
	"""
	Get the mask to blur a face


	Parameters
	----------
	path : str
		path to the image file to anonymize

	Returns
	-------
	list
		a list with bounding boxes of (x, x1, y, y1) for the faces
	"""
	from cv2 import CascadeClassifier, imread, cvtColor, COLOR_BGR2GRAY
	face_cascade = CascadeClassifier('./files/haarcascade_frontalface_default.xml')
	img = imread(path)
	gray = cvtColor(img, COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.1, 4)
	results = []
	for (x, y, w, h) in faces:
		results.append([x, x + w, y, y + h])
	return results


class anonymous(image_handler.ImageHandler, poisson.poisson, boundary.Boundary):
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
	mask: list

	def __init__(self, path: str, color: bool = True):
		image_handler.ImageHandler.__init__(self, path, color)
		poisson.poisson.__init__(self)
		boundary.Boundary.__init__(self)

		self.alpha: float = 0.1
		self.mask = get_mask(path)
		self.u0 = self.data.copy()
		self.set_u0(self.u0)

	def iteration(self) -> Array:
		"""
		Does one iteration of the method.

		Returns
		-------
		ndarray
			returns the new computed image
		"""
		blur = blurring.blur(None)
		for mask in self.mask:
			blur.set_data(self.data.copy()[mask[0]:mask[1], mask[2]:mask[3]])
			blur.set_boundary("neumann")
			self.data[mask[0]:mask[1], mask[2]:mask[3]] = blur.iteration()

			# creates the mask for diriclet
			data_mask = np.ones((self.data.shape))
			data_mask[mask[0]:mask[1], mask[2]:mask[3]] = 0

			self.data = self.diriclet(self.data, data_mask)
		return self.data

	def fit(self, epochs: int):# -> anonymous:
		"""
		Makes multiple iterations of the method

		Calls iteration as many times as spesifed in by the parameter epochs

		Parameters
		----------
		epochs : int
			The iteration count

		Returns
		-------
		anonymous
			returns self
		"""
		for _ in range(epochs):
			self.iteration()
		return self
