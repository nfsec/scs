#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -----------------
# title            : HTTPsrvREAPER
# description      : HTTP Server Header Scanner.
# author           : Patryk 'agresor' Krawaczynski
# date             : 01.08.2014
# version          : 0.2
# usage            : python3 httpsrvreaper.py [start net] [end net] | ./httpsrvreaper.py [start net] [end net]
# python version   : 3.2.3
# required modules : netaddr 0.7.11 (http://github.com/drkjam/netaddr/)
#                  : requests 2.3.0 (http://python-requests.org)
# notes            : Number of networks to scan is equal to the number of threads that script will launch.
# -----------------

import os
import sys
import json
import socket
import requests
import threading
from netaddr import *


def isopen(ip, port):
    """
    Check if IP address have open port.
    :param ip:
    :param port:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((ip, port))
        s.settimeout(None)
        s.shutdown(2)
        print("Connected to: " + str(ip) + " on port: " + str(port))
        return True
    except socket.error as e:
        print ("Problem with connection to: " + str(ip) + " on port: " + str(port) + ". Error code:", e)
        return False


def isconnected(address, port):
    """
    Try to connect to the host to check the internet connection.
    If host is unreachable do the infinite loop until host or connection is up.
    :param address:
    :param port:
    """
    while True:
        try:
            host = socket.gethostbyname(address)
            sock = socket.create_connection((address, port), 2)
            return
        except:
            pass


def worker(number):
    """
    Worker will scan only public IPs (with open http(80) port) from networks
    in CIDR/8 (cut to /16) notation and save IP, time to handle request and 
    server header in json format to logfile. If you lose power or scanning
    was interrupted - simply remove the last file of the subnet to resume
    scanning.
    :param number:
    """
    port = 80
    network = IPNetwork('{0}.0.0.0/8'.format(number))
    subnets = network.subnet(16)
    for subnet in subnets:
        logname = str(subnet).replace("/16","")+'.log'
        if os.path.isfile(logname):
            pass
        else:
            log_file = open(logname, mode='a', encoding='utf-8', buffering=1)
            for ip in subnet.iter_hosts():
                isconnected('nfsec.pl', 80)
                if ip.is_unicast() and not ip.is_private():
                    if isopen(str(ip), port):
                        print('Scanning:  {}'.format(ip))
                        http_ip = 'http://' + str(ip)
                        try:
                            headers = { 'User-Agent': 'HTTPsrvReaper/0.2 (+http://nfsec.pl)' }
                            req = requests.get(http_ip, timeout=10, allow_redirects=True, headers=headers)
                            srv_data = {}
                            srv = req.headers.get('server')
                            if not srv:
                                srv_data['Server'] = 'Undefined'
                            else:
                                srv_data['Server'] = srv
                            srv_data['IP'] = str(ip)
                            srv_data['Time'] = str(req.elapsed.total_seconds())
                            print (json.dumps(srv_data)+"\n")
                            log_file.write(json.dumps(srv_data)+"\n")
                        except:
                            pass
                    else:
                        pass
            log_file.close


def main(start, stop):
    """
    Start one thread per network to speedup scanning.
    :param start:
    :param stop:
    """
    threads = []
    for net in list(range(start, stop+1)):
        t = threading.Thread(target=worker, name=net, args=(net,))
        threads.append(t)
        t.start()

if __name__ == '__main__': 
    if len(sys.argv) != 3:
        print ('Usage: {} [start] [end] NET/8.'.format(sys.argv[0]))
        sys.exit(1)
    else:
        main(int(sys.argv[1]), int(sys.argv[2]))
