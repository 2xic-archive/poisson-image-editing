#from test import *
import numpy as np
import unittest
from backend import grayscale
import os

class test_grayscale(unittest.TestCase):
	def test_fit(self):
		grayscale_object = grayscale.grayscale("./files/test_images/lena.png")
		old_image = grayscale_object.get_data().copy()
		grayscale_object.fit(1)
		self.assertFalse(np.all(old_image == grayscale_object))