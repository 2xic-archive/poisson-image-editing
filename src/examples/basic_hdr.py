"""
Need to make it possible to add HDR support
"""
import sys
sys.path.append('./')

import unittest
import numpy as np
import scipy.io
from engine import hdr_image_handler
from backend import hdr_reconstruction


from backend import inpaiting

x = hdr_reconstruction.hdr_reconstruction()
x.fit()
x.show()

