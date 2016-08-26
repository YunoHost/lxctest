import time
import logging
import os

from . import util


class Container:
    def __init__(self, name, log_dir, debug):
        self.name = name

        self.setup_logging(log_dir, debug)
        self.log = logging.getLogger(name=self.name)

    def _run(self, cmd):
        self.log.info(cmd)
        out, err, return_code = util.run(cmd.split())

        out = out.rstrip()
        err = err.rstrip()

        if out is not "":
            self.log.info('%s' % out.rstrip())

        if return_code != 0:
            self.log.critical('Execution of command failed: %s' % cmd)
            self.log.critical(err.rstrip())

    def return_code(self):
        return all(rc == 0 for rc in self.return_codes)

    def execute(self, command):
        """
        Executes a command on a container.
        """
        self._run('lxc exec %s -- %s' % (self.name, command))

    def config(self, config):
        """
        Sets configuration of a container (e.g. user-data).
        """
        self._run('lxc config set %s %s' % (self.name, config))

    def delete(self):
        """
        Force deletes a container.
        """
        self._run('lxc delete --force %s' % self.name)

    def init(self, store, fingerprint):
        """
        Initializes a specific container.
        """
        self._run('lxc init %s:%s %s' % (store, fingerprint, self.name))

    def pull(self, source, target):
        """
        Pulls a file to a container.
        """
        self._run('lxc file pull %s/%s %s' % (self.name, source, target))

    def push(self, source, target):
        """
        Pushes a file to a container.
        """
        self._run('lxc file push %s %s/%s' % (source, self.name, target))

    def start(self):
        """
        Starts a container
        """
        self._run('lxc start %s' % self.name)
        self._ready()

    def _ready(self, timeout=15):
        """
        Checks that a container is ready for usage.
        """
        for attempt in range(timeout):
            time.sleep(1)
            cmd = 'lxc exec %s -- %s' % (self.name, 'echo 0')
            _, _, return_code = util.run(cmd.split())
            if return_code == 0:
                self.log.debug('Check if started (attempt %s): UP' % attempt)
                return True
            else:
                self.log.debug('Check if started (attempt %s): DOWN' % attempt)

        self.log.info('Failed to start %s' % self.name)
        return False

    def setup_logging(self, log_dir, debug):
        """
        Sets up a logging mechanism for each container's tests
        rather than having everything dump into one.
        """
        level = logging.DEBUG if debug else logging.INFO
        log = logging.getLogger(self.name)

        file_name = os.path.join(log_dir, self.name + '.log')
        file_handler = logging.FileHandler(file_name, 'w')

        file_format = '%(asctime)s - %(message)s'
        formatter = logging.Formatter(file_format)
        file_handler.setFormatter(formatter)

        log.setLevel(level)
        log.addHandler(file_handler)
