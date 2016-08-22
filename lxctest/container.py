from . import util


class Container:
    def __init__(self, name):
        self.name = name

    def execute(self, command):
        """
        Runs a command on a container.
        """
        cmd = 'lxc exec %s -- %s' % (self.name, command)
        util.run(cmd.split())

    def config(self, config):
        """
        Sets configuration of a container (e.g. user-data).
        """
        cmd = 'lxc config set %s %s' % (self.name, config)
        util.run(cmd.split())

    def delete(self):
        """
        Force deletes a container.
        """
        cmd = 'lxc delete --force %s' % self.name
        util.run(cmd.split())

    def init(self, store, fingerprint):
        """
        Initializes a specific container.
        """
        cmd = 'lxc init %s:%s %s' % (store, fingerprint, self.name)
        util.run(cmd.split())

    def pull(self, source, target):
        """
        Pulls a file to a container.
        """
        cmd = 'lxc file pull %s/%s %s' % (self.name, source, target)
        util.run(cmd.split())

    def push(self, source, target):
        """
        Pushes a file to a container.
        """
        cmd = 'lxc file push %s %s/%s' % (source, self.name, target)
        util.run(cmd.split())

    def start(self):
        """
        Starts a container
        """
        cmd = 'lxc start %s' % self.name
        util.run(cmd.split())
