#!/usr/bin/env python
import argparse

from . import configuration, log, lxc, util

DEPENDENCIES = ['lxc', 'lxd', 'distro-info']


def main(filename, debug=False):
    log.init(debug)
    util.check_dependencies(DEPENDENCIES)
    config = configuration.load(filename)
    # TODO
    # print out the config here

    lxc.run(config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='YAML file with configuration')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    main(args.filename, args.debug)
