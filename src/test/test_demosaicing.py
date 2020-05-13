import unittest

import numpy as np
from PyQt5 import QtCore

# from test.general import *
import test.general
from backend import demosaicing
from gui.interfaces import demosaic_qt


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

def test_basics(qtbot):
    ex = demosaic_qt.demonsaic_window()
    ex.init_UI()
    ex.show()
    assert ex.isVisible()
    assert ex.windowTitle() == "lena.png"

    # qtbot.add_widget(ex)

    current_image = ex.method.data.copy()

    #	mosaic_button
    qtbot.mousePress(ex.mosaic_button, QtCore.Qt.LeftButton, delay=10)
    qtbot.mouseRelease(ex.mosaic_button, QtCore.Qt.LeftButton, delay=10)

    #	make sure change is made
    qtbot.waitUntil(lambda: not ex.method.data.shape == current_image.shape,
                    timeout=3000)  # np.allclose(ex.method.data, current_image), timeout=10000)
    # current_image = ex.method.data.copy()
    # current_image = ex.method.results.copy()

    qtbot.mousePress(ex.action_button, QtCore.Qt.LeftButton, delay=10)
    qtbot.mouseRelease(ex.action_button, QtCore.Qt.LeftButton, delay=10)

    def view_updated():
        return (ex.method.data.shape == current_image.shape)

    qtbot.wait(300)
    qtbot.waitUntil(view_updated)
    ex.close()


def test_noisy_clicker(qtbot):
    def setup(qtbot, ex, current_image):
        qtbot.mousePress(ex.mosaic_button, QtCore.Qt.LeftButton, delay=10)
        qtbot.mouseRelease(ex.mosaic_button, QtCore.Qt.LeftButton, delay=10)

        qtbot.wait(300)
        qtbot.waitUntil(lambda: not ex.method.data.shape == current_image.shape, timeout=3000)

    ex = demosaic_qt.demonsaic_window()
    ex.init_UI()
    ex.show()

    test.general.test_rest(qtbot, ex, setup)
