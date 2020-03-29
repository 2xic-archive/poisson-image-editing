import unittest
import numpy as np
from backend import demosaicing
from gui.interfaces import demosaic_qt
from PyQt5 import QtCore

class test_demosaic(unittest.TestCase):
    def test_fit(self):
        demosaic_object = demosaicing.Demosaic("./files/test_images/lena.png", True)
        old_image = demosaic_object.get_data().copy()
        demosaic_object.fit(1)
        self.assertFalse(np.all(old_image == demosaic_object))
     
def test_basics(qtbot):
	ex = demosaic_qt.demonsaic_window()
	ex.init_UI()
	ex.show()
	assert ex.isVisible()
	assert ex.windowTitle() == "lena.png"

	qtbot.add_widget(ex)

	current_image = ex.method.data.copy()

	#	mosaic_button
	# we first need to delete some information from the image
	qtbot.mousePress(ex.mosaic_button, QtCore.Qt.LeftButton, delay=10)
	qtbot.mouseRelease(ex.mosaic_button, QtCore.Qt.LeftButton, delay=10)

	#	make sure change is made

	qtbot.mousePress(ex.action_button, QtCore.Qt.LeftButton, delay=10)
	qtbot.mouseRelease(ex.action_button, QtCore.Qt.LeftButton, delay=10)

	qtbot.mousePress(ex.action_button, QtCore.Qt.LeftButton, delay=10)
	qtbot.mouseRelease(ex.action_button, QtCore.Qt.LeftButton, delay=10)

	qtbot.waitUntil(lambda: not np.allclose(ex.method.data, current_image), timeout=10000)
