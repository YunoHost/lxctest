import argparse
from distutils.spawn import find_executable
import logging
import os
from random import randint
import sys

from .configuration import Configuration
from .container import Container
from .image import Image


DEPENDENCIES = ['lxd', 'lxc', 'distro-info']


def init():
    check_python_version()
    check_dependencies()
    filename, debug = get_arguments()

    main(filename, debug)


def main(filename, debug):
    index, log_dir = setup_logging('lxctest', debug)
    config = Configuration(filename)
    images = Image(config.lxc, index)

    # for each image run with config.test
    log = logging.getLogger('lxctest')
    log.info('Building containers and running tests')
    for fingerprint, name in images.library.items():
        run_tests(config.lxc['store'], fingerprint, name,
                  config.test, log_dir, debug)


def run_tests(store, fingerprint, name, test, log_dir, debug):
    """
    Wrapper function to run a complete test.
    """
    c = Container(name, log_dir, debug)
    c.init(store, fingerprint)

    if 'push' in test:
        for push in test['push']:
            c.push(push[0], push[1])

    if 'user-data' in test:
        with open(test['user-data'], 'r') as user_data_file:
            user_data = user_data_file.read()
        c.config('user.user-data "%s"' % user_data)

    c.start()

    if 'execute' in test:
        for command in test['execute']:
            c.execute(command)

    if 'pull' in test:
        target = os.path.join(log_dir, name)
        if not os.path.exists(target):
            os.makedirs(target)
        for pull in test['pull']:
            c.pull(pull, target)

    c.delete()


def check_python_version():
    """
    Verifies running in Python 3.0 or greater.
    """
    if sys.version_info < (3, 0):
        sys.stdout.write("Requires Python 3 or greater.\n")
        sys.exit(1)


def check_dependencies():
    """
    Verifies all dependencies exist.
    """
    for depend in DEPENDENCIES:
        if not find_executable(depend):
            print('%s: command not found, please install!' % depend)
            sys.exit(1)


def get_arguments():
    """
    Argparse function to collect filename and debug flag.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='YAML file with configuration')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    return args.filename, args.debug


def setup_logging(name, debug):
    """
    Setup logging to stdout and file.
    """
    LOG = logging.getLogger(name=name)
    # Basic Setup
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(stream=sys.stdout,
                        level=level)

    # Determine Unique Folder Name
    log_dir = 'logs'
    index = None
    folder_created = False
    while folder_created is False:
        index = str(randint(1000, 9999))
        if not os.path.exists(os.path.join(log_dir, index)):
            os.makedirs(os.path.join(log_dir, index))
            folder_created = True

    # File Stream Handler
    file_name = os.path.join(log_dir, index, name + '.log')
    fh = logging.FileHandler(file_name, 'w')
    formatter = logging.Formatter('%(asctime)s - %(levelname)8s - %(message)s')
    fh.setFormatter(formatter)
    LOG.addHandler(fh)

    LOG.info('Logging to %s' % file_name)

    return index, os.path.join(log_dir, index)
