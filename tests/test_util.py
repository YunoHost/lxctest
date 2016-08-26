import unittest

from lxctest import util


class TestUtil(unittest.TestCase):
    def test_invalid_command(self):
        stdout, stderr, rc = util.run('xyzzy')
        self.assertEqual(2, rc)

if __name__ == '__main__':
    unittest.main()
