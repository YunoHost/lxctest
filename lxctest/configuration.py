import logging
import os
import sys
import yaml

import util


CONFIG_KEYS_REQUIRED = ['push', 'user-data', 'execute', 'pull']
LXC_STORES = ['images', 'ubuntu', 'ubuntu-daily']
LXC_STORES_DEFAULT = 'images'
LXC_STORES_CLOUD = ['ubuntu', 'ubuntu-daily']
LXC_RELEASE_DEFAULT = ['lts']


class Configuration:
    def __init__(self, filename):
        self.test = {}
        self.lxc = {}

        self.log = logging.getLogger('lxctest')
        self.log.info('Loading configuration from file')
        self.load_file(filename)

        self.log.debug('Starting configuration validation')
        self.validate_required_fields()
        self.setup_lxc_stanza()
        self.setup_lxc_releases()
        self.validate_cloud_image()
        self.validate_execute()
        self.validate_lxc_store()
        self.validate_pull()
        self.validate_push()
        self.validate_user_data()

        self.log.info('Test configuration:')
        self.log.info(self.test)
        self.log.info('LXC configuration:')
        self.log.info(self.lxc)

    def load_file(self, filename):
        """
        Reads the given YAML filename containing configuration and returns
        the file as a dictionary.
        """
        self.log.debug('Reading file: %s' % filename)

        if not self.file_exist(filename):
            self.log.critical('Given configuration filename does not exist')
            sys.exit(1)

        config = self.read_yaml_file(filename)
        if config is None:
            self.log.critical('Config is invalid yaml or empty')
            sys.exit(1)

        self.log.debug('Configuration from file: %s' % config)

        # seperate LXC specific stuff
        if 'lxc' in config:
            self.lxc = config['lxc']
            del config['lxc']

        self.test = config

    def setup_lxc_releases(self):
        """
        Converts the LXC release wildcards to actual release names.
        """
        releases = []
        for release in self.lxc['releases']:
            if release == 'lts':
                releases = releases + self.get_ubuntu_release_lts()
            elif release == 'supported':
                releases = releases + self.get_ubuntu_release_supported()
            else:
                releases.append(release)

        self.lxc['releases'] = list(set(releases))

    def setup_lxc_stanza(self):
        """
        Validates that the LXC stanza exists and if not inputs the default
        values for each field. Files in arch field based on system
        information.

        Also changes the LXC release field to a list if it is not already.
        """
        if 'store' not in self.lxc:
            self.lxc['store'] = LXC_STORES_DEFAULT
        if 'releases' not in self.lxc:
            self.lxc['releases'] = LXC_RELEASE_DEFAULT

        self.lxc['arch'] = self.get_system_arch()

        # Convert release to list to be consistent from here on out
        # Avoids needing to check for string or list everywhere
        if isinstance(self.lxc['releases'], str):
            releases = self.lxc['releases'].split()
            self.lxc['releases'] = releases

    def validate_cloud_image(self):
        """
        Validates that if user-data was passed in then a cloud store is used.
        """
        if 'user-data' in self.test:
            if self.lxc['store'] not in set(LXC_STORES_CLOUD):
                self.log.critical('You specified user-data, but not a ' +
                                  'cloud store, choose from:')
                self.log.critical(LXC_STORES_CLOUD)
                sys.exit(1)

    def validate_execute(self):
        """
        Validates that execute is a list and not a string.
        """
        if 'execute' in self.test:
            if type(self.test['execute']) != list:
                self.log.critical('Execute must be a list of commands')
                sys.exit(1)

    def validate_lxc_store(self):
        """
        Validates the LXC store option is from one of the valid options.
        """
        if type(self.lxc['store']) != str:
            self.log.critical('LXC store must be a string not a list')
            sys.exit(1)

        if self.lxc['store'] not in set(LXC_STORES):
            self.log.critical('LXC store is not a valid option')
            self.log.critical('Choose from:')
            self.log.critical(LXC_STORES)
            sys.exit(1)

    def validate_pull(self):
        """
        Validates that the pull file list is a list.
        """
        if 'pull' in self.test:
            if type(self.test['pull']) != list:
                self.log.critical('Pull files must be a list')
                sys.exit(1)

    def validate_push(self):
        """
        Validates that the push file list is a list and the files
        exist.
        """
        if 'push' in self.test:
            push_list = self.test['push']
            if type(push_list) != list:
                self.log.critical('Push files must be a list')
                sys.exit(1)

            for item in push_list:
                if not self.file_exist(item[0]):
                    self.log.critical('Push file (%s) does not exist' %
                                      item[0])
                    sys.exit(1)

    def validate_required_fields(self):
        """
        Validates that at least one of the required fields exist in the
        config.
        """
        if set(CONFIG_KEYS_REQUIRED).isdisjoint(self.test):
            self.log.critical('Missing at least one required value')
            self.log.critical('Choose from:')
            self.log.critical(CONFIG_KEYS_REQUIRED)
            sys.exit(1)

    def validate_user_data(self):
        """
        Validates that there exists one user-data file and that it exists.
        """
        if 'user-data' in self.test:
            user_data = self.test['user-data']
            if type(user_data) != str:
                self.log.critical('User-data must be a string not a list')
                sys.exit(1)

            if not self.file_exist(user_data):
                import os
                print(os.path)
                print(user_data)
                self.log.critical('User-data file (%s) does not exist' %
                                  user_data)
                sys.exit(1)

    @staticmethod
    def file_exist(filename):
        """
        Determines if file exists
        """
        if not filename:
            return False

        return os.path.isfile(filename)

    @staticmethod
    def get_system_arch():
        """
        Determines system package architecture.

        Output differs from arch in that it is more simple and
        does not require translation between one-offs (e.g. 386, 586, 686)
        """
        stdout, _, _ = util.run(['dpkg', '--print-architecture'])
        return stdout.rstrip()

    @staticmethod
    def get_ubuntu_release_lts():
        """
        Returns list of current Ubuntu LTS release(s).
        """
        stdout, _, _ = util.run(['distro-info', '--lts'])
        return stdout.split()

    @staticmethod
    def get_ubuntu_release_supported():
        """
        Returns list of supported Ubuntu releases.
        """
        stdout, _, _ = util.run(['distro-info', '--supported'])
        return stdout.split()

    @staticmethod
    def read_yaml_file(filename):
        """
        Attempts to read and parse a YAML file into a dictionary.
        """
        with open(filename, 'r') as fp:
            try:
                yaml_dict = yaml.safe_load(fp)
            except yaml.parser.ParserError:
                return None

        return yaml_dict
