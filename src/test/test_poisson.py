import unittest
import numpy as np
#from backend import engine
from engine import poisson

class testDec:#(object):

	@property
	def x(self): 
		return self._x

	@x.setter
	def x(self, value): 
		self._x = value
		
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

	def test_setter_getter(self):
		w = testDec()
		w.x = 10
		assert(w.x == 10)


		x = poisson.poisson()
		x.mode_poisson = 1
		assert(x.mode_poisson == 1)

		x.mode_poisson = 0
		assert(x.mode_poisson == 0)