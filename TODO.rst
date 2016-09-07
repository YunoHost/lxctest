TODO
====

lxctest.py
==========

-  Enable asyncio to run more than one test at a time.
-  Change logging directory to use datetime.datetime.now().isoformat() replace : with ""

container.py
============

-  make use of lxd api calls instead of commands
-  lxc config set, run get afterwards to confirm or print it out
-  Write tests (going to be long running most likly)
-  redirect lxc exec output to a file - how?
  - lxc exec "${containername}" -- bash -c 'echo user = \"root\" >> /etc/libvirt/qemu.conf'
  - better escaping of command
-  lxc pull contianer/folder/* allow wild card * only
-  lxc push container/folder/* allow wild card * only


documentation
=============

- Get it started
