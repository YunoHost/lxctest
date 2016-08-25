from . import log, util
from .configuration import Configuration
from .container import Container
from .image import Image
from .log import LOG


DEPENDENCIES = ['lxc', 'lxd', 'distro-info']


def main(filename, debug):
    index, log_dir = log.init(debug)
    util.check_dependencies(DEPENDENCIES)
    config = Configuration(filename)
    images = Image(config.lxc, index)

    # for each image run with config.test
    LOG.info('Building containers and running tests')
    for fingerprint, name in images.library.items():
        rc = run_tests(config.lxc['store'], fingerprint, name,
                       config.test, log_dir)

        if rc:
            LOG.info('%s: All tests completed sucessfully' % name)
        else:
            LOG.critical('%s: A test failed, refer to logs' % name)


def run_tests(store, fingerprint, name, test, log_dir):
    c = Container(name)
    c.init(store, fingerprint)

    if 'push' in test:
        for push in test['push']:
            c.push(push[0], push[1])

    if 'user-data' in test:
        c.config('user.user-data - < %s' % test['user-data'])

    c.start()

    if 'execute' in test:
        for command in test['execute']:
            c.execute(command)

    if 'pull' in test:
        for pull in test['pull']:
            c.pull(pull, log_dir)

    c.delete()

    return c.return_code
