import unittest

from lxctest import log


class TestLog(unittest.TestCase):
    def test_log(self):
        index, logpath = log.init()
        self.assertIsInstance(index, str)
        self.assertIsInstance(logpath, str)

    def test_debug_log(self):
        index, logpath = log.init(True)
        self.assertIsInstance(index, str)
        self.assertIsInstance(logpath, str)

if __name__ == '__main__':
    unittest.main()
