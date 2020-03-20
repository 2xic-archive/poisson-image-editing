#import cv2
import image_handler
import poisson
import numpy as np
from PIL import Image
import blurring

class anonymous(image_handler.ImageHandler, poisson.poisson):
	def __init__(self, path, color=False):
		image_handler.ImageHandler.__init__(self, path, color)
		poisson.poisson.__init__(self)
		self.alpha = 0.1
		self.mask = self.get_mask(self.data, path)
		self.u0 = self.data.copy()
	
	def get_mask(self, input_image, path):
		import cv2
		face_cascade = cv2.CascadeClassifier('../haarcascade_frontalface_default.xml')
		img = cv2.imread(path)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.1, 4)
		for (x, y, w, h) in faces:
			return (x, x + w, y, y + h)

	def iteration(self):
		"""
		[TODO:summary]

		[TODO:description]
		"""		
		blur = blurring.blur(None)
		blur.set_data(self.data.copy()[self.mask[0]:self.mask[1], self.mask[2]:self.mask[3]])
		self.data[self.mask[0]:self.mask[1], self.mask[2]:self.mask[3]] = blur.iteration()

	def fit(self,epochs):
		"""
		[TODO:summary]

		[TODO:description]

		Parameters
		----------
		epochs : int
			The iteration count
		"""
		for i in range(epochs):
			self.iteration()
		return self
