#from test import *
import numpy as np
import unittest
from backend import matting
import os

class test_matting(unittest.TestCase):
	def test_fit(self):
		matting_object = matting.matting("./files/test_images/target.png", "./files/test_images/source.png")
		matting_object.po
		old_image = matting_object.get_data().copy()
		matting_object.fit(1)
		self.assertFalse(np.all(old_image == matting_object))