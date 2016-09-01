import unittest

from lxctest.configuration import Configuration


class TestConfiguration(unittest.TestCase):
    def test_execute(self):
        yaml = 'examples/tests/execute.yaml'
        self.assertIsInstance(Configuration(yaml),
                              Configuration)

    def test_lxc_empty(self):
        yaml = 'examples/tests/lxc_empty.yaml'
        self.assertIsInstance(Configuration(yaml),
                              Configuration)

    def test_lxc_lts(self):
        yaml = 'examples/tests/lxc_lts.yaml'
        self.assertIsInstance(Configuration(yaml),
                              Configuration)

    def test_lxc_release_fedora(self):
        yaml = 'examples/tests/lxc_release_fedora.yaml'
        self.assertIsInstance(Configuration(yaml),
                              Configuration)

    def test_lxc_store_daily(self):
        yaml = 'examples/tests/lxc_store_daily.yaml'
        self.assertIsInstance(Configuration(yaml),
                              Configuration)

    def test_lxc_store_images(self):
        yaml = 'examples/tests/lxc_store_images.yaml'
        self.assertIsInstance(Configuration(yaml),
                              Configuration)

    def test_lxc_store_ubuntu(self):
        yaml = 'examples/tests/lxc_store_ubuntu.yaml'
        self.assertIsInstance(Configuration(yaml),
                              Configuration)

    def test_lxc_supported(self):
        yaml = 'examples/tests/lxc_supported.yaml'
        self.assertIsInstance(Configuration(yaml),
                              Configuration)

    def test_negative_empty_yaml(self):
        self.assertRaises(SystemExit,
                          Configuration,
                          'examples/tests/negative/empty.yaml')

    def test_negative_empty_required(self):
        self.assertRaises(SystemExit,
                          Configuration,
                          'examples/tests/negative/empty_required.yaml')

    def test_negative_enoent(self):
        self.assertRaises(SystemExit,
                          Configuration,
                          'enoent.yaml')

    def test_negative_execute_string(self):
        self.assertRaises(SystemExit,
                          Configuration,
                          'examples/tests/negative/execute_string.yaml')

    def test_negative_filename(self):
        self.assertFalse(Configuration.file_exist(None))

    def test_negative_invalid(self):
        self.assertRaises(SystemExit,
                          Configuration,
                          'examples/tests/negative/invalid.yaml')

    def test_negative_lxc_store_invalid(self):
        self.assertRaises(SystemExit,
                          Configuration,
                          'examples/tests/negative/lxc_store_invalid.yaml')

    def test_negative_lxc_store_list(self):
        self.assertRaises(SystemExit,
                          Configuration,
                          'examples/tests/negative/lxc_store_list.yaml')

    def test_negative_pull_string(self):
        self.assertRaises(SystemExit,
                          Configuration,
                          'examples/tests/negative/pull_string.yaml')

    def test_negative_push_enoent(self):
        self.assertRaises(SystemExit,
                          Configuration,
                          'examples/tests/negative/push_enoent.yaml')

    def test_negative_push_string(self):
        self.assertRaises(SystemExit,
                          Configuration,
                          'examples/tests/negative/push_string.yaml')

    def test_negative_user_data_enoent(self):
        self.assertRaises(SystemExit,
                          Configuration,
                          'examples/tests/negative/user_data_enoent.yaml')

    def test_negative_user_data_images(self):
        self.assertRaises(SystemExit,
                          Configuration,
                          'examples/tests/negative/user_data_images.yaml')

    def test_negative_user_data_list(self):
        self.assertRaises(SystemExit,
                          Configuration,
                          'examples/tests/negative/user_data_list.yaml')

    def test_pull(self):
        yaml = 'examples/tests/pull.yaml'
        self.assertIsInstance(Configuration(yaml),
                              Configuration)

    def test_push(self):
        yaml = 'examples/tests/push.yaml'
        self.assertIsInstance(Configuration(yaml),
                              Configuration)

    def test_user_data(self):
        yaml = 'examples/tests/user_data.yaml'
        self.assertIsInstance(Configuration(yaml),
                              Configuration)

if __name__ == '__main__':
    unittest.main()
