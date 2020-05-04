import unittest
import numpy as np
from backend import demosaicing
from gui.interfaces import demosaic_qt
from PyQt5 import QtCore
#from test.general import *
import test.general 
import pytest

class test_demosaic(unittest.TestCase):
	def test_fit(self):
		demosaic_object = demosaicing.Demosaic("./files/test_images/lena.png", True)
		old_image = demosaic_object.get_data().copy()
		demosaic_object.simulate()
		demosaic_object.fit(1)
		self.assertFalse(np.all(old_image == demosaic_object))
	 
	def test_forgot_simulate(self):
		demosaic_object = demosaicing.Demosaic("./files/test_images/lena.png", True)
		old_image = demosaic_object.get_data().copy()
		try:
			demosaic_object.fit(1)
			self.assertFalse(True)
		except Exception as e:
			# should fail because we have not simulated  
			pass

#@pytest.mark.gui
def test_basics(qtbot):
	ex = demosaic_qt.demonsaic_window()
	ex.init_UI()
	ex.show()
	assert ex.isVisible()
	assert ex.windowTitle() == "lena.png"

	#qtbot.add_widget(ex)

	current_image = ex.method.data.copy()

	#	mosaic_button
	qtbot.mousePress(ex.mosaic_button, QtCore.Qt.LeftButton, delay=10)
	qtbot.mouseRelease(ex.mosaic_button, QtCore.Qt.LeftButton, delay=10)

	#	make sure change is made
	qtbot.waitUntil(lambda: not ex.method.data.shape == current_image.shape, timeout=3000) #np.allclose(ex.method.data, current_image), timeout=10000)
	#current_image = ex.method.data.copy()
	#current_image = ex.method.results.copy()

	qtbot.mousePress(ex.action_button, QtCore.Qt.LeftButton, delay=10)
	qtbot.mouseRelease(ex.action_button, QtCore.Qt.LeftButton, delay=10)

	print(ex.method.data.shape)

	def view_updated():
		print(1, ex.method.data.shape == current_image.shape)
		return ( ex.method.data.shape == current_image.shape)

		# np.allclose(ex.method.data, current_image) #view_model.count() > 10

	qtbot.wait(300)
	qtbot.waitUntil(view_updated)
	ex.close()


#@pytest.mark.gui
def test_noisy_clicker(qtbot):
#	ex = demosaic_qt.demonsaic_window()
	def setup(qtbot, ex, current_image):
		qtbot.mousePress(ex.mosaic_button, QtCore.Qt.LeftButton, delay=10)
		qtbot.mouseRelease(ex.mosaic_button, QtCore.Qt.LeftButton, delay=10)

		qtbot.wait(300)
		qtbot.waitUntil(lambda: not ex.method.data.shape == current_image.shape, timeout=3000) 

	ex = demosaic_qt.demonsaic_window()
	ex.init_UI()
	ex.show()


	test.general.test_rest(qtbot, ex, setup)

	'''
	"""
	Make sure that all reset buttons work as they should
	"""
	ex = demosaic_qt.demonsaic_window()
	ex.init_UI()
	ex.show()

	"""
	BEFORE
	"""
	current_image = ex.method.data.copy()
	elemenets = []
	for index, i in enumerate(ex.screen_elements):
		elemenets.append(i.element.isEnabled())
	#	i.index_id = index

	#	press some buttons
	qtbot.mousePress(ex.mosaic_button, QtCore.Qt.LeftButton, delay=10)
	qtbot.mouseRelease(ex.mosaic_button, QtCore.Qt.LeftButton, delay=10)

	qtbot.waitUntil(lambda: not ex.method.data.shape == current_image.shape, timeout=3000) 

	qtbot.mousePress(ex.action_button, QtCore.Qt.LeftButton, delay=10)
	qtbot.mouseRelease(ex.action_button, QtCore.Qt.LeftButton, delay=10)

	qtbot.waitUntil(lambda: ex.reset_button.isEnabled(), timeout=3000) 

	#	reset and verify that the state is the same
	qtbot.mousePress(ex.reset_button, QtCore.Qt.LeftButton, delay=10)
	qtbot.mouseRelease(ex.reset_button, QtCore.Qt.LeftButton, delay=10)

	qtbot.waitUntil(lambda: ex.method.data.shape == current_image.shape, timeout=3000) 

	qtbot.waitUntil(lambda: not np.allclose(ex.method.data, current_image), timeout=3000)

	qtbot.waitUntil(lambda: not ex.reset_button.isEnabled(), timeout=3000) 

	"""
	AFTER
	"""
	for index, i in enumerate(ex.screen_elements):
		assert (elemenets[index] == i.element.isEnabled()), "error -> state is not the same after reset (index id: {}, {})".format(index, i.element.text())
	'''





