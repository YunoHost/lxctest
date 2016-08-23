import unittest

from lxctest import log


class TestLog(unittest.TestCase):
    def TestLog(self):
        index, logpath = log.init()
        self.assertIsInstance(index, str)
        self.assertIsInstance(logpath, str)

    def TestDebugLog(self):
        index, logpath = log.init(True)
        self.assertIsInstance(index, str)
        self.assertIsInstance(logpath, str)

if __name__ == '__main__':
    unittest.main()
