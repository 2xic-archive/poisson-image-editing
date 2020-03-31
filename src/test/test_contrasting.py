import unittest
import numpy as np
from backend import contrasting
from extra import local_adaptive_histogram
from gui.interfaces import contrast_qt
import test.general 

class test_contrast(unittest.TestCase):
	def test_fit(self):
		contrast_object = contrasting.Contrast("./files/test_images/contrast.jpg", False)
		old_image = contrast_object.get_data().copy()
		contrast_object.fit(1)
		self.assertFalse(np.all(old_image == contrast_object))

	def test_extra(self):
		contrast_object = contrasting.Contrast("./files/test_images/contrast.jpg", False)
		local_adaptive_histogram.contrast_enhancement(contrast_object.data)

def test_noisy_clicker(qtbot):
	ex = contrast_qt.contrast_window()
	ex.init_UI()
	ex.show()

	test.general.test_rest(qtbot, ex)

