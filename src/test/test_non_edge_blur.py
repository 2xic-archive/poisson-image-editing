import unittest
import numpy as np
from backend import non_edge_blurring


class test_blur(unittest.TestCase):
	def test_fit(self):
		blur_object = non_edge_blurring.non_edge_blur("./files/test_images/lena.png", False)
		old_image = blur_object.get_data().copy()
		blur_object.fit(1)
		self.assertFalse(np.all(old_image == blur_object))
