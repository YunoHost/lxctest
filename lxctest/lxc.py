import json
from random import randint
import sys


from .log import LOG
from . import util


STORE_DICT = {
    'release': 'images',
    'cloud': 'ubuntu',
    'cloud-daily': 'ubuntu-daily'
}


def run(config):
    store = STORE_DICT[config['lxc']['store']]
    arch = util.get_system_arch()
    LOG.debug('Using host architechture: [%s]' % arch)

    LOG.info('Finding images...')
    images = images_find(store, config['lxc']['release'], arch)

    LOG.info('Deploying images...')
    images_deploy(store, images)

    LOG.info('Destorying images...')
    images_delete(images)


def images_delete(images):
    for name in images:
        cmd = 'lxc delete --force %s' % name
        util.run(cmd.split())


def images_deploy(store, images):
    for name, fingerprint in images.items():
        cmd = 'lxc init %s:%s %s' % (store, fingerprint, name)
        out, err = util.run(cmd.split())

        LOG.info(out)
        LOG.info(err)


def images_find(store, releases, arch):
    images = {}
    name_prefix = 'lxctest-' + str(randint(1000, 9999)) + '-'
    for release in releases:
        cmd = 'lxc image list --format=json %s: %s/%s' % (store, release, arch)

        out, _ = util.run(cmd.split())
        results = json.loads(out)

        if len(results) == 0:
            LOG.critical('Found no matching results for:')
            LOG.critical('%s:%s:%s' % (store, release, arch))
        elif len(results) > 1:
            LOG.critical('Found too many images matching results:')
            for result in results:
                LOG.critical('%s' % result['properties']['description'])
        else:
            LOG.debug('%s' % results[0]['properties']['description'])
            name = name_prefix + release.replace('/', '-') + '-' + arch
            images[name] = results[0]['fingerprint']

    if len(images) == 0:
        LOG.critical('No valid images found.')
        sys.exit(1)

    return images
