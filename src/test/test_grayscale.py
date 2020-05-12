# from test import *
import unittest

import numpy as np
import pytest

# from test.general import *
import test.general
from backend import grayscale
# from gui
from gui.interfaces import grayscale_qt


class test_Grayscale(unittest.TestCase):
    def test_fit(self):
        grayscale_object = grayscale.Grayscale("./files/test_images/lena.png")
        old_image = grayscale_object.get_data().copy()
        grayscale_object.fit(1)
        self.assertFalse(np.all(old_image == grayscale_object))

    @pytest.mark.gui
    def test_reset(self):
        grayscale_object = grayscale.Grayscale("./files/test_images/lena.png")
        old_image = grayscale_object.get_data().copy()
        grayscale_object.fit(1)
        grayscale_object.reset()
        assert (np.allclose(old_image, grayscale_object.get_data()))


@pytest.mark.gui
def test_noisy_clicker(qtbot):
    ex = grayscale_qt.grayscale_window()
    ex.init_UI()
    ex.show()

    test.general.test_rest(qtbot, ex)
