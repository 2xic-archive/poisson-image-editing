from test import *
import numpy as np
import unittest
import inpaiting

class test_inpaiting(unittest.TestCase):
	def test_fit(self):
		path = os.path.dirname(os.path.abspath(__file__))
		inpait_object = inpaiting.inpait(PATH + "../files/test_images/lena.png", False)
		old_image = inpait_object.get_data().copy()
		try:
			inpait_object.fit(1)
			self.assertFalse(True)
		except Exception as e:
			# should fail because we have not destroyed any information/set a mask
			pass
		inpait_object.destroy_information()
		inpait_object.fit(1)
		self.assertFalse(np.all(old_image == inpait_object))