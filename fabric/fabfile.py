#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -----------------
# title            : Fabric
# description      : Fabric input file for multinodes managment.
# author           : Patryk 'agresor' Krawaczynski
# date             : 11.04.2016
# version          : 0.1
# usage            : fab --skip-bad-hosts command:'if test -e /etc/file; then echo "Skipping"; else mv /etc/file /etc/file.old && wget -O file http://server.com/newfile; fi'
# python version   : 2.7.10
# required modules : Fabric 1.10.2 (http://www.fabfile.org/)
# notes            : fabfile.py must be in root directory when fab is executed.
# -----------------

from fabric.api import *
from fabric.colors import *
from fabric.contrib.console import confirm
from fabric.operations import *

env.user = ''
env.password = ''
env.roledefs = {
    'mynodes' : ['']
}

@roles('mynodes')
def command(runthis, failok=False):
    with hide("running", "stdout"):
        host = run("hostname -f")
        print(red("Hostname: ") + green(host))
    result = sudo(runthis, warn_only=True)
    if failok:
        pass
    else:
        if result.failed and not confirm("Commnd failed. Continue anyway?"):
            abort("Aborting at user request.")
    print(yellow("||| Done.") + "\n")
