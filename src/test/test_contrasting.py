#from test import *
import numpy as np
import unittest
from backend import contrasting
import os
from extra import local_adaptive_histogram

class test_contrast(unittest.TestCase):
	def test_fit(self):
		contrast_object = contrasting.Contrast("./files/test_images/contrast.jpg", False)
		old_image = contrast_object.get_data().copy()
		contrast_object.fit(1)
		self.assertFalse(np.all(old_image == contrast_object))

	def test_extra(self):
		contrast_object = contrasting.Contrast("./files/test_images/contrast.jpg", False)
		local_adaptive_histogram.contrast_enhancement(contrast_object.data)