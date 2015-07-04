#!/usr/bin/python

import sys

# conversions
def bytes_to_kb(bytes):
    return bytes / 1024.0

def bytes_to_mb(bytes):
    return bytes_to_kb(bytes) / 1024.0

def bytes_to_gb(bytes):
    return bytes_to_mb(bytes) / 1024.0

def bytes_to_tb(bytes):
    return bytes_to_gb(bytes) / 1024.0

def bytes_to_pb(bytes):
    return bytes_to_tb(bytes) / 1024.0

# find the best representation
def bytes_to_best(bytes):
    representations = [ 'KB', 'MB', 'GB', 'TB', 'PB' ]
    actualSize = bytes
    lastRepr = representations[0]
    for reprs in representations:
        actualSize /= 1024.0
        if round(actualSize) > 0.0:
            lastRepr = reprs
            continue
        else:
            break
    
    finalSize = bytes
    if lastRepr == 'KB':
        finalSize = bytes_to_kb(bytes)
    elif lastRepr == 'MB':
        finalSize = bytes_to_mb(bytes)
    elif lastRepr == 'GB':
        finalSize = bytes_to_gb(bytes)
    elif lastRepr == 'TB':
        finalSize = bytes_to_tb(bytes) 
    else:
        finalSize = bytes_to_pb(bytes)

    return "%.2f %s" % (finalSize, lastRepr) 

if len(sys.argv) == 2:
    print bytes_to_best(int(sys.argv[1]))
else:
    print 'Usage: %s <number_of_bytes>'