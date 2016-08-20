import unittest

from lxctest import configuration


class TestConfiguration(unittest.TestCase):
    def TestFileEnoent(self):
        self.assertRaises(SystemExit, configuration.load,
                          'examples/enoent.yaml')

    def TestMissingKey(self):
        config = {}
        self.assertRaises(SystemExit, configuration.validate_defaults, config)

    def TestMissingLxc(self):
        config = {
            "execute": "date",
        }

        expected = {
            "execute": "date",
            "lxc": {
                "release": ["lts"],
                "store": "release"
            }
        }

        self.assertEqual(expected, configuration.validate_defaults(config))

    def TestMissingRelease(self):
        config = {
            "execute": "date",
            "lxc": {
                "store": "release"
            }
        }
        expected = {
            "execute": "date",
            "lxc": {
                "release": ["lts"],
                "store": "release"
            }
        }

        self.assertEqual(expected, configuration.validate_defaults(config))

    def TestMissingStore(self):
        config = {
            "execute": "date",
            "lxc": {
                "release": "lts"
            }
        }

        expected = {
            "execute": "date",
            "lxc": {
                "release": ["lts"],
                "store": "release"
            }
        }

        self.assertEqual(expected, configuration.validate_defaults(config))

    def TestLxcBadStore(self):
        config = {
            "execute": "date",
            "lxc": {
                "release": ["lts"],
                "store": "xxyzz"
            }
        }

        self.assertRaises(SystemExit, configuration.validate_lxc, config)

    def TestLxcBadRelease(self):
        config = {
            "execute": "date",
            "lxc": {
                "release": ["xxyzz"],
                "store": "release"
            }
        }

        self.assertRaises(SystemExit, configuration.validate_lxc, config)

    def TestLxcUserData(self):
        config = {
            "customize": {
                "user-data": "my_data.txt"
            },
            "lxc": {
                "release": ["lts"],
                "store": "release"
            }
        }

        self.assertRaises(SystemExit, configuration.validate_lxc, config)

    def TestUserDataList(self):
        config = {
            "customize": {
                "user-data": [
                    "file1",
                    "file2"
                ]
            },
            "lxc": {
                "release": "lts",
                "store": "release"
            }
        }

        self.assertRaises(SystemExit, configuration.validate_customize, config)

    def TestUserDataEnoent(self):
        config = {
            "customize": {
                "user-data": "enoent.txt"
            },
            "lxc": {
                "release": ["lts"],
                "store": "release"
            }
        }

        self.assertRaises(SystemExit, configuration.validate_customize, config)

    def TestPushString(self):
        config = {
            "customize": {
                "push": "enoent.sh"
            },
            "lxc": {
                "release": "lts",
                "store": "release"
            }
        }
        self.assertRaises(SystemExit, configuration.validate_customize, config)

    def TestPushEnoent(self):
        config = {
            "customize": {
                "push": [
                    [
                        "enoent.sh",
                        "/usr/bin/"
                    ]
                ]
            },
            "lxc": {
                "release": "lts",
                "store": "release"
            }
        }

        self.assertRaises(SystemExit, configuration.validate_customize, config)

    def TestPositive(self):
        expected = {
            "execute": "date",
            "lxc": {
                "release": ["lts"],
                "store": "release"
            }
        }

        self.assertEqual(expected, configuration.load('examples/basic.yaml'))

if __name__ == '__main__':
    unittest.main()
