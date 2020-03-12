import os
import sys
import numpy as np

PATH = os.path.dirname(os.path.abspath(__file__)) 
PATH += "/" if not PATH.endswith("/") else ""

print(PATH)
sys.path.append(PATH + "../")

import unittest
import contrasting

class test_contrast(unittest.TestCase):
    def test_fit(self):
        path = os.path.dirname(os.path.abspath(__file__))
        x = contrasting.contrast(PATH + "../test_images/contrast.jpg", False)
        old = x.data.copy()
        x.fit(1)
        self.assertFalse(np.all(old == x.data))