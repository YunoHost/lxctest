from . import configuration, log, lxc, util

DEPENDENCIES = ['lxc', 'lxd', 'distro-info']


def main(filename, debug):
    log.init(debug)
    util.check_dependencies(DEPENDENCIES)
    config = configuration.load(filename)
    lxc.run(config)
