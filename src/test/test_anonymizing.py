import os
import unittest

import numpy as np

# from test.general import *
import test.general
from backend import anonymizing
from gui.interfaces import anonymizing_qt


class test_Anonymous(unittest.TestCase):
    def test_fit(self):
        path = os.path.dirname(os.path.abspath(__file__))
        anonymous_object = anonymizing.Anonymous("./files/test_images/lena.png", False)
        old_image = anonymous_object.get_data().copy()
        anonymous_object.fit(1)
        self.assertFalse(np.all(old_image == anonymous_object))


def test_noisy_clicker(qtbot):
    ex = anonymizing_qt.anonymizing_window()
    ex.init_UI()
    ex.show()

    test.general.test_rest(qtbot, ex)
