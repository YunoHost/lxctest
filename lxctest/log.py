from random import randint


import logging
import os
import sys


APPNAME = 'lxctest'
LOG = logging.getLogger(name=APPNAME)


def init(debug=False):
    """
    Initializes logging to stdout and a file with the INFO level.
    """
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(stream=sys.stdout, level=level)

    # create unique folder name
    log_dir = 'logs'

    index = None
    folder_created = False
    while folder_created is False:
        index = str(randint(1000, 9999))
        if not os.path.exists(os.path.join(log_dir, index)):
            os.makedirs(os.path.join(log_dir, index))
            folder_created = True

    file_name = os.path.join(log_dir, index, APPNAME + '.log')
    file_handler = logging.FileHandler(file_name, 'w')
    file_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(file_format)
    file_handler.setFormatter(formatter)
    LOG.addHandler(file_handler)

    LOG.info('Logging to %s' % file_name)

    return index, os.path.join(log_dir, index)
