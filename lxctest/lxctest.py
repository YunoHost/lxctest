import logging
import os
from random import randint
import sys

from .configuration import Configuration
from .container import Container
from .image import Image


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
        for pull in test['pull']:
            c.pull(pull, log_dir)

    c.delete()


def setup_logging(name, debug):
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
