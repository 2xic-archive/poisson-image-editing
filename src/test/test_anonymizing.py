import numpy as np
import unittest
from backend import anonymizing
import os
from gui.interfaces import anonymizing_qt
from PyQt5 import QtCore
#from test.general import *
import test.general 


class test_anonymous(unittest.TestCase):
	def test_fit(self):
		path = os.path.dirname(os.path.abspath(__file__))
		anonymous_object = anonymizing.anonymous("./files/test_images/lena.png", False)
		old_image = anonymous_object.get_data().copy()
		anonymous_object.fit(1)
		self.assertFalse(np.all(old_image == anonymous_object))


def test_noisy_clicker(qtbot):
	ex = anonymizing_qt.anonymizing_window()
	ex.init_UI()
	ex.show()

	test.general.test_rest(qtbot, ex)