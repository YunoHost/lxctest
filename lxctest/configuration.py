import sys

from . import util
from .log import LOG


CONFIG_KEYS_REQUIRED = ['push', 'user-data', 'execute', 'pull']
LXC_STORES = ['images', 'ubuntu', 'ubuntu-daily']
LXC_STORES_DEFAULT = 'images'
LXC_STORES_CLOUD = ['ubuntu', 'ubuntu-daily']
LXC_RELEASE_DEFAULT = ['lts']


class Configuration:
    def __init__(self, filename):
        self.test = {}
        self.lxc = {}

        LOG.info('Loading configuration from file')
        self.load_file(filename)

        LOG.debug('Starting configuration validation')
        self.validate_required_fields()
        self.setup_lxc_stanza()
        self.setup_lxc_releases()
        self.validate_cloud_image()
        self.validate_execute()
        self.validate_lxc_store()
        self.validate_pull()
        self.validate_push()
        self.validate_user_data()

        LOG.info('Test configuration:')
        LOG.info(self.test)
        LOG.info('LXC configuration:')
        LOG.info(self.lxc)

    def load_file(self, filename):
        """
        Reads the given YAML filename containing configuration and returns
        the file as a dictionary.
        """
        LOG.debug('Reading file: %s' % filename)

        if not util.file_exist(filename):
            LOG.critical('Given configuration filename does not exist')
            sys.exit(1)

        config = util.read_yaml_file(filename)
        if config is None:
            LOG.critical('Config is empty, need at least one required value')
            LOG.critical('Choose from:')
            LOG.critical(CONFIG_KEYS_REQUIRED)
            sys.exit(1)

        LOG.debug('Configuration from file: %s' % config)

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
                releases = releases + util.get_ubuntu_release_lts()
            elif release == 'supported':
                releases = releases + util.get_ubuntu_release_supported()
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

        self.lxc['arch'] = util.get_system_arch()

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
                LOG.critical('You specified user-data, but not a cloud store'
                             ' Choose from:')
                LOG.critical(LXC_STORES_CLOUD)
                sys.exit(1)

    def validate_execute(self):
        """
        Validates that execute is a list and not a string.
        """
        if 'execute' in self.test:
            if type(self.test['execute']) != list:
                LOG.critical('Execute must be a list of commands')
                sys.exit(1)

    def validate_lxc_store(self):
        """
        Validates the LXC store option is from one of the valid options.
        """
        if type(self.lxc['store']) != str:
            LOG.critical('LXC store must be a string not a list')
            sys.exit(1)

        if self.lxc['store'] not in set(LXC_STORES):
            LOG.critical('LXC store is not a valid option')
            LOG.critical('Choose from:')
            LOG.critical(LXC_STORES)
            sys.exit(1)

    def validate_pull(self):
        """
        Validates that the pull file list is a list.
        """
        if 'pull' in self.test:
            if type(self.test['pull']) != list:
                LOG.critical('Pull files must be a list')
                sys.exit(1)

    def validate_push(self):
        """
        Validates that the push file list is a list and the files
        exist.
        """
        if 'push' in self.test:
            push_list = self.test['push']
            if type(push_list) != list:
                LOG.critical('Push files must be a list')
                sys.exit(1)

            for item in push_list:
                if not util.file_exist(item[0]):
                    LOG.critical('Push file (%s) does not exist' %
                                 item[0])
                    sys.exit(1)

    def validate_required_fields(self):
        """
        Validates that at least one of the required fields exist in the
        config.
        """
        if set(CONFIG_KEYS_REQUIRED).isdisjoint(self.test):
            LOG.critical('Missing at least one required value')
            LOG.critical('Choose from:')
            LOG.critical(CONFIG_KEYS_REQUIRED)
            sys.exit(1)

    def validate_user_data(self):
        """
        Validates that there exists one user-data file and that it exists.
        """
        if 'user-data' in self.test:
            user_data = self.test['user-data']
            if type(user_data) != str:
                LOG.critical('User-data must be a string not a list')
                sys.exit(1)

            if not util.file_exist(user_data):
                import os
                print(os.path)
                print(user_data)
                LOG.critical('User-data file (%s) does not exist' %
                             user_data)
                sys.exit(1)
