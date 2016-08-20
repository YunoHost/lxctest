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


def get_platform_arch():
    platform2arch = {
        'i586': 'i386',
        'i686': 'i386',
        'x86_64': 'amd64',
        'ppc64le': 'ppc64el',
        'aarch64': 'arm64',
    }

    return platform2arch.get(platform.machine(), platform.machine())


def get_ubuntu_releases():
    stdout, _ = run(['distro-info', '--all'])
    return set(stdout.split())


def read_yaml_file(filename):
    with open(filename, 'r') as fp:
        try:
            yaml_dict = yaml.safe_load(fp)
        except yaml.parser.ParserError:
            LOG.critical('File is not valid YAML.')
            sys.exit(1)

    return yaml_dict


def run(command):
    try:
        sp = subprocess.Popen(command,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)

        (stdout, stderr) = sp.communicate()
    except OSError:
        LOG.debug("Command %s failed" % command)
        sys.exit(1)

    return stdout, stderr


def which(command):
    return find_executable(command)
