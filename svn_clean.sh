#!/bin/bash

# This script deletes all .svn directories from current directory. 
find . -iname ".svn" -print0 | xargs -0 rm -r

