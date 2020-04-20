import unittest
import numpy as np
#from backend import engine
from engine import poisson

class test_engine(unittest.TestCase):
	def test_setter(self):
		x = poisson.poisson()
		def test_set():
			x.mode_boundary = 3
		self.assertRaises(Exception, test_set)

		def test_set_func():
			x.set_boundary(3)
		self.assertRaises(Exception, test_set_func)

		assert type(x.mode_boundary) == int
		x.set_boundary(1)
		x.mode_boundary = 0