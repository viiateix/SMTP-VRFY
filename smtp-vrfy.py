#!/usr/bin/python

import socket
import sys

'''
Begin snippet for gsstyle.py, a paste-in or importable module for
output style for use in future scripts.
'''

import colorama
from colorama import Fore, Back, Style

colorama.init()

def printinfo(output):
    print Style.DIM + "[*] ",
    for field in output:
        print field,
    print Style.RESET_ALL

def printresult(output):
    print Style.BRIGHT + Fore.BLUE + "[>] ",
    for field in output:
        print field,
    print Style.RESET_ALL

def printalert(output):
    print Style.BRIGHT + Fore.RED + "[!] ",
    for field in output:
        print field,
    print Style.RESET_ALL

'''
End snippet for gsstyle.py.
'''

# Help section
#
if len(sys.argv) != 4:
    print "Usage: ./smtp-vrfy.py <ip.addr> <port> <input_file>"
    print
    print "ARGUMENT        FORMAT  DESCRIPTION"
    print " <ip.addr>       IPv4    IP address of host you want to test."
    print " <port>          int     Destination (server) port to use. Typically 25."
    print " <input_file>    str     File with list of usernames to VRFY."
    print
    print "Ex:"
    print "  # ./smtp-vrfy.py 10.11.1.254 25 usernames.txt"
    print
    sys.exit(0)


               
# Set skip value
skip = 0

# Create the socket
printinfo(["Creating socket..."])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
printinfo(["Connecting to", sys.argv[1], "on port", sys.argv[2], "..."])
try:
    connect = s.connect((sys.argv[1], int(sys.argv[2])))
except:
    printalert(["Cannot connect to", sys.argv[1], "...!"])
    printinfo(["Ending ..."])
    skip = 1

# Receive the banner
if skip != 1:
    printinfo(["Retrieving banner..."])
    banner = s.recv(1024)
    printresult([banner])

# Ingest file of usernames
if skip != 1:
    with open(sys.argv[3]) as f:
        namelist = f.readlines()

# Strip escaped newlines
if skip != 1:
    namelist = [x.strip('\n') for x in namelist]
    printinfo(["Testing usernames in", sys.argv[3], "..."])

# VRFY the usernames
if skip != 1:
    for name in namelist:
        if name != '':
            s.send('VRFY ' + name + '\r\n')
            result = s.recv(1024)
            if "550" not in result:
                printresult([result])

# Close the socket
printinfo(["Closing socket..."])
s.close()
