vnf-model
=========

This is a repository for the model that I created as part of the
Boston University Computer Science Department networking depth exam.

The top-level directory of the repository contains scripts for creating
Linux containers that have separate Ethernet bridges for virtual Ethernet
isolation.

The scripts that are relevant to the model are in the scripts directory,
and are named with respect to Figure 1 in the paper "OpenNF: Enabling
Innovation in Network Function Control" by Gember-Jacobson et al.

The model currently only has the capability to simulate traffic flowing
to an NF and then being migrated to a different NF when a SLA for packet
loss is broken.

To use the scripts, execute the following steps on Ubuntu 14.04 LTS:

 $ git clone http://github.com/bucs2/vnf-model.git

Before the scripts can be used, the basic LXC package, Ruby, and tools for network bridges must be obtained:

 # apt-get install lxc ruby1.9.1 bridge-utils

Additonally, the Ruby library ("gem") netaddr must be installed:

 # gem install netaddr 

Then, a network containing five nodes in a star topology can be generated
from inside the nfv-model directory:

 $ sudo ruby xlxc-net.rb -n test -s 5 --create -t star

For each of these containers, you can copy the scripts from the scripts
directory and run them in the containers:

 # cp scripts/h1/run.py /var/lib/lxc/test0/rootfs/root/run.py
 # cp scripts/h2/run.py /var/lib/lxc/test1/rootfs/root/run.py
 # cp scripts/h3/run.py /var/lib/lxc/test2/rootfs/root/run.py
 # cp scripts/ids1/run.py /var/lib/lxc/test3/rootfs/root/run.py
 # cp scripts/ids2/run.py /var/lib/lxc/test4/rootfs/root/run.py

Then, each of the containers can be individually started on separate
terminals:

 # sudo ruby xlxc-start.rb -n test4    # log-in as root
 # python3 run.py

 # sudo ruby xlxc-start.rb -n test3    # log-in as root
 # python3 run.py

 # sudo ruby xlxc-start.rb -n test2    # log-in as root
 # python3 run.py

 # sudo ruby xlxc-start.rb -n test1    # log-in as root
 # python3 run.py

 # sudo ruby xlxc-start.rb -n test0    # log-in as root
 # python3 run.py

The SDN switch script will be run by the host machine in another shell,
since it connects all of the containers:

 $ cd scripts
 $ python3 run.py

The model should then run and output how many packets were transferred
to H2 and H3.
