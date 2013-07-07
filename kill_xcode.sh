#!/bin/bash
# Multiple times to kill everything for sure ;)

while kill -9 `ps x | grep Xcode | cut -c 1-6 | head -n 1` ; do : ; done
while kill -9 `ps x | grep Xcode | cut -c 1-6 | head -n 1` ; do : ; done
while kill -9 `ps x | grep Xcode | cut -c 1-6 | head -n 1` ; do : ; done
