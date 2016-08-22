import json
from random import randint
import sys


from . import util
from .log import LOG


class Image:
    def __init__(self, config):
        self.store = config['store']
        self.arch = config['arch']
        self.releases = config['releases']
        self.library = {}

        self.build_image_library()

    def build_image_library(self):
        """
        Given the configruation, build a library (dict) of images.
        """
        LOG.debug('Finding images...')
        suffix = str(randint(1000, 9999))
        for release in self.releases:
            fingerprint = self.find_lxc_image(self.store, self.arch, release)
            name = ('lxctest-' + release.replace('/', '-') +
                    '-' + self.arch + '-' + suffix)
            self.library[fingerprint] = name

        if len(self.library) == 0:
            LOG.critical('No valid images found.')
            sys.exit(1)

    def find_lxc_image(self, store, arch, release):
        """
        Given a specific LXC store, arch, and release find a matching
        image. Assumes you want 1 image and not many. In fact errors out
        if 0 or many are found.
        """
        cmd = 'lxc image list --format=json %s: %s/%s' % (
              self.store, release, self.arch)
        out, _ = util.run(cmd.split())
        results = json.loads(out)

        if len(results) == 0:
            LOG.critical('Found no matching results for:')
            LOG.critical('%s:%s:%s' % (store, release, arch))
            sys.exit(1)
        elif len(results) > 1:
            LOG.critical('Found too many images matching results:')
            for result in results:
                LOG.critical('%s' % result['properties']['description'])
            sys.exit(1)

        LOG.debug('%s' % results[0]['properties']['description'])
        return results[0]['fingerprint']