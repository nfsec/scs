#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------
# title            : UnHider
# description      : Show hidden pids in Linux system.
# author           : Patryk 'agresor' Krawaczynski
# date             : 22.10.2024
# version          : 0.2
# usage            : python3 unhider.py
# python version   : 3.11.2
# -----------------

import os

proc_path = '/proc'

def process_list_behind_the_fog():
    pid_list = []
    for pid_number in os.listdir(proc_path):
        if os.path.isdir(os.path.join(proc_path, pid_number)):
            if pid_number.isnumeric():
                pid_list.append(int(pid_number))
    for pid_number in pid_list:
        for task_number in os.listdir(os.path.join(proc_path, str(pid_number), "task")):
            if int(task_number) in pid_list:
                pass
            else:
                pid_list.append(int(task_number))
    return(pid_list)

def process_list_before_the_fog():
    pid_list = []
    with open('/proc/sys/kernel/pid_max', 'r') as pid_max:
        upper_limit = int(pid_max.read()) + 1
    for pid_number in range(0, upper_limit):
        if os.path.isdir(os.path.join(proc_path, str(pid_number))):
            pid_list.append(int(pid_number))
    return(pid_list)

if __name__ == "__main__":
    print(f'## Hidden PID revealer v0.2 by NFsec.pl')
    print(f'')
    print(f'Scanning system please wait...')
    print(f'')
    print(f'PIDs from /proc: ' + str(process_list_behind_the_fog()))
    print(f'')
    print(f'PIDs enumerated: ' + str(process_list_before_the_fog()))
    print(f'')
    print(f'Hidden PIDs: ' + str(list(set(process_list_before_the_fog()) \
                           - set(process_list_behind_the_fog()))))
