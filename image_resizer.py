#!/usr/bin/python

# This script is a utility that provides easy way to batch-resize various images
# 
# It requires Pillow library and it is tested on OS X 10.10 with Xcode 6.1
# 
# Easiest installation of Pillow library:
# 1. Make sure you have 'brew' installed
# 2. Make sure you have 'pip' installed (sudo easy_install pip)
# 3. Install all Pillow requirements for support many formats:
# 	$ brew install libtiff libjpeg webp little-cms2
# 4. Install Pillow from PIP repository:
#	$ pip install Pillow
# 
# For more information go here: http://pillow.readthedocs.org/en/latest/installation.html
# Enjoy! 

import string, os, os.path, sys, re

try:
	__import__("PIL")
except ImportError:
	print "This script requires Pillow library! You can find instructions for install here: http://pillow.readthedocs.org/en/latest/installation.html"
	exit(1)

from PIL import Image

# constants
MIN_SIZE = 2

# utility functions
def warning(msg=""):
	print "warning: %s" % (msg)

def error(msg=""):
	print "error: %s" % (msg)
	exit(1)

def log_file_operation(filename):
	print "writing file: %s" % (os.path.basename(filename))

def print_help():
	print "Usage:"
	print "%s <new_size> FILE1 [FILE2 ...]\n" % (sys.argv[0])
	print "You can describe new size in three formats:\n"
	print "1024x768: your out file will have this exact size"
	print "200%: your out file will be this percent bigger/smaller"
	print "0.5: your out file size will be multiplied by this value"
	print "help - prints this message"

# regexes
def is_number(param):
	return re.match(r'^[-+]?[0-9]*\.?[0-9]+$', param) != None

def is_size(param):
	return re.match(r'^[0-9]*[x][0-9]*$', param) != None

def is_percent(param):
	return re.match(r'^[1-9]\d*[%]$', param) != None

# resizing
def perform_resize(size_args, files):
	for im_file in files:
		# check if file format is supported
		im_filename, im_extension = os.path.splitext(im_file)
		supported_formats = ['.png', '.jpg', '.jpeg', '.tga']
		supported_formats += [string.upper(fmt) for fmt in supported_formats]
		if im_extension not in supported_formats:
			warning('unsupported format: %s' % im_extension)
			return

		im = None
		try:
			im = Image.open(im_file)
		except IOError:
			error("cannot find input file: %s" % (im_file))

		# figure out final size
		original_size = im.size
		destination_size = None
		if size_args[0] == 'size':
			destination_size = size_args[1]
		elif size_args[0] == 'scale':
			scale = size_args[1]
			destination_size = (original_size[0] * scale, original_size[1] * scale)
		elif size_args[0] == 'percent':
			scale = float(size_args[1]) / 100.0
			destination_size = (original_size[0] * scale, original_size[1] * scale)

		# make sure destination size is valid and integer
		destination_size = ( int(max(destination_size[0], MIN_SIZE)), 
			                 int(max(destination_size[1], MIN_SIZE)) )

		# resizing
		log_file_operation(im_file)
		outim = im.resize(destination_size, Image.ANTIALIAS)
		outim.save(im_file)

	return


# start
if len(sys.argv) == 1:
	print_help()
	exit(1)

cmd = param = sys.argv[1]
if cmd == "help" or cmd == "h" or cmd == "-h":
	print_help()
elif is_size(param):
	size = param.split('x')
	size = (int(size[0]), int(size[1]))
	perform_resize(('size', size), sys.argv[2:])
elif is_percent(param):
	percent = int(param[:-1])
	perform_resize(('percent', percent), sys.argv[2:])
elif is_number(param):
	scale = float(param)
	perform_resize(('scale', scale), sys.argv[2:])
else:
	print_help()
	exit(1)

