from test import *
import numpy as np
import unittest
import grayscale

class test_grayscale(unittest.TestCase):
	def test_fit(self):
		path = os.path.dirname(os.path.abspath(__file__))
		grayscale_object = grayscale.grayscale()
		old_image = grayscale_object.get_data().copy()
		grayscale_object.fit(1)
		self.assertFalse(np.all(old_image == grayscale_object))