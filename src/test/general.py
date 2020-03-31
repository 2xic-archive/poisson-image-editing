import numpy as np
from PyQt5 import QtCore


def test_rest(_qt_bot_, interface_app, setup_code=lambda x, y, z: 0):#, change_dimension=None):
	"""
	Make sure that all reset buttons work as they should
	"""

	"""
	BEFORE
	"""
	current_image = interface_app.method.data.copy()
	elemenets = []
	for index, i in enumerate(interface_app.screen_elements):
		elemenets.append(i.element.isEnabled())


	setup_code(_qt_bot_, interface_app, current_image)

	_qt_bot_.mousePress(interface_app.action_button, QtCore.Qt.LeftButton, delay=10)
	_qt_bot_.mouseRelease(interface_app.action_button, QtCore.Qt.LeftButton, delay=10)

	_qt_bot_.waitUntil(lambda: (interface_app.method.data.shape != current_image.shape) or not np.allclose(interface_app.method.data, current_image) , timeout=3000)

	_qt_bot_.waitUntil(lambda: interface_app.reset_button.isEnabled(), timeout=3000) 
	
	#	reset and verify that the state is the same
	_qt_bot_.mousePress(interface_app.reset_button, QtCore.Qt.LeftButton, delay=10)
	_qt_bot_.mouseRelease(interface_app.reset_button, QtCore.Qt.LeftButton, delay=10)

#	if custom_check is None:
	_qt_bot_.waitUntil(lambda: not interface_app.reset_button.isEnabled(), timeout=3000) 
#	_qt_bot_.waitUntil(lambda: not interface_app.reset_button.isEnabled(), timeout=3000) 
	
#	if not change_dimension is None:
#		change_dimension(_qt_bot_, interface_app, current_image)

	_qt_bot_.waitUntil(lambda: interface_app.method.data.shape == current_image.shape, timeout=3000) 
	_qt_bot_.waitUntil(lambda: np.allclose(interface_app.method.data, current_image), timeout=3000)

	"""
	AFTER
	"""
	for index, i in enumerate(interface_app.screen_elements):
		assert (elemenets[index] == i.element.isEnabled()), "error -> state is not the same after reset (index id: {}, {})".format(index, i.element.text())


	interface_app.close()


