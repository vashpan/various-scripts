#!/usr/bin/env python3

# A small script that helps when entering passwords 
# with separate "windows" for letters

import getpass

input_string = getpass.getpass("Enter password: ")

for i, char in enumerate(input_string):
    index = str(i+1).zfill(2)
    print(f"{index}: {char}")
