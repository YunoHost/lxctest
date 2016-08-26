import argparse
from distutils.spawn import find_executable
import sys

from .lxctest import main


DEPENDENCIES = ['lxc', 'lxd', 'distro-info']

if __name__ == '__main__':
    for depend in DEPENDENCIES:
        if not find_executable(depend):
            print('%s: command not found, please install!' % depend)
            sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='YAML file with configuration')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    main(args.filename, args.debug)
