#from test import *
import numpy as np
import unittest
from backend import demosaicing
import os

class test_demosaic(unittest.TestCase):
    def test_fit(self):
#        path = os.path.dirname(os.path.abspath(__file__))
        demosaic_object = demosaicing.demosaic("./files/test_images/lena.png", True)
        old_image = demosaic_object.get_data().copy()
#        demosaic_object.fit(1)
#        self.assertFalse(np.all(old_image == demosaic_object))
