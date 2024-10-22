#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------
# title            : SSLsrvREAPER
# description      : TLS Certificate Server Scraper.
# author           : Patryk 'agresor' Krawaczynski
# date             : 28.09.2024
# version          : 0.1
# usage            : python3 sslsrvreaper.py
# python version   : 3.11.2
# required modules : -
# -----------------
import json
import socket
import ssl
import time


def check_open_port(host: str, port: int, timeout: int):
    """
    Check that the IP address has an open port.
    :param host:
    :param port:
    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
        sock.settimeout(None)
        sock.shutdown(2)
        print(f'Connected to: {host} on port: {port}')
        return True
    except socket.error as e:
        print(f'Problem with connection to: {host} on port {port}. Error message: {e}')
        return False


def check_connection(host: str, port: int, timeout: int):
    """
    Try connecting to the host to check the Internet connection.
    If host is unreachable, run the infinite loop until host or connection is up.
    :param host:
    :param port:
    :return:
    """
    while True:
        try:
            socket.gethostbyname(host)
            socket.create_connection((host, port), timeout)
            return True
        except Exception as error:
            print(error)


def ssl_worker(host: str, port: int, timeout: int):
    """
    Connect to the server and get certificate information.
    :param host:
    :return:
    """
    try:
        ssl_client = ssl.create_default_context()
        ssl_client.check_hostname = False
        ssl_client.hostname_checks_common_name = False
        with ssl_client.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=host) as sock:
            sock.settimeout(timeout)
            sock.connect((host, port))
            cert = sock.getpeercert()
            sock.settimeout(None)
            sock.shutdown(2)
            cert_dict = {}
            cert_dict['subject_hostName'] = host
            cert_dict['subject_hostIP'] = socket.gethostbyname(host)
            for key in cert:
                if type(cert[key]) is tuple:
                    for value in cert[key]:
                        if type(value) is tuple:
                            if len(value) == 1:
                                cert_dict[key + "_" + str(value[0][0])] = str(value[0][1])
                            else:
                                cert_dict.setdefault(key, [])
                                cert_dict[key].append(value[1])
                        else:
                            cert_dict[key] = value
                else:
                    cert_dict[key] = cert[key]
        log_file = open('domains.log', mode='a', encoding='utf-8', buffering=1)
        log_file.write(json.dumps(cert_dict) + "\n")
        log_file.close()
    except Exception as error:
        print(error)


if __name__ == '__main__':
    with open('domains.txt', 'r') as domains:
        for domain in domains:
            check_connection('nfsec.pl', 443, 5)
            host = domain.strip()
            if check_open_port(host, 443, 5):
                ssl_worker(host, 443, 5)
                time.sleep(1)
