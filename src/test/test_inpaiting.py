import os
import sys
import numpy as np

PATH = os.path.dirname(os.path.abspath(__file__)) 
PATH += "/" if not PATH.endswith("/") else ""

print(PATH)
sys.path.append(PATH + "../")

import unittest
import inpaiting

class test_inpaiting(unittest.TestCase):
	def test_fit(self):
		path = os.path.dirname(os.path.abspath(__file__))
		x = inpaiting.inpait(PATH + "../test_images/lena.png", False)
		old = x.data.copy()
		try:
			x.fit(1)
			self.assertFalse(True)
		except Exception as e:
			# should fail because we have not destroyed any information/set a mask
			pass
		x.destroy_information()
		x.fit(1)
		self.assertFalse(np.all(old == x.data))