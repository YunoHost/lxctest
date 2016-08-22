import logging
import sys


LOG = logging.getLogger(name='lxctest')


def init(debug=False):
    """
    Initializes logging to stdout and INFO level.
    """
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(stream=sys.stdout, level=level)
