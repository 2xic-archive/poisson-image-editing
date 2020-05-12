import unittest

import numpy as np
import scipy.io

from engine import hdr_image_handler
from engine import image_handler


class test_hdr_image_handler(unittest.TestCase):
    def test_matlab(self):
        hdr = hdr_image_handler.hdr_handler([
            image_handler.ImageHandler('../hdr-bilder/Adjuster/Adjuster_00064.png'),
            image_handler.ImageHandler('../hdr-bilder/Adjuster/Adjuster_00128.png'),
            image_handler.ImageHandler('../hdr-bilder/Adjuster/Adjuster_00256.png'),
            image_handler.ImageHandler('../hdr-bilder/Adjuster/Adjuster_00512.png')
        ])
        matlab_z = scipy.io.loadmat("./test/test_files/Z.mat")["Z"]

        matlab_a = scipy.io.loadmat("./test/test_files/matlab_a 1.mat")["A"]
        matlab_b = scipy.io.loadmat("./test/test_files/matlab_b 1.mat")["b"]

        A, b, n = hdr.get_Ab(matlab_z[:, :, 0])

        np.allclose(A, matlab_a)
        np.allclose(b, matlab_b)
