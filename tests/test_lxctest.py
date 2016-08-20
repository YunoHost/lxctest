import unittest

from lxctest import lxctest


class TestLxctest(unittest.TestCase):
    def TestHappyPath(self):
        lxctest.main('examples/basic.yaml')
        assert True
