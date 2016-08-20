import logging

PROJECT_NAME = 'lxctest'


def init(debug=False):
    if debug:
        logging.basicConfig(level=logging.debug)
    else:
        logging.basicConfig()


LOG = logging.getLogger(name=PROJECT_NAME)
