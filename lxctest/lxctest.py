from . import log, util
from .configuration import Configuration
from .image import Image
from .container import Container


DEPENDENCIES = ['lxc', 'lxd', 'distro-info']


def main(filename, debug):
    log.init(debug)
    util.check_dependencies(DEPENDENCIES)
    config = Configuration(filename)
    images = Image(config.lxc)

    # for each image run with config.test
    for fingerprint, name in images.library.items():
        run_tests(config.lxc['store'], fingerprint, name, config.test)


def run_tests(store, fingerprint, name, test):
    print('%s %s %s %s' % (store, fingerprint, name, test))
    c = Container(name)

    # init
    c.init(store, fingerprint)

    # push
    for push in test['push']:
        c.push(push[0], push[1])

    # config
    config = 'user.user-data - < %s' % test['user-data']
    c.config(config)

    # start
    c.start()

    # execute
    for command in test['execute']:
        c.execute(command)

    # pull
    for pull in test['pull']:
        c.pull(pull[0], pull[1])

    # destory
    c.delete()
