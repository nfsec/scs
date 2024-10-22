#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------
# title            : BleachBitch
# description      : "Anti forensic software in forensics purposes."
# author           : Patryk 'agresor' Krawaczynski
# date             : 17.05.2017
# version          : 0.1
# usage            : ./bleachbitch.py > log.txt
# python version   : 3.5.1
# required modules : GitPython 1.0.2 (https://github.com/gitpython-developers/GitPython)
# notes            : The original idea and first version by Adam Ziaja (https://github.com/adamziaja/python/blob/master/bleachbit.py)
# -----------------

import os
from git import Repo
from xml.dom import minidom
import xml.etree.ElementTree as ET


def clone_repo(directory):
    """Clone BleachBit repo for cleaners files."""
    if os.path.isdir(directory):
        print("Repository already cloned. Skipping...")
    else:
        try:
            print("Cloning repository into `{0}` ...".format(directory))
            Repo.clone_from("http://github.com/az0/bleachbit", directory)
        except Exception as e:
            print("Error:", e)



def parse_path(xpath):
    """Check whether there are any files or directories."""
    try:
        check_code = os.system("ls -al %s > /dev/null 2>&1" % xpath)
        if check_code != 0:
            print("{} - Not Found.".format(xpath))
        else:
            print("{} - FOUND !!!".format(xpath))
    except Exception as e:
        print("Error:", e)


def parse_xmls(directory):
    """Extract the file paths and directories."""
    try:
        for file in os.listdir(directory):
            if file.endswith(".xml"):
                tree = ET.parse(directory + "/" + file)
                root = tree.getroot()
                label = root.find('label')
                if label is not None:
                    print("### Checking: ", label.text, end="")
                descr = root.find('description')
                if descr is not None:
                    print(" - " + descr.text)
                else:
                    print("")
                domtree = minidom.parse(directory + "/" + file)
                for i in domtree.getElementsByTagName('action'):
                    xpath = i.getAttribute('path')
                    if len(xpath) != 0:
                        if "/" not in xpath:
                            continue
                        else:
                            parse_path(i.getAttribute('path'))
    except Exception as e:
        print("Error:", e)

if __name__  == "__main__":
    clone_repo('bleachbit')
    parse_xmls('bleachbit/cleaners')
