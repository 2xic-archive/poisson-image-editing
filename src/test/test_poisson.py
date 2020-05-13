import unittest
from engine import poisson

class test_engine(unittest.TestCase):
    def test_setter(self):
        poisson_obj = poisson.Poisson()

        def test_set():
            poisson_obj.mode_boundary = 3

        self.assertRaises(Exception, test_set)

        def test_set_func():
            poisson_obj.set_boundary(3)

        self.assertRaises(Exception, test_set_func)

        assert type(poisson_obj.mode_boundary) == int
        poisson_obj.set_boundary(1)
        poisson_obj.mode_boundary = 0

    def test_setter_getter(self):
        poisson_obj = poisson.Poisson()
        poisson_obj.mode_poisson = 1
        assert (poisson_obj.mode_poisson == 1)

        poisson_obj.mode_poisson = 0
        assert (poisson_obj.mode_poisson == 0)
