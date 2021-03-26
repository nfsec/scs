#!/usr/bin/env python3
# -----------------
# title            : PKGkeeper
# description      : Script adds or removes packages from hold state
#                  : with apt-mark tool in Ubuntu using python sets.
# author           : Patryk 'agresor' Krawaczynski
# date             : 25.03.2021
# version          : 0.1
# usage            : ./pkgkeeper package1 package2 package2
#                  : ./pkgkeeper (clears all packages)
# python version   : 3.X
# required modules : python-apt (https://launchpad.net/python-apt/)
# notes            : Script without arguments will purge all packages from list.
# -----------------

import apt
import sys
import subprocess

def error(message):
    """
    Print error message and exit with status = 0.
    """
    print(message)
    sys.exit(1)


def check_package(package):
    """
    Check if package is installed in system before marking it.
    """
    try:
        cache = apt.Cache()
        pkg = cache[package]
        return pkg.is_installed
    except Exception as e:
        error("ERROR: " + str(e))


def new_markers():
    """
    Read name of packages from scripts arguments and create set of them.
    """
    new_markers = set()
    for x in sys.argv[1:]:
        if check_package(x):
            new_markers.add(x)
        else:
            error(f"ERROR: Package {x} not installed in system. Can't mark it.")
    return new_markers


def old_markers():
    """
    Read name of packages from existing 'hold list' and create set of them.
    """
    try:
        showhold = (subprocess.check_output("apt-mark showhold", stderr=subprocess.STDOUT, shell=True, universal_newlines=True).splitlines())
        old_markers = set(showhold)
        return old_markers
    except Exception as e:
        error("ERROR: " + str(e))

def compare_markers(old, new):
    """
    Compare two sets and return information in list - what to add and what to remove.
    """
    try:
        if new == old:
            sys.exit(0)
        else:
            add = new_markers().difference(old_markers())
            add = list(add)
            remove = old_markers().difference(new_markers())
            remove = list(remove)
            return add, remove
    except Exception as e:
        error("ERROR: " + str(e))


def add_markers(*args):
    """
    Add new packages to hold state.
    """
    if args is not None:
        try:
            for arg in args:
                subprocess.run(["apt-mark","hold",arg], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            error("ERROR: " + str(e))


def del_markers(*args):
    """
    Remove no longer needed packages from hold state.
    """
    if args is not None:
        try:
            for arg in args:
                subprocess.run(["apt-mark","unhold",arg], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            error("ERROR: " + str(e))


if __name__ == "__main__":
    add_markers(*compare_markers(new_markers(), old_markers())[0])
    del_markers(*compare_markers(new_markers(), old_markers())[1])
