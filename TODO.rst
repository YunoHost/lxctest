TODO
====

lxctest.py
==========

-  Enable asyncio to run more than one test at a time.
-  Pretty print the config information

container.py
============

-  Better method for determining if a container is up (e.g. networking not up till?)
  -  you could look for an IP in lxc info
  - or do something like "lxc file pull <container name>/etc/resolv.conf - | grep -q nameserver", so basically waiting until you do have a DNS resolver in there
-  lxc config set, run get afterwards to confirm or print it out
-  Write tests (going to be long running most likly)
-  pulled files need to go into a specific directory or have name appended to them

documentation
=============

- Get it started
