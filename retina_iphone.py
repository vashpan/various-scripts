#!/usr/bin/python

# Script for renaming in SVN all files that has @2x suffix, to add them ~iphone 
# to distinguish retina versions for iPhone only.
#
# It is working on given directory

import sys, os, os.path, glob, subprocess

def error(msg):
	print "Error:",msg
	exit(1)


# start
images = ["png", "jpg"]
files = []

dir = None
if len(sys.argv) == 2:
	dir = sys.argv[1]
	if dir[-1] == "/":
		dir = dir[0:-1] # remove '/' if user put it
	print "Renaming files in %s dir" % dir
else:
	error("wrong dir path")

for img_type in images:
	for full_path in glob.glob(dir + "/*." + img_type):
		prev_path = full_path
		base, path = os.path.split(full_path)
		path, ext  = os.path.splitext(path)

		retina_end = ""
		retina_start_pos = path.find("@2x")
		if retina_start_pos > 0:
			retina_end = path[retina_start_pos:]

			if retina_end == "@2x":
				orig_path = path
				path = base + "/" + path + "~iphone" + ext
				svn_ret = subprocess.call(["svn", "mv", prev_path + "@", path])
				if svn_ret == 0:
					print "Renamed: %s" % orig_path
				else:
					print "Rename %s failed!" % orig_path

		