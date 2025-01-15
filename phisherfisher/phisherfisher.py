#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------
# title            : PhisherFisher
# description      : This script checks if the domain is
#                  : a phishing domain known to CERT.pl.
# author           : Patryk 'agresor' Krawaczynski
# date             : 15.01.2025
# version          : 0.2
# usage            : python3 phisherfisher.py <URL>
# python version   : 3.11.2
# required modules : requests, tldextract, rapidfuzz
# -----------------

import os
import re
import sys
import time

import requests
import tldextract
from rapidfuzz import process, fuzz

allow_list = [
    'nfsec.pl',
]

phishing_file = 'domains.txt'
phishing_url = 'https://hole.cert.pl/domains/domains.txt'


def check_phishing() -> bool:
    with open(phishing_file, 'r') as f:
        picks: list[str] = [line.split()[0] for line in f]
    if find_similar_score(picks):
        return True
    elif find_similar_subdomain_charm(picks):
        return True
    elif find_similar_domain_charm(picks):
        return True
    else:
        return False


def find_similar_score(entries: list[str]) -> bool:
    report: list[tuple[str, float, int]] = process.extract(
        query=fqdn,
        choices=entries,
        limit=999999,
        score_cutoff=90
    )
    if not report:
        print(f'INFO: Based on score, no similar phishing domain(s) found.')
        return False
    else:
        print(f'INFO: Domain score found {len(report)} similar phishing domain(s).'
              f' Example:\n      {report[0][0]} with score {round(report[0][1], 2)}.')
        return True


def find_similar_subdomain_charm(entries: list[str]) -> bool:
    report = [entry for entry in entries
              if re.search(f'^{subdomain}\.', entry)
              and create_map(fqdn) == create_map(entry)]
    if not report:
        print(f'INFO: Based on subdomain charm, no similar phishing domain(s) found')
        return False
    else:
        print(f'INFO: Subdomain charm found {len(report)} similar'
              f' phishing domain(s). Example(s):\n      {report[0]}.')
        return True


def find_similar_domain_charm(entries: list[str]) -> bool:
    report = [(entry, score) for entry in entries
              if (score := fuzz.WRatio(create_map(fqdn), create_map(entry),
                                       score_cutoff=95)) > 95
              and re.search(f'\.{tld}$', entry)]
    if not report:
        print(f'INFO: Based on score, no similar phishing domain(s) found.')
        return False
    else:
        print(f'INFO: Domain charm found {len(report)} similar phishing domain(s).'
              f' Example:\n      {report[0][0]} with score {round(report[0][1], 2)}.')
        return True


def create_map(item: str) -> str:
    return ''.join('a' if c.isalpha() else
                   'd' if c.isdigit() else
                   c for c in item)


def download_phishing_domains() -> None:
    remove_old_file(phishing_file)
    http_headers = {
        'User-Agent': 'Threat Hunting Team from NFsec.pl'
    }
    if not os.path.exists(phishing_file):
        response = requests.get(phishing_url,
                                allow_redirects=True,
                                headers=http_headers)
        if response.status_code == 200:
            with open(phishing_file, 'wb') as f:
                f.write(response.content)
        else:
            print('ERROR: Failed to download phishing domains list.')
            sys.exit(2)


def remove_old_file(file: str) -> None:
    if os.path.exists(file):
        file_age = time.time() - os.path.getctime(file)
        if file_age > 3600:
            os.remove(file)
            print(f'INFO: Removed old file {file}.')
        else:
            print(f'INFO: File {file} is too young to remove.')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <URL>')
        sys.exit(2)
    url: str = sys.argv[1]
    extracted = tldextract.extract(url)
    fqdn: str = extracted.fqdn; domain: str = extracted.registered_domain
    tld: str = extracted.suffix; subdomain: str = extracted.subdomain
    if fqdn in allow_list or domain in allow_list:
        print('INFO: Domain is in allow list. Skipping...')
    else:
        download_phishing_domains()
        if not check_phishing():
            sys.exit(1)
        else:
            sys.exit(0)
