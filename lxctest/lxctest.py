import argparse
import datetime
from distutils.spawn import find_executable
import logging
import os
import sys

from configuration import Configuration
from container import Container
from image import Image


DEPENDENCIES = ['lxd', 'lxc', 'distro-info']


def init():
    check_python_version()
    check_dependencies()
    filename, debug, logdir, save = get_arguments()

    main(filename, debug, logdir, save)


def main(filename, debug=False, logdir=False, save=False):
    index, log_dir = setup_logging('lxctest', debug, logdir)
    config = Configuration(filename)
    images = Image(config.lxc, index)

    # for each image run with config.test
    log = logging.getLogger('lxctest')
    log.info('Building containers and running tests')
    for fingerprint, name in images.library.items():
        run_tests(config.lxc['store'], fingerprint, name,
                  config.test, log_dir, debug, save)


def run_tests(store, fingerprint, name, test, log_dir, debug, save):
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

    if not save:
        c.delete()

    if 'analyze' in test:
        for command in test['analyze']:
            command = command+" "+log_dir
            c._run(command)


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
    parser.add_argument('filename',
                        help='YAML file with test case')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable additional output')
    parser.add_argument('-l', '--logdir',
                        help='optional location to log directory')
    parser.add_argument('-s', '--save', action='store_true',
                        help='save containers, do not delete')
    args = parser.parse_args()

    return args.filename, args.debug, args.logdir, args.save


def setup_logging(name, debug, user_logdir):
    """
    Setup logging to stdout and file.
    """
    LOG = logging.getLogger(name=name)

    # Basic Setup
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(stream=sys.stdout,
                        level=level)

    # Determine Unique Folder Name
    # index like '20160901T133119'
    index = (datetime.datetime.now().isoformat()
             .replace(':', '').replace('-', '').replace('T', '-')
             .split('.')[0])

    if user_logdir:
        log_dir = os.path.join(user_logdir, index)
    else:
        log_dir = os.path.join('logs', index)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # File Stream Handler
    log_file = os.path.join(log_dir, name + '.log')
    fh = logging.FileHandler(log_file, 'w')
    formatter = logging.Formatter('%(asctime)s - %(levelname)8s - %(message)s')
    fh.setFormatter(formatter)
    LOG.addHandler(fh)

    LOG.info('Logging to %s' % log_file)

    return index, log_dir
