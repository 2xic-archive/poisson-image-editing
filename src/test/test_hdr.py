#from test import *
import numpy as np
import unittest
from engine import hdr_image_handler
import os
import scipy.io

class test_hdr_image_handler(unittest.TestCase):
	def test_matlab(self):
		hdr = hdr_image_handler.hdr_handler()
		matlab_Z = scipy.io.loadmat("./test/test_files/Z.mat")["Z"]

		matlab_A = scipy.io.loadmat("./test/test_files/matlab_a 1.mat")["A"]
		matlab_b = scipy.io.loadmat("./test/test_files/matlab_b 1.mat")["b"]
		
		A, b, n = hdr.get_Ab(matlab_Z[:, :, 0])

		np.allclose(A, matlab_A)
		np.allclose(b, matlab_b)



#		grayscale_object = grayscale.grayscale("./files/test_images/lena.png")
#		old_image = grayscale_object.get_data().copy()
#		grayscale_object.fit(1)
#		self.assertFalse(np.all(old_image == grayscale_object))