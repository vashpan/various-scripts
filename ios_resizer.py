#!/usr/bin/python

# This script is a utility that provides easy methods to create images for iOS development
# 
# It requires Pillow library and it is tested on OS X 10.9 with Xcode 5.1, 

import os, os.path, sys

try:
	__import__("PIL")
except ImportError:
	print "This script requires Pillow library! You can find instructions for install here: http://pillow.readthedocs.org/en/latest/"
	exit(1)

from PIL import Image

# Constant sizes for checking
kValidSourceIconSizes = ( (512, 512), (1024,1024) )
kValidSourceDefaultScreenSizes = ( (640, 1136), (2048, 1496), (1536, 2008) ) 

kIconSizes = [
	('Icon-60@2x.png', (120, 120)),
	('Icon-76.png', (76, 76)),
	('Icon-76@2x.png', (152, 152)),
	('Icon.png', (57, 57)),
	('Icon@2x.png', (114, 114)),
	('Icon-72.png', (72, 72)),
	('Icon-72@2x.png', (144, 144)),
	('Icon-Small-40.png', (40, 40)),
	('Icon-Small-40@2x.png', (80, 80)),
	('Icon-Small.png', (29, 29)),
	('Icon-Small@2x.png', (58, 58)),
	('Icon-Small-50.png', (50, 50)),
	('Icon-Small-50@2x.png', (100, 100)),

	('iTunesArtwork', (512, 512))
]

kDefaultScreenSizes = [
	('Default.png', (320, 480)),
	('Default@2x.png', (640, 960)),
	('Default-568@2x.png', (640, 1136)),
	('Default-Landscape.png', (1024, 748)),
	('Default-Portrait.png', (768, 1004)),
	('Default-Landscape@2x.png', (2048, 1496)),
	('Default-Portrait@2x.png', (1536, 2008)),
]

# Utility functions
def error(msg=""):
	print "error: %s" % (msg)
	exit(1)

def log_file_operation(filename):
	print "writing file: %s" % (os.path.basename(filename))

def print_help():
	print "Usage:"
	print "%s <command> <args>\n" % (sys.argv[0])
	print "Valid commands:\n"
	print "icon <source_icon> [destination_directory]"
	print "image <source_image> [destination_directory]"
	print "defaultscreen <source_default_screen> [destination_directory]"
	print "help - prints this message"

# Support for commands
def handle_icon_cmd(args):
	if len(args) > 2:
		error("wrong number of icon command arguments!")

	# by default, out dir is current dir
	outdir = "."
	infile = args[0]
	if len(args) == 2:
		outdir = args[1]

	im = None
	try:
		im = Image.open(infile)
	except IOError:
		error("cannot find input file: %s" % (infile))
		
	for icon in kIconSizes:
		outfile = os.path.join(outdir, icon[0])
		size = icon[1]

		log_file_operation(outfile)
		outim = im.resize(size, Image.ANTIALIAS)
		outim.save(outfile, "PNG")

	return 

def handle_image_cmd(args):
	return False

def handle_defaultscreen_cmd(args):
	# todo: remember to name iPad splash screens differently for portrait and landscape
	return False



# start
if len(sys.argv) == 1:
	print_help()
	exit(1)

cmd = sys.argv[1]
if cmd == "icon":
	handle_icon_cmd(sys.argv[2:])
elif cmd == "image":
	handle_image_cmd(sys.argv[2:])
elif cmd == "defaultscreen":
	handle_defaultscreen_cmd(sys.argv[2:])
elif cmd == "help" or cmd == "h" or cmd == "-h":
	print_help()
else:
	error("invalid command: %s" % (cmd)) 