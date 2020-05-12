import os
import platform
import unittest

import numpy as np
from PyQt5 import QtCore

from backend import blurring
# from test.general import *
from gui.interfaces import blurring_qt

# Because travis does not have a screen ~
if not (platform.system() == "Darwin"):
    from pyvirtualdisplay import Display

    display = Display(visible=0, size=(1366, 768))
    display.start()


class test_Blur(unittest.TestCase):
    def test_fit(self):
        path = os.path.dirname(os.path.abspath(__file__))
        blur_object = blurring.Blur("./files/test_images/lena.png", False)
        old_image = blur_object.get_data().copy()
        blur_object.fit(1)
        self.assertFalse(np.all(old_image == blur_object))


def test_color_switch(qtbot):
    ex = blurring_qt.blur_window()
    ex.init_UI()
    ex.show()

    old_image = ex.method.data.copy()

    qtbot.waitUntil(lambda: ex.color_checkbox.checkState() == QtCore.Qt.Unchecked, timeout=10000)

    with qtbot.waitExposed(ex.color_checkbox, timeout=500):
        qtbot.mousePress(ex.color_checkbox, QtCore.Qt.LeftButton, delay=10)
        qtbot.mouseRelease(ex.color_checkbox, QtCore.Qt.LeftButton, delay=10)

    ex.color_checkbox.setChecked(True)

    qtbot.waitUntil(lambda: ex.color_checkbox.checkState() == QtCore.Qt.Checked, timeout=10000)
    qtbot.waitUntil(lambda: not ex.method.data.shape == old_image.shape, timeout=10000)

    ex.color_checkbox.setChecked(False)
    qtbot.waitUntil(lambda: ex.color_checkbox.checkState() == QtCore.Qt.Unchecked, timeout=10000)
    qtbot.waitUntil(lambda: not "total" in ex.epoch_label.text().lower(), timeout=10000)

    qtbot.waitUntil(lambda: ex.method.data.shape == old_image.shape, timeout=10000)

    ex.close()
    del ex


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
    qtbot.waitUntil(lambda: "total" in ex.epoch_label.text().lower() and
                            ex.reset_button.isEnabled(), timeout=10000)

    # the result should be almost the same as running it without the gui
    blur_object = blurring.Blur("./files/test_images/lena.png", False)
    old_image = blur_object.get_data().copy()
    blur_object.fit(1)

    assert (np.allclose(ex.method.data, blur_object.data))

    # press the button and wait for action
    qtbot.mousePress(ex.reset_button, QtCore.Qt.LeftButton, delay=10)
    qtbot.mouseRelease(ex.reset_button, QtCore.Qt.LeftButton, delay=10)
    qtbot.waitUntil(lambda: not "total" in ex.epoch_label.text().lower(), timeout=10000)
    assert (not np.allclose(ex.method.data, blur_object.data))
    ex.close()
    del ex
