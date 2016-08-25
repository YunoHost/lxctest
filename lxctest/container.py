import time


from . import util
from .log import LOG


class Container:
    def __init__(self, name):
        self.name = name
        self.return_codes = []

    def execute(self, command):
        """
        Runs a command on a container.
        """
        cmd = 'lxc exec %s -- %s' % (self.name, command)
        out, err, return_code = util.run(cmd.split())

        if return_code != 0:
            LOG.critical('Execution of command failed: %s' % command)
            LOG.critical(err.rstrip())

        LOG.debug(out.rstrip())

        self.return_codes.append(return_code)

    def config(self, config):
        """
        Sets configuration of a container (e.g. user-data).
        """
        cmd = 'lxc config set %s %s' % (self.name, config)
        _, _, return_code = util.run(cmd.split())

        self.return_codes.append(return_code)

    def delete(self):
        """
        Force deletes a container.
        """
        cmd = 'lxc delete --force %s' % self.name
        _, _, return_code = util.run(cmd.split())

        self.return_codes.append(return_code)

    def init(self, store, fingerprint):
        """
        Initializes a specific container.
        """
        cmd = 'lxc init %s:%s %s' % (store, fingerprint, self.name)
        out, err, return_code = util.run(cmd.split())

        if return_code != 0:
            LOG.critical('Could not init %s' % self.name)
            LOG.critical(err.rstrip())

        LOG.debug(out.rstrip())

        self.return_codes.append(return_code)

    def pull(self, source, target):
        """
        Pulls a file to a container.
        """
        cmd = 'lxc file pull %s/%s %s' % (self.name, source, target)
        _, _, return_code = util.run(cmd.split())

        self.return_codes.append(return_code)

    def push(self, source, target):
        """
        Pushes a file to a container.
        """
        cmd = 'lxc file push %s %s/%s' % (source, self.name, target)
        _, _, return_code = util.run(cmd.split())

        self.return_codes.append(return_code)

    def return_code(self):
        return all(rc == 0 for rc in self.return_codes)

    def start(self, timeout=15):
        """
        Starts a container
        """
        cmd = 'lxc start %s' % self.name
        _, _, return_code = util.run(cmd.split())

        if return_code != 0:
            LOG.critical('Could not start %s' % self.name)

        for attempt in range(timeout):
            time.sleep(1)
            cmd = 'lxc exec %s -- %s' % (self.name, 'echo 0')
            _, _, return_code = util.run(cmd.split())
            if return_code == 0:
                self.return_codes.append(0)
                LOG.debug('Successfully started %s' % self.name)
                break
