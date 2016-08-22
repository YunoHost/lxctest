# LXC Test (lxctest)

## Overview

LXC Test provides a wrapper around LXC to automate test execution, while leaving the test creation and analysis to the user. It uses LXC to launch Ubuntu containers with specific customizations, run a series of commands, and items to gather as output all set by the user. By using LXC the user has a much faster way of running tests compared to VMs.

## YAML Format

A single YAML test case file is used to define the following items for each test:

- Image Specification
- Image Customization
- Command Execution
- File Collection

The syntax for each of the above is defined below.

### Image Specification

The image specification defines what LXC image will be used for the test. This includes the store and release. If no options are received, then by default the release LTS image will be used. Specifically:

```
lxc:
  store: release
  release: lts
```

#### Store

Defines which store of Ubuntu images to use. Two options:

- release: standard images, see `lxc image list images:` for a full list. This is the default option.
- cloud: Images containing cloud-init, see `lxc image list ubuntu:` for a full list.
- cloud-daily: Daily images containing cloud-init, see `lxc image list ubuntu-daily:` for a full list.

```
lxc:
  store: release  # Default
  store: cloud
  store: cloud-daily
```

#### Release

Defines the targeted releases from the following options:

- lts: Use the current Ubuntu LTS, see `ubuntu-distro-info --lts`. This is the default option.
- supported: Run across all supported Ubuntu versions, see `ubuntu-distro-info --supported`.
- Specify a specific collection of releases. If one of the releases does not exist then no tests will run.

```
lxc:
  release: lts  # Default
  release: supported
  release:
    - xenial
    - yakkety
    - fedora/22
```

#### Architecture

Architecture to test is defined by the system's architecture.

### Image Customization

There are two possible ways to customize an image: 1) push specific files to a container 2) use cloud-init's user-data to inject data.

#### Push Files

Files can be pushed over using `lxc file push` to customize the container. This is done via a list of lists specifying the source and then destination.

```
customize:
  push:
    - - my_local_script.sh
      - /usr/bin/
    - - examples/scripts/test.py
      - /root/
```

#### User-Data

If the image used contains cloud-init, then user-data can be passed to the container. This is done using a file containing the cloud data. This data is passed in via `--config=user.user-data=` option on container launch.

```
customize:
  user-data: my_data.txt
```

### Command Execution

Runs `lxc exec` on a command or list of commands to execute once the container is up and running.

```
execute: python my_script.py
execute:
  - whoami
  - date
  - uname -a
```

### File Collection

Files can be pulled using `lxc file pull` to collect information or results from the container. Only the source is required as all files will be put in the log directory.

```
collect:
  pull: file
  pull:
    - file1
    - file2
```

## Development

Running locally:

  * Install the dependencies via `pip install -r requirements.txt`
  * Run `python -m lxctest` or `python3 -m lxctest` for python3
  
For development and testing:

  * To run the tests you will need to install tox: `pip install tox`
  * Run `tox` after changes to get testing across Python 2.7 and 3.4
  * In addition, it will verify coverage and lint the code
  * To get coverage report run: `nosetests --with-coverage --cover-erase --cover-tests --cover-package=lxctest --cover-html` and see the cover directory for an HTML report.
  * Running `nosetest -d` will show values of the objects that fail the comparison in asserts
  * To see test output run `nosetests --nocapture` as the flag will pass standard out to the console to aid in debugging.
  
  
