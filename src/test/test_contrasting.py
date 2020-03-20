from test import *
import numpy as np
import unittest
import contrasting

class test_contrast(unittest.TestCase):
    def test_fit(self):
        path = os.path.dirname(os.path.abspath(__file__))
        contrast_object = contrasting.contrast(PATH + "../files/test_images/contrast.jpg", False)
        old_image = contrast_object.get_data().copy()
        contrast_object.fit(1)
        self.assertFalse(np.all(old_image == contrast_object))