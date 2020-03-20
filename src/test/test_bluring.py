from test import *
import numpy as np
import unittest
import blurring

class test_blur(unittest.TestCase):
	def test_fit(self):
		path = os.path.dirname(os.path.abspath(__file__))
		blur_object = blurring.blur(PATH + "../files/test_images/lena.png", False)
		old_image = blur_object.get_data().copy()
		blur_object.fit(1)
		self.assertFalse(np.all(old_image == blur_object))

'''
from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api

def test_basics(qtbot):
#	assert qt_api.QApplication.instance() is not None
#	widget = qt_api.QWidget()
#	qtbot.addWidget(widget)
#	widget.setWindowTitle("W1")
#	widget.show()
	from blurring_qt import blur_window
	ex = blur_window()
	ex.initUI()
	ex.show()
	assert ex.isVisible()
	assert ex.windowTitle() == "W1"
'''