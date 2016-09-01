import json
import logging
import sys

from . import util


class Image:
    def __init__(self, config, index):
        self.store = config['store']
        self.arch = config['arch']
        self.releases = config['releases']
        self.index = index
        self.library = {}

        self.log = logging.getLogger('lxctest')

        self.build_image_library()

    def build_image_library(self):
        """
        Given the configruation, build a library (dict) of images.
        """
        self.log.info('Finding images')
        for release in self.releases:
            fingerprint = self.find_lxc_image(self.store, self.arch, release)
            name = ('lxctest-' + self.arch + '-' +
                    release.replace('/', '-') + '-' + self.index)
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

        results = json.loads(out)

        if len(results) != 1:
            self.log.critical(('Image search resulted in %s results. '
                               'Need 1 result.') % len(results))
            self.log.critical('lxc image list --format=json %s:%s:%s' %
                              (store, release, arch))
            sys.exit(1)

        self.log.info('%s' % results[0]['properties']['description'])
        return results[0]['fingerprint']
