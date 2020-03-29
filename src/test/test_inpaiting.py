import unittest
import numpy as np
from backend import inpaiting
from gui.interfaces import inpaiting_qt
from PyQt5 import QtCore


class test_inpaiting(unittest.TestCase):
    def test_fit(self):
        inpaint_object = inpaiting.inpaint("./files/test_images/lena.png", False)
        old_image = inpaint_object.get_data().copy()
        try:
            inpaint_object.fit(1)
            self.assertFalse(True)
        except Exception as e:
            # should fail because we have not destroyed any information/set a mask
            pass
        inpaint_object.destroy_information()
        inpaint_object.fit(1)
        self.assertFalse(np.all(old_image == inpaint_object))


def test_basics(qtbot):
    ex = inpaiting_qt.inpait_window()
    ex.init_UI()
    ex.show()
    assert ex.isVisible()
    assert ex.windowTitle() == "lena.png"

    qtbot.add_widget(ex)

    current_image = ex.method.data.copy()

    # we first need to delete some information from the image
    qtbot.mousePress(ex.noise_button, QtCore.Qt.LeftButton, delay=10)
    qtbot.mouseRelease(ex.noise_button, QtCore.Qt.LeftButton, delay=10)

    #	make sure change is made
    qtbot.waitUntil(lambda: not np.allclose(ex.method.data, current_image), timeout=10000)

    # the result should be almost the same as running it without the gui
    inpaiting_object = inpaiting.inpaint("./files/test_images/lena.png", False)
    # old_image = inpaiting_object.get_data().copy()

    inpaiting_object.mask = ex.method.mask.copy()
    inpaiting_object.original_data = ex.method.original_data.copy()
    inpaiting_object.data = ex.method.data.copy()

    # press the button and wait for action
    qtbot.mousePress(ex.action_button, QtCore.Qt.LeftButton, delay=10)
    qtbot.mouseRelease(ex.action_button, QtCore.Qt.LeftButton, delay=10)
    print(ex.epoch_label.text().lower())
    qtbot.waitUntil(lambda: "total" in ex.epoch_label.text().lower(), timeout=10000)

    inpaiting_object.fit(epochs=1)
    assert (np.allclose(ex.method.data, inpaiting_object.data))

    # press the button and wait for action
    qtbot.mousePress(ex.extra_button, QtCore.Qt.LeftButton, delay=10)
    qtbot.mouseRelease(ex.extra_button, QtCore.Qt.LeftButton, delay=10)

    old_frame = ex.frameGeometry().width()
    qtbot.waitUntil(lambda: not ex.frameGeometry().width() == old_frame, timeout=10000)

    # press the button and wait for action
    qtbot.mousePress(ex.extra_action_button, QtCore.Qt.LeftButton, delay=10)
    qtbot.mouseRelease(ex.extra_action_button, QtCore.Qt.LeftButton, delay=10)

    old = ex.extra_label.pixmap().toImage()
    qtbot.waitUntil(lambda: not old == ex.extra_label.pixmap().toImage(), timeout=10000)

    qtbot.mousePress(ex.reset_button, QtCore.Qt.LeftButton, delay=10)
    qtbot.mouseRelease(ex.reset_button, QtCore.Qt.LeftButton, delay=10)
    qtbot.waitUntil(lambda: not "total" in ex.epoch_label.text().lower(), timeout=10000)
