import os
import platform
import subprocess
import sys
import yaml

from distutils.spawn import find_executable

from .log import LOG


def check_dependencies(dependencies):
    for depend in dependencies:
        if not which(depend):
            LOG.critical('%s: command not found. Please install.' % depend)
            sys.exit(1)


def file_exist(filename):
    return os.path.isfile(filename)


def get_system_arch():
    return hw_to_arch(platform.machine())


def get_ubuntu_release_lts():
    stdout, _ = run(['distro-info', '--lts'])
    return stdout.split()


def get_ubuntu_release_supported():
    stdout, _ = run(['distro-info', '--supported'])
    return stdout.split()


def hw_to_arch(arch):
    hw_to_arch = {
        'i586': 'i386',
        'i686': 'i386',
        'x86_64': 'amd64',
        'ppc64le': 'ppc64el',
        'aarch64': 'arm64',
    }
    return hw_to_arch.get(arch, arch)


def read_yaml_file(filename):
    with open(filename, 'r') as fp:
        try:
            yaml_dict = yaml.safe_load(fp)
        except yaml.parser.ParserError:
            LOG.critical('File is not valid YAML.')
            sys.exit(1)

    return yaml_dict


def run(command):
    LOG.debug(' '.join(command))

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
    return find_executable(command)
