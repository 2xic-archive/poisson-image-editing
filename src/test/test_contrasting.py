#from test import *
import numpy as np
import unittest
from backend import contrasting
import os

class test_contrast(unittest.TestCase):
    def test_fit(self):
#        path = os.path.dirname(os.path.abspath(__file__))
        contrast_object = contrasting.contrast("./files/test_images/contrast.jpg", False)
        old_image = contrast_object.get_data().copy()
        contrast_object.fit(1)
        self.assertFalse(np.all(old_image == contrast_object))