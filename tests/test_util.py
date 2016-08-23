import unittest

from lxctest import util


class TestUtil(unittest.TestCase):
    def TestBadDependency(self):
        self.assertRaises(SystemExit, util.check_dependencies, 'xyzzy')

    def TestBadCommand(self):
        self.assertRaises(SystemExit, util.run, 'xyzzy')

    def TestBadYaml(self):
        self.assertRaises(SystemExit, util.read_yaml_file,
                          'examples/tests/negative/invalid.yaml')

if __name__ == '__main__':
    unittest.main()
