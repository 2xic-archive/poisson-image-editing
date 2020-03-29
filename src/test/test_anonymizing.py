import numpy as np
import unittest
from backend import anonymizing
import os

class test_anonymous(unittest.TestCase):
    def test_fit(self):
        path = os.path.dirname(os.path.abspath(__file__))
        anonymous_object = anonymizing.anonymous("./files/test_images/lena.png", False)
        old_image = anonymous_object.get_data().copy()
        anonymous_object.fit(1)
        self.assertFalse(np.all(old_image == anonymous_object))
