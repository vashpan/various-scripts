#!/usr/bin/env python3

# This script is a utility that provides easy methods to create images for iOS development
# 
# It requires Pillow library and it is tested on OS X 12.x with Xcode 13
# 
# Easiest installation of Pillow library:
# 
# 1. Make sure you have 'pip3' available
#
# 2. Install dependencies (choose your package manager):
#   $ brew install libtiff libjpeg webp little-cms2
# or...
#   $ sudo port install tiff jpeg webp lcms2
#
# 3. Install Pillow from PIP repository:
#	$ pip3 install Pillow
# 
# For more information go here: http://pillow.readthedocs.org/en/latest/installation.html
# Enjoy! 
#

import os, os.path, sys, math

try:
	__import__("PIL")
except ImportError:
	print("This script requires Pillow library! You can find instructions for install here: http://pillow.readthedocs.org/en/latest/installation.html")
	exit(1)

from PIL import Image

# Constant sizes for checking (by default in landscape orientation)
valid_source_icon_size = (1024,1024)

image_postfixes = {
	'' : 0.25,
	'@2x' : 0.5,
	'@3x' : 0.75,
	'@2x~ipad' : 1.0,
	'~ipad' : 0.5
}

ios_icon_sizes = [
	('iOS-Icon-60@2x.png', (120, 120)),
	('iOS-Icon-60@3x.png', (180, 180)),
	
	('iOS-Icon-76.png', (76, 76)),
	('iOS-Icon-76@2x.png', (152, 152)),
	
	('iOS-Icon-83@2x.png', (167, 167)), # 83.5 x 2 in fact, for iPad Pro
	
	('iOS-Icon-57.png', (57, 57)),
	('iOS-Icon-57@2x.png', (114, 114)),
	
	('iOS-Icon-72.png', (72, 72)),
	('iOS-Icon-72@2x.png', (144, 144)),
	
	('iOS-Icon-40.png', (40, 40)),
	('iOS-Icon-40@2x.png', (80, 80)),
	('iOS-Icon-40@3x.png', (120, 120)),
	
	('iOS-Icon-29.png', (29, 29)),
	('iOS-Icon-29@3x.png', (87, 87)),
	('iOS-Icon-29@2x.png', (58, 58)),

	('iOS-Icon-20.png', (20, 20)),
	('iOS-Icon-20@2x.png', (40, 40)),
	('iOS-Icon-20@3x.png', (60, 60)),

	('iOS-Icon-50.png', (50, 50)),

	('iOS-AppStore.png', (1024, 1024))
]

watchos_icon_sizes = [
	('watchOS-Icon-24@2x.png', (48, 48)),
	('watchOS-Icon-27@2x.png', (55, 55)),

	('watchOS-Icon-29@2x.png', (58, 58)),
	('watchOS-Icon-29@3x.png', (87, 87)),

	('watchOS-Icon-40@2x.png', (80, 80)),
	('watchOS-Icon-44@2x.png', (88, 88)),
	('watchOS-Icon-50@2x.png', (100, 100)),

	('watchOS-Icon-86@2x.png', (172, 172)),
	('watchOS-Icon-98@2x.png', (196, 196)),
	('watchOS-Icon-108@2x.png', (216, 216)),

	('watchOS-AppStore.png', (1024, 1024)),
]

imessage_icon_sizes = [
    ('iMessage-Icon-60x45@2x.png', (120, 90)),
	('iMessage-Icon-60x45@3x.png', (180, 135)),

	('iMessage-Icon-29@2x.png', (58, 58)),
	('iMessage-Icon-29@3x.png', (87, 87)),

	('iMessage-Icon-60x50@2x.png', (120, 100)),
	('iMessage-Icon-60x50@3x.png', (180, 150)),

	('iMessage-Icon-67x50@2x.png', (134, 100)),

	('iMessage-Icon-74x55@2x.png', (148, 110)),

	('iMessage-Icon-27x20@2x.png', (54, 40)),
	('iMessage-Icon-27x20@3x.png', (81, 60)),

	('iMessage-Icon-32x24@2x.png', (64, 48)),
	('iMessage-Icon-32x24@3x.png', (96, 72)),

	('iMessage-AppStore.png', (1024, 1024)),
	('iMessage-MessagesAppStore.png', (1024, 768))
]

# Utility functions
def error(msg=""):
	print("error: %s" % (msg))
	exit(1)

def log_file_operation(filename):
	print("writing file: %s" % (os.path.basename(filename)))

def print_help():
	print("Usage:")
	print("%s <command> <args>\n" % (sys.argv[0]))
	print("Valid commands:\n")
	print("image <source_image> [destination_directory]")
	print("icon <source_icon> [destination_directory]")
	print("help - prints this message")

def make_sure_dir_exists(dirname):
	if not os.path.exists(dirname):
 		os.makedirs(dirname)	

# Support for commands
def handle_icon_cmd(args):
	if len(args) > 2:
		error("wrong number of icon command arguments!")

	# by default, out dir is current dir
	outdir = "."
	infile = os.path.expanduser(args[0])
	if len(args) == 2:
		outdir = args[1]
		make_sure_dir_exists(outdir)

	im = None
	try:
		im = Image.open(infile)
	except IOError:
		error("cannot find input file: %s" % (infile))

	# check if source file has a proper size
	size_valid = (valid_source_icon_size == im.size)

	if size_valid == False:
		error("invalid size of source icon! Valid size: %dx%d" % (valid_source_icon_size[0], valid_source_icon_size[1]) )

	# check if image is not transparent & doesn't have alpha channel
	has_alpha = im.mode == 'RGBA'
	if has_alpha == True:
		error("source icon can't have alpha channel!")

	ios_out_dir = os.path.join(outdir, "iOS")
	make_sure_dir_exists(ios_out_dir)
	for icon in ios_icon_sizes:
		outfile = os.path.join(ios_out_dir, icon[0])
		size = icon[1]

		log_file_operation(outfile)
		
		outim = im.resize(size, Image.ANTIALIAS)
		outim.save(outfile, "PNG")

	watchos_out_dir = os.path.join(outdir, "watchOS")
	make_sure_dir_exists(watchos_out_dir)
	for icon in watchos_icon_sizes:
		outfile = os.path.join(watchos_out_dir, icon[0])
		size = icon[1]

		log_file_operation(outfile)
		
		outim = im.resize(size, Image.ANTIALIAS)
		outim.save(outfile, "PNG")

	imessage_out_dir = os.path.join(outdir, "iMessage")
	make_sure_dir_exists(imessage_out_dir)
	for icon in imessage_icon_sizes:
		outfile = os.path.join(imessage_out_dir, icon[0])
		size = icon[1]

		log_file_operation(outfile)

		target_aspect_ratio = size[1] / size[0]
		target_width = valid_source_icon_size[0]
		target_height = valid_source_icon_size[1] * target_aspect_ratio
		target_box = (
			0, (valid_source_icon_size[1] - target_height) / 2.0, 
			target_width, (valid_source_icon_size[1] - (valid_source_icon_size[1] - target_height) / 2.0)
		)

		tempim = im.crop(target_box)		
		outim = tempim.resize(size, Image.ANTIALIAS)
		outim.save(outfile, "PNG")
#

def handle_image_cmd(args):
	if len(args) > 2:
		error("wrong number of icon command arguments!")

	# by default, out dir is current dir
	outdir = "."
	infile = os.path.expanduser(args[0])
	if len(args) == 2:
		outdir = args[1]
		make_sure_dir_exists(outdir)

	im = None
	try:
		im = Image.open(infile)
	except IOError:
		error("cannot find input file: %s" % (infile))

	for postfix in image_postfixes:
		basename, ext = os.path.splitext(infile)
		scale = image_postfixes[postfix]
		outfile = os.path.join(outdir, basename + postfix + ext)

		size = (int(math.ceil(im.size[0] * scale)), int(math.ceil(im.size[1] * scale)))
		log_file_operation(outfile)
		outim = im.resize(size, Image.ANTIALIAS)
		outim.save(outfile, "PNG")
#

# start
if len(sys.argv) == 1:
	print_help()
	exit(1)

cmd = sys.argv[1]
if cmd == "icon":
	handle_icon_cmd(sys.argv[2:])
elif cmd == "image":
	handle_image_cmd(sys.argv[2:])
elif cmd == "help" or cmd == "h" or cmd == "-h":
	print_help()
else:
	error("invalid command: %s" % (cmd)) 
