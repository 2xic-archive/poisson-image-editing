from test import *
import numpy as np
import unittest
import matting

class test_matting(unittest.TestCase):
	def test_fit(self):
		path = os.path.dirname(os.path.abspath(__file__))
		matting_object = matting.matting(PATH + "../files/test_images/target.png", PATH + "../files/test_images/source.png")
		old_image = matting_object.get_data().copy()
		matting_object.fit(1)
		self.assertFalse(np.all(old_image == matting_object))