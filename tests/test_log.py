import unittest

from lxctest import log


class TestLog(unittest.TestCase):
    def TestLog(self):
        self.assertEqual(None, log.init())

    def TestDebugLog(self):
        self.assertEqual(None, log.init(True))


if __name__ == '__main__':
    unittest.main()
