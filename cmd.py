""" Execute commands in BASH. """

import time
import subprocess

PROCESSES = []
MAX_BASH_COMMANDS = 100

def popen(cmd):
    while len(PROCESSES) >= MAX_BASH_COMMANDS:
        print('Waiting for a free process...')
        for i in sorted(range(len(PROCESSES)), reverse=True):
            if PROCESSES[i].poll() is not None:
                del PROCESSES[i]
        time.sleep(5)
    p = subprocess.Popen(cmd)
    PROCESSES.append(p)

def popen_wait():
    print()
    while len(PROCESSES):
        for i in sorted(range(len(PROCESSES)), reverse=True):
            print('\r' + 'Waiting for ' + str(len(PROCESSES)) + ' processes to complete... ', end='', flush=True)
            if PROCESSES[i].poll() is not None:
                del PROCESSES[i]
        time.sleep(5)
    print('All commands have  completed.')


