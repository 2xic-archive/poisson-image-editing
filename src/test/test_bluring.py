import os
import platform
import unittest
from PyQt5 import QtCore
import numpy as np
from backend import blurring
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

	def test_fit_implicit(self):
		blur_object = blurring.blur("./files/test_images/lena.png", False)
		blur_object.mode_poisson = blur_object.IMPLICIT
		old_image = blur_object.get_data().copy()
		blur_object.fit(1)
		self.assertFalse(np.all(old_image == blur_object))


def test_basics(qtbot):
	ex = blurring_qt.blur_window()
	ex.init_UI()
	ex.show()
	assert ex.isVisible()
	assert ex.windowTitle() == "lena.png"

	qtbot.add_widget(ex)

	# press the button and wait for action
	qtbot.mousePress(ex.action_button, QtCore.Qt.LeftButton, delay=10)
	qtbot.mouseRelease(ex.action_button, QtCore.Qt.LeftButton, delay=10)
	qtbot.waitUntil(lambda: "total" in ex.epoch_label.text().lower(), timeout=10000)

	# the result should be almost the same as running it without the gui
	blur_object = blurring.blur("./files/test_images/lena.png", False)
	old_image = blur_object.get_data().copy()
	blur_object.fit(1)		
	assert(np.allclose(ex.method.data, blur_object.data))

	# press the button and wait for action
	qtbot.mousePress(ex.reset_button, QtCore.Qt.LeftButton, delay=10)
	qtbot.mouseRelease(ex.reset_button, QtCore.Qt.LeftButton, delay=10)
	qtbot.waitUntil(lambda: not "total" in ex.epoch_label.text().lower(), timeout=10000)
	assert(not np.allclose(ex.method.data, blur_object.data))









