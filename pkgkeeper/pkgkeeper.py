#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------
# title            : PKGkeeper
# description      : Script adds or removes packages from hold state 
#                  : with apt-mark tool in Ubuntu [12.04.4 LTS] using sets.
# author           : Patryk 'agresor' Krawaczynski
# date             : 25.08.2014
# version          : 0.2
# usage            : ./pkgkeeper.py package1 package2 package2
#                  : ./pkgkeeper.py (clears all packages)
# python version   : 2.7.8
# required modules : python-apt 0.8.3 (https://launchpad.net/python-apt/)
# notes            : Script without arguments will purge all packages from list.
# -----------------

import gc
import apt
import sys
import subprocess


def error(message):
    """
    Print error message and exit with status = 2.
    :rtype : object
    :param message:
    """
    print message
    sys.exit(2)


def check_package(package):
    """
    Check if package is installed in system before marking it.
    :type package: object
    :param package: 
    :return: 
    """
    try:
        gc.collect()
        cache = apt.Cache()
        pkg = cache[package]
        pkg.is_installed
        return pkg.is_installed
    except KeyError, e:
        error("ERROR: " + str(e))


def new_markers():
    """
    Read name of packages from scripts arguments and create set of them.
    :return:
    """
    new_markers = []
    for x in sys.argv[1:]:
        if check_package(x):
            new_markers.append(x)
        else:
            error("ERROR: Package %s not installed in system. Can't mark it." % x)
    new_markers_set = set(new_markers)
    return new_markers_set


def old_markers():
    """
    Read name of packages from existing 'hold list' and create set of them.
    :rtype : object
    :return:
    """
    try:
        old_markers = subprocess.check_output("apt-mark showhold", stderr=subprocess.STDOUT, shell=True).splitlines()
        old_markers_set = set(old_markers)
        return old_markers_set
    except subprocess.CalledProcessError, e:
        error("ERROR: " + str(e))


def compare_markers(old, new):
    """
    Compare two sets and return information in list - what to add and what to remove.
    :param old:
    :param new:
    :return:
    """
    if new == old:
        print "Nothing to add. Nothing to diminish. Carry on..."
        sys.exit(0)
    else:
        add = new_markers().difference(old_markers())
        add = list(add)
        remove = old_markers().difference(new_markers())
        remove = list(remove)
        return add, remove


def add_markers(*args):
    """
    Add new packages to hold state.
    :param args:
    :return:
    """
    if args is not None:
        try:
            for arg in args:
                subprocess.check_output("apt-mark hold %s" % arg, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError, e:
            error("ERROR: " + str(e))


def del_markers(*args):
    """
    Remove no longer needed packages from hold state.
    :param args:
    :return:
    """
    if args is not None:
        try:
            for arg in args:
                subprocess.check_output("apt-mark unhold %s" % arg, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError, e:
            error("ERROR: " + str(e))


if __name__ == "__main__":
    add_markers(*compare_markers(new_markers(), old_markers())[0])
    del_markers(*compare_markers(new_markers(), old_markers())[1])
