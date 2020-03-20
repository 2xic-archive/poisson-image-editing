from test import *
import numpy as np
import unittest
import inpaiting

class test_inpaiting(unittest.TestCase):
	def test_fit(self):
		path = os.path.dirname(os.path.abspath(__file__))
		inpaint_object = inpaiting.inpaint(PATH + "../files/test_images/lena.png", False)
		old_image = inpaint_object.get_data().copy()
		try:
			inpaint_object.fit(1)
			self.assertFalse(True)
		except Exception as e:
			# should fail because we have not destroyed any information/set a mask
			pass
		inpaint_object.destroy_information()
		inpaint_object.fit(1)
		self.assertFalse(np.all(old_image == inpaint_object))