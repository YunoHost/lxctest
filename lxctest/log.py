import logging
import sys

PROJECT_NAME = 'lxctest'


def init(debug=False):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(stream=sys.stdout, level=level)

LOG = logging.getLogger(name=PROJECT_NAME)
