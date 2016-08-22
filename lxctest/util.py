from distutils.spawn import find_executable
import os
import subprocess
import sys
import yaml


from .log import LOG


def check_dependencies(dependencies):
    """
    Determines if command exists
    """
    for depend in dependencies:
        if not which(depend):
            LOG.critical('%s: command not found. Please install.' % depend)
            sys.exit(1)


def file_exist(filename):
    """
    Determines if file exists
    """
    return os.path.isfile(filename)


def get_system_arch():
    """
    Determines system package architecture.

    Output differs from arch in that it is more simple and
    does not require translation between one-offs (e.g. 386, 586, 686)
    """
    stdout, _ = run(['dpkg', '--print-architecture'])
    return stdout.rstrip()


def get_ubuntu_release_lts():
    """
    Returns list of current Ubuntu LTS release(s).
    """
    stdout, _ = run(['distro-info', '--lts'])
    return stdout.split()


def get_ubuntu_release_supported():
    """
    Returns list of supported Ubuntu releases.
    """
    stdout, _ = run(['distro-info', '--supported'])
    return stdout.split()


def read_yaml_file(filename):
    """
    Attempts to read and parse a YAML file into a dictionary.
    """
    with open(filename, 'r') as fp:
        try:
            yaml_dict = yaml.safe_load(fp)
        except yaml.parser.ParserError:
            LOG.critical('File is not valid YAML.')
            sys.exit(1)

    return yaml_dict


def run(command):
    """
    Wrapper around subprocess to execute commands.
    """
    LOG.debug('Running command: `%s`' % ' '.join(command))

    try:
        sp = subprocess.Popen(command,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)

        (stdout, stderr) = sp.communicate()
    except OSError as e:
        LOG.critical("Command failed: %s" % command)
        LOG.critical("Error: %s: %s" % (e.errno, e.strerror))
        sys.exit(1)

    return stdout.decode('utf-8'), stderr.decode('utf-8')


def which(command):
    """
    Like the unix 'which' command, but returns boolean.
    """
    return find_executable(command)
