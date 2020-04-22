#!/usr/bin/python3

# TODOs:
# - add option to use "hdiutil" and .dmg format
# - maybe try to estimate % of progress according to input? 

import sys, os
from getpass import getpass

# helpers
def print_usage_and_exit(msg = None):
    if msg != None:
        print(msg + "\n")

    print("Usage: %s [-c] source destination" % sys.argv[0])
    exit(1)

def backup_7z(use_compression, password, source, destination):
    launch_args = ["7z", "a", "-p%s" % password, "-mhe=on", '"' + destination + '"', '"' + source + '"']
    if not use_compression:
        launch_args.insert(4, "-m0=Copy")

    launch_cmd = " ".join(launch_args)

    cmd_result = os.system(launch_cmd)

    if cmd_result == 0:
        print("OK!")


# check & parse arguments
args_count = len(sys.argv)

source = None
destination = None
use_compression = False
password = None

if args_count == 4:
    compression_flag = sys.argv[1]
    if compression_flag == "-c":
        use_compression = True
    else:
        print_usage_and_exit("Unrecognized flag: %s" % compression_flag)

    source = sys.argv[2]
    destination = sys.argv[3]
elif args_count == 3:
    use_compression = False
    source = sys.argv[1]
    destination = sys.argv[2]
else:
    print_usage_and_exit()

# perform backup
print("(Very) Lazy Backup Script!")
print()
print("Compression: %r" % use_compression)
print()
password = getpass("Password: ")
if password != getpass("Retype password: "):
    print("Passwords don't match!")
    exit(2)

print()
print("Archiving: %s -> %s ..." % (source, destination))

# print(source)
# print(destination)
# print(use_compression)
# print(password)

backup_7z(use_compression, password, source, destination)
