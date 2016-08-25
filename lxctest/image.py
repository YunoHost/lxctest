import json
import sys


from . import util
from .log import LOG


class Image:
    def __init__(self, config, index):
        self.store = config['store']
        self.arch = config['arch']
        self.releases = config['releases']
        self.index = index
        self.library = {}

        self.build_image_library()

    def build_image_library(self):
        """
        Given the configruation, build a library (dict) of images.
        """
        LOG.info('Finding images')
        for release in self.releases:
            fingerprint = self.find_lxc_image(self.store, self.arch, release)
            name = ('lxctest-' + release.replace('/', '-') +
                    '-' + self.arch + '-' + self.index)
            self.library[fingerprint] = name

    def find_lxc_image(self, store, arch, release):
        """
        Given a specific LXC store, arch, and release find a matching
        image. Assumes you want 1 image and not many. In fact errors out
        if 0 or many are found.
        """
        cmd = 'lxc image list --format=json %s: %s/%s' % (
              self.store, release, self.arch)
        out, err, rc = util.run(cmd.split())

        try:
            results = json.loads(out)
        except json.decoder.JSONDecodeError:
            LOG.critical('Invalid JSON received for:')
            LOG.critical('%s:%s:%s' % (store, release, arch))
            sys.exit(1)

        if len(results) != 1:
            LOG.critical('Invalid (none or too many) image results for:')
            LOG.critical('%s:%s:%s' % (store, release, arch))
            sys.exit(1)

        LOG.info('%s' % results[0]['properties']['description'])
        return results[0]['fingerprint']
