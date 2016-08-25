import unittest

from lxctest.image import Image


class TestImage(unittest.TestCase):
    def test_negative_no_valid_images(self):
        index = '40'
        config = {'store': 'images',
                  'releases': ['hpux'],
                  'arch': 'ia64'}

        self.assertRaises(SystemExit, Image, config, index)

    def test_negative_too_many_images(self):
        index = '41'
        config = {'store': 'images',
                  'releases': ['fedora'],
                  'arch': ''}

        self.assertRaises(SystemExit, Image, config, index)

    def test_find_xenial(self):
        index = '42'
        config = {'store': 'ubuntu',
                  'releases': ['xenial'],
                  'arch': 'amd64'}

        self.assertIsInstance(Image(config, index), Image)

if __name__ == '__main__':
    unittest.main()
