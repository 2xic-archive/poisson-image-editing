import os
import sys
import numpy as np

PATH = os.path.dirname(os.path.abspath(__file__)) 
PATH += "/" if not PATH.endswith("/") else ""

print(PATH)
sys.path.append(PATH + "../")

import unittest
import blurring

class test_blur(unittest.TestCase):
    def test_fit(self):
        path = os.path.dirname(os.path.abspath(__file__))
        blur_object = blurring.blur(PATH + "../test_images/lena.png", False)
        old_image = blur_object.get_data().copy()
        blur_object.fit(1)
        self.assertFalse(np.all(old_image == blur_object))

