#!/usr/bin/python

# This script is a utility that provides easy methods to create images for iOS development
# 
# It requires Pillow library and it is tested on OS X 10.10 with Xcode 6.1
# 
# Easiest installation of Pillow library:
# 1. Make sure you have 'brew' installed
# 2. Make sure you have 'pip' installed (sudo easy_install pip)
# 2. Install all Pillow requirements for support many formats:
# 	$ brew install libtiff libjpeg webp little-cms2
# 3. Install Pillow from PIP repository:
#	$ pip install Pillow
# 
# For more information go here: http://pillow.readthedocs.org/en/latest/installation.html
# Enjoy! 

import os, os.path, sys

try:
	__import__("PIL")
except ImportError:
	print "This script requires Pillow library! You can find instructions for install here: http://pillow.readthedocs.org/en/latest/installation.html"
	exit(1)

from PIL import Image

# Constant sizes for checking
kValidSourceIconSizes = ( (512, 512), (1024,1024) )
kValidSourceDefaultScreenSize = (2300, 2300) 

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

# (filename, width, height, landscape?)
kiPhoneDefaultScreenSizes = [
	('Default.png', (320, 480), 0),
	('Default@2x.png', (640, 960), 0),
	('Default-568@2x.png', (640, 1136), 0),
]

kiPadDefaultScreenSizes = [
	('Default-Landscape.png', (1024, 748), 1),
	('Default-Portrait.png', (768, 1004), 0),
	('Default-Landscape@2x.png', (2048, 1496), 1),
	('Default-Portrait@2x.png', (1536, 2008), 0),
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
	vs = kValidSourceIconSizes
	size_valid = False
	for size in vs:
		if size == im.size:
			size_valid = True
			break

	if size_valid == False:
		error("invalid size of source icon! Possible sizes: %dx%d and %dx%d" % (vs[0][0], vs[0][1], vs[1][0], vs[1][0]))

	for icon in kIconSizes:
		outfile = os.path.join(outdir, icon[0])
		size = icon[1]

		log_file_operation(outfile)
		outim = im.resize(size, Image.ANTIALIAS)
		outim.save(outfile, "PNG")
#

def handle_image_cmd(args):
	if len(args) < 2:
		error("wrong number of image command arguments!")

	# by default, out dir is current dir, so we check if last item is a directory
	outdir = None
	infiles = args[0:-1]
	outdir = os.path.expanduser(args[-1])
	if outdir != None:
		make_sure_dir_exists(outdir)
	if not os.path.isdir(outdir):
		infiles.append(outdir)
		outdir = "."

	for infile in infiles:
		im = None
		try:
			im = Image.open(infile)
		except IOError:
			error("cannot find input file: %s" % (infile))

		infileBase, ext = os.path.splitext(infile)
		retinaPostfix = "@2x"
		hasRetinaPostfix = False
		if infileBase[-3:] == retinaPostfix:
			infileBase = infileBase[0:-3]
			hasRetinaPostfix = True

		# create retina image if not exists
		if not hasRetinaPostfix:
			outfile = infileBase + retinaPostfix + ext
			log_file_operation(outfile)
			im.save(outfile)

		# always create non-retina image
		outfile = infileBase + ext
		smallSize  = (im.size[0] / 2, im.size[1] / 2)
		outim = im.resize(smallSize, Image.ANTIALIAS)
		log_file_operation(outfile)
		outim.save(outfile)
	#
#

def handle_defaultscreen_cmd(args):
	# todo: remember to name iPad splash screens differently for portrait and landscape
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

	# check if source file has a proper size and calculate orientation
	kOrientationLandscape = 0
	kOrientationPortrait  = 1
	orientation = 0
	size_valid = (im.size == kValidSourceDefaultScreenSize)

	if size_valid == False:
		error("invalid size of default screen source! Possible size: %dx%d" % (kValidSourceDefaultScreenSize[0], kValidSourceDefaultScreenSize[1]))

	retinaPostfix = "@2x"
	all_default_screens = kiPhoneDefaultScreenSizes + kiPadDefaultScreenSizes
	for defaultscreen in all_default_screens:
		outfile = os.path.join(outdir, defaultscreen[0])
		size = defaultscreen[1]
		scrorientation = defaultscreen[2]
		isretina = (os.path.splitext(outfile)[0][-3:] == retinaPostfix)
		isiphone = (defaultscreen in kiPhoneDefaultScreenSizes)
		isipad = (defaultscreen in kiPadDefaultScreenSizes)

		log_file_operation(outfile)

		# rotate if necessary
		inim = im.copy()
		if orientation != scrorientation:
			inim = inim.rotate(-180, Image.NEAREST)

		# downsize if necessary
		if isiphone:
			inim = inim.resize((inim.size[0]/2, inim.size[1]/2), Image.ANTIALIAS)

		# crop image
		if isretina:
			cropscale = 1
		else:
			cropscale = 2

		W = inim.size[0]
		H = inim.size[1]
		w = size[0] * cropscale
		h = size[1] * cropscale
		cropbox = ( (W-w)/2, (H-h)/2, W-(W-w)/2, H-(H-h)/2 )
		outim = inim.crop(cropbox)
		
		# resize if non-retina
		if not isretina:
			outim = outim.resize(size, Image.ANTIALIAS)
		outim.save(outfile, "PNG")
	#
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
elif cmd == "defaultscreen":
	handle_defaultscreen_cmd(sys.argv[2:])
elif cmd == "help" or cmd == "h" or cmd == "-h":
	print_help()
else:
	error("invalid command: %s" % (cmd)) 
