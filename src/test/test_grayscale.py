#from test import *
import unittest
import numpy as np
from backend import grayscale
#from gui
from gui.interfaces import grayscale_qt
from PyQt5 import QtCore
#from test.general import *
import test.general 


class test_grayscale(unittest.TestCase):
	def test_fit(self):
		grayscale_object = grayscale.grayscale("./files/test_images/lena.png")
		old_image = grayscale_object.get_data().copy()
		grayscale_object.fit(1)
		self.assertFalse(np.all(old_image == grayscale_object))

	def test_reset(self):
		grayscale_object = grayscale.grayscale("./files/test_images/lena.png")
		old_image = grayscale_object.get_data().copy()
		grayscale_object.fit(1)
		grayscale_object.reset()
		assert(np.allclose(old_image, grayscale_object.get_data()))

def test_noisy_clicker(qtbot):
	ex = grayscale_qt.grayscale_window()
	ex.init_UI()
	ex.show()

#	def test_extra(qtbot, ex, current_image):
#		qtbot.waitUntil(lambda: ex.action_button.isEnabled(), timeout=3000) 

	test.general.test_rest(qtbot, ex)#, change_dimension=test_extra)
