import sys

from . import util
from .log import LOG

CONFIG_KEYS_REQUIRED = ['customize', 'execute', 'collect']
LXC_STORES = ['release', 'cloud', 'cloud-daily']
LXC_STORES_DEFAULT = 'release'
LXC_STORES_CLOUD = ['cloud', 'cloud-daily']
LXC_RELEASE = ['lts', 'supported']
LXC_RELEASE_DEFAULT = 'lts'
LOG_PREFIX = '[Configuration] '


def load(filename):
    LOG.info('Starting configuration validation...')
    LOG.debug('Reading file: %s' % filename)

    if not util.file_exist(filename):
        LOG.critical('Given filename does not exist.')
        sys.exit(1)

    config = validate_defaults(util.read_yaml_file(filename))
    validate_customize(config)
    config = validate_lxc(config)

    LOG.info('Configuration validation complete!')
    LOG.debug('Configuration after validation: %s' % config)
    return config


def validate_defaults(config):
    LOG.debug('Configuration from file: %s' % config)
    if config is None or set(CONFIG_KEYS_REQUIRED).isdisjoint(config):
        LOG.critical('Missing at least one required YAML value. Choose from:')
        LOG.critical(CONFIG_KEYS_REQUIRED)
        sys.exit(1)

    if 'lxc' in config:
        if 'store' not in config['lxc']:
            config['lxc']['store'] = LXC_STORES_DEFAULT
        if 'release' not in config['lxc']:
            config['lxc']['release'] = LXC_RELEASE_DEFAULT
    else:
        config['lxc'] = {}
        config['lxc']['store'] = LXC_STORES_DEFAULT
        config['lxc']['release'] = LXC_RELEASE_DEFAULT

    # Convert release to list to be consistent from here on out
    # Avoids needing to check for string or list everywhere
    if isinstance(config['lxc']['release'], str):
        config['lxc']['release'] = config['lxc']['release'].split()

    return config


def validate_lxc(config):
    if config['lxc']['store'] not in set(LXC_STORES):
        LOG.critical('LXC store is not a valid option. Choose from:')
        LOG.critical(LXC_STORES)
        sys.exit(1)

    releases = []
    for release in config['lxc']['release']:
        if release == 'lts':
            releases = releases + util.get_ubuntu_release_lts()
        elif release == 'supported':
            releases = releases + util.get_ubuntu_release_supported()
        else:
            releases.append(release)

    config['lxc']['release'] = list(set(releases))

    if 'customize' in config and 'user-data' in config['customize']:
        if config['lxc']['store'] not in set(LXC_STORES_CLOUD):
            LOG.critical('You specified user-data, but not a cloud store.'
                         ' Choose from:')
            LOG.critical(LXC_STORES_CLOUD)
            sys.exit(1)

    return config


def validate_customize(config):
    if 'customize' in config:
        if 'user-data' in config['customize']:
            user_data = config['customize']['user-data']
            if type(user_data) != str:
                LOG.critical('User-data must be a string not a list.')
                sys.exit(1)

            if not util.file_exist(user_data):
                LOG.critical('User-data file (%s) does not exist.' % user_data)
                sys.exit(1)
        if 'push' in config['customize']:
            push_list = config['customize']['push']
            if type(push_list) != list:
                LOG.critical('Push files must be a list.')
                sys.exit(1)

            for item in push_list:
                if not util.file_exist(item[0]):
                    LOG.critical('Push file (%s) does not exist.' % item[0])
                    sys.exit(1)
