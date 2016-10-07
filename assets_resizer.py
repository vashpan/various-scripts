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

import os, os.path, sys, math

try:
	__import__("PIL")
except ImportError:
	print "This script requires Pillow library! You can find instructions for install here: http://pillow.readthedocs.org/en/latest/installation.html"
	exit(1)

from PIL import Image

# Constant sizes for checking (by default in landscape orientation)
kValidSourceIconSize = (1024,1024)
kValidSourceDefaultScreenSize = (2300, 2700)

kImagePostfixes = {
	'' : 0.25,
	'@2x' : 0.5,
	'@3x' : 0.75,
	'@2x~ipad' : 1.0,
	'~ipad' : 0.5
}

kIconSizes = [
	('Icon-60@2x.png', (120, 120)),
	('Icon-60@3x.png', (180, 180)),
	('Icon-76.png', (76, 76)),
	('Icon-76@2x.png', (152, 152)),
	('Icon-83@2x.png', (167, 167)), # 83.5 x 2 in fact, for iPad Pro
	('Icon.png', (57, 57)),
	('Icon@2x.png', (114, 114)),
	('Icon-72.png', (72, 72)),
	('Icon-72@2x.png', (144, 144)),
	('Icon-Small-40.png', (40, 40)),
	('Icon-Small-40@2x.png', (80, 80)),
	('Icon-Small-40@3x.png', (120, 120)),
	('Icon-Small.png', (29, 29)),
	('Icon-Small@2x.png', (58, 58)),
	('Icon-Small@3x.png', (87, 87)),
	('Icon-Small-50.png', (50, 50)),
	('Icon-20.png', (20, 20)),
	('Icon-20@2x.png', (40, 40)),
	('Icon-20@3x.png', (60, 60)),

	('iTunesArtwork', (1024, 1024))
]

# (filename, width, height, landscape?)
kiPhoneDefaultScreenSizes = [
	('Default.png', (320, 480), 0),
	('Default@2x.png', (640, 960), 0),
	('Default-568@2x.png', (640, 1136), 0),
	('Default-667@2x.png', (750, 1334), 0),
	('Default-736@3x.png', (1242, 2208), 0),
	('Default-Landscape-736@3x.png', (2208, 1242), 1)
]

kiPadDefaultScreenSizes = [
	('Default-Landscape.png', (1024, 748), 1),
	('Default-Portrait.png', (768, 1004), 0),
	('Default-Landscape@2x.png', (2048, 1496), 1),
	('Default-Portrait@2x.png', (1536, 2008), 0),
]

kiPhoneScreenshotSizes = [
	('-iP4-960x640.png', (960, 640)),
	('-iP5-1136x640.png', (1136, 640)),
	('-iP6-1334x750.png', (1334, 750)),
	('-iP6P-2208x1242.png', (2208, 1242)),
]

kiPadScreenshotSizes = [
	('-iPad1-1024x768.png', (1024, 768)),
	('-iPad3-2048x1536.png', (2048, 1536)),
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
	print "image <source_image> [destination_directory]"
	print "icon <source_icon> [destination_directory]"
	print "launchscreen <source_launch_screen> [destination_directory]"
	print "screenshot --ipad/--iphone <source_screenshot> [destination_directory]"
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
	size_valid = (kValidSourceIconSize == im.size)

	if size_valid == False:
		error("invalid size of source icon! Valid size: %dx%d" % (kValidSourceIconSize[0], kValidSourceIconSize[1]) )

	for icon in kIconSizes:
		outfile = os.path.join(outdir, icon[0])
		size = icon[1]

		log_file_operation(outfile)
		outim = im.resize(size, Image.ANTIALIAS)
		outim.save(outfile, "PNG")
#

def handle_launchscreen_cmd(args):
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

	retinaPostfix = ("@2x", "@3x")
	retinaScale = 1
	all_default_screens = kiPhoneDefaultScreenSizes + kiPadDefaultScreenSizes
	for launchscreen in all_default_screens:
		outfile = os.path.join(outdir, launchscreen[0])
		size = launchscreen[1]
		scrorientation = launchscreen[2]
		postfix = os.path.splitext(outfile)[0][-3:]
		isretina = (postfix in retinaPostfix)
		if isretina:
			retinaScale = int(postfix[1])
		isiphone = (launchscreen in kiPhoneDefaultScreenSizes)
		isipad = (launchscreen in kiPadDefaultScreenSizes)

		log_file_operation(outfile)

		# copy & downsize if necessary (not on 6+)
		inim = im.copy()
		if isiphone and retinaScale < 3:
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

def handle_screenshot_cmd(args):
	kScreenshotiPhone = 0
	kScreenshotiPad = 1

	if len(args) > 3:
		error("wrong number of icon command arguments!")

	# check what screenshot we want
	screenshotType = None
	if args[0] == "--ipad":
		screenshotType = kScreenshotiPad
	elif args[0] == "--iphone":
		screenshotType = kScreenshotiPhone
	else:
		error("you need to choose if you want iPad or iPhone screenshot!")

	# by default, out dir is current dir
	outdir = "."
	infile = os.path.expanduser(args[1])
	if len(args) == 3:
		outdir = args[2]
		make_sure_dir_exists(outdir)

	im = None
	try:
		im = Image.open(infile)
	except IOError:
		error("cannot find input file: %s" % (infile))

	# check if source file has a proper size
	landscape = im.size[0] > im.size[1]
	sizes = None
	if screenshotType == kScreenshotiPhone:
		sizes = kiPhoneScreenshotSizes
	elif screenshotType == kScreenshotiPhone:
		sizes = kiPadScreenshotSizes

	src_size = im.size
	size_valid = False
	for s in sizes:
		size = s[1]
		if not landscape:
			size = (size[1], size[0])

		if	src_size == size:
			size_valid = True
			break

	if size_valid == False:
		error("invalid size of screenshot source! Check Apple documentation for valid sizes")

	# rescale
	for screenshot in sizes:
		basename = os.path.splitext(os.path.basename(infile))[0]
		outfile = os.path.join(outdir, basename + screenshot[0])
		size = screenshot[1]
		if not landscape:
			size = (size[1], size[0])

		log_file_operation(outfile)
		outim = im.resize(size, Image.ANTIALIAS)
		outim.save(outfile, "PNG")

	return
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

	for postfix in kImagePostfixes:
		basename, ext = os.path.splitext(infile)
		scale = kImagePostfixes[postfix]
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
elif cmd == "launchscreen":
	handle_launchscreen_cmd(sys.argv[2:])
elif cmd == "screenshot":
	handle_screenshot_cmd(sys.argv[2:])
elif cmd == "image":
	handle_image_cmd(sys.argv[2:])
elif cmd == "help" or cmd == "h" or cmd == "-h":
	print_help()
else:
	error("invalid command: %s" % (cmd)) 
