#from test import *
import numpy as np
import unittest
from backend import blurring
import platform
import os
from gui.interfaces import blurring_qt


# Because travis does not have a screen ~
if not (platform.system() == "Darwin"):
	from pyvirtualdisplay import Display
	display = Display(visible=0, size=(1366, 768))
	display.start()

class test_blur(unittest.TestCase):
	def test_fit(self):
		path = os.path.dirname(os.path.abspath(__file__))
		blur_object = blurring.blur("./files/test_images/lena.png", False)
		old_image = blur_object.get_data().copy()
		blur_object.fit(1)
		self.assertFalse(np.all(old_image == blur_object))

from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api

def test_basics(qtbot):
	ex = blurring_qt.blur_window()
	ex.init_UI()
	ex.show()
	assert ex.isVisible()
	assert ex.windowTitle() == "lena.png"