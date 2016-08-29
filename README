lxctest
=======

.. image:: https://img.shields.io/pypi/v/lxctest.svg
   :target:  https://pypi.python.org/pypi/lxctest/

Overview
--------

lxctest provides a wrapper around lxd-client tools to automate test
execution, while leaving the test creation and analysis to the user. It
uses LXC to launch Ubuntu containers with specific customizations, run a
series of commands, and items to gather as output all set by the user.
By using LXC the user has a much faster way of running tests compared to
VMs.

Running lxctest
---------------

Distribution Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    sudo apt install lxd distro-info python3-pip python3-yaml

Install via PyPI
~~~~~~~~~~~~~~~~

::

    pip3 install lxctest
    lxctest <filename>

Install via git
~~~~~~~~~~~~~~~

::

    git clone https://github.com/powersj/lxctest
    cd lxctest
    pip3 install -r requirements.txt
    python3 -m lxctest <filename>

YAML Format
-----------

A single YAML test case file is used to define the following items for
each test:

-  Image Specification
-  Image Customization
-  Command Execution
-  File Collection

The syntax for each of the above is defined below.

Image Specification
~~~~~~~~~~~~~~~~~~~

The image specification defines what LXC image will be used for the
test. This includes the store and release. If no options are received,
then by default the release LTS image will be used. Specifically:

::

    lxc:
      store: release
      releases: lts

Store
^^^^^

Defines which store of Ubuntu images to use. Two options:

-  images: standard images, see ``lxc image list images:`` for a full
   list. This is the default option.
-  ubuntu: Images containing cloud-init, see ``lxc image list ubuntu:``
   for a full list.
-  ubuntu-daily: Daily images containing cloud-init, see
   ``lxc image list ubuntu-daily:`` for a full list.

::

    lxc:
      store: images  # Default
      store: ubuntu
      store: ubuntu-daily

Release
^^^^^^^

Defines the targeted releases from the following options:

-  lts: Use the current Ubuntu LTS, see ``ubuntu-distro-info --lts``.
   This is the default option.
-  supported: Run across all supported Ubuntu versions, see
   ``ubuntu-distro-info --supported``.
-  Specify a specific collection of releases. If one of the releases
   does not exist then no tests will run.

::

    lxc:
      releases: lts  # Default
      releases: supported
      releases:
        - xenial
        - yakkety
        - fedora/22

Architecture
^^^^^^^^^^^^

Architecture to test is defined by the system's architecture.

Image Customization
~~~~~~~~~~~~~~~~~~~

There are two possible ways to customize an image: 1) push specific
files to a container 2) use cloud-init's user-data to inject data.

Push Files
^^^^^^^^^^

Files can be pushed over using ``lxc file push`` to customize the
container. This is done via a list of lists specifying the source and
then destination.

::

    push:
      - - my_local_script.sh
        - /usr/bin/
      - - examples/scripts/test.py
        - /root/

User-Data
^^^^^^^^^

If the image used contains cloud-init, then user-data can be passed to
the container. This is done using a file containing the cloud data. This
data is passed in via ``--config=user.user-data=`` option on container
launch.

::

    user-data: my_data.txt

Command Execution
~~~~~~~~~~~~~~~~~

Runs ``lxc exec`` on a list of commands to execute once the container is
up and running.

::

    execute:
      - python my_script.py
    execute:
      - whoami
      - date
      - uname -a

File Collection
~~~~~~~~~~~~~~~

Files can be pulled using ``lxc file pull`` to collect information or
results from the container. Only the source is required as all files
will be put in the log directory.

::

    pull:
      - file
    pull:
      - file1
      - file2
