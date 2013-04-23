# UnitsSpriteMaker.py
#
# This script is used for creating cropped units sprites
# To run this script, you will need PIL library, for Windows 
# you can found it here:
#
# http://www.lfd.uci.edu/~gohlke/pythonlibs/#pil 
# ( this location contains binaries also for 64-bit Windows/Python )
#
# Usage: 'python UnitsSpriteMaker.py <XXXX> 
#
# Where <XXXX> is the name of input asset directory. 
#
# Output cropped sprites will be in XXXX_trim folder
# 
#
# Known issues: 
# - This script assumes that every input frame has the same size. and isnt enmpty space
#

import os, os.path, shutil, sys, glob

from PIL import Image

IMAGE_EXT = '.png'
OUTPUT_DIR = 'Playsoft'

def error(msg):
	print 'Error: %s' % msg
	exit(1)

def biggestBBox(bboxes):
	biggest = [sys.float_info.max, sys.float_info.max, 0.0, 0.0]

	for bbox in bboxes:
		if bbox[0] < biggest[0]:
			biggest[0] = bbox[0]
		if bbox[1] < biggest[1]:
			biggest[1] = bbox[1]
		if bbox[2] > biggest[2]:
			biggest[2] = bbox[2]
		if bbox[3] > biggest[3]:
			biggest[3] = bbox[3]
	
	return tuple(biggest)

def prepareUnit(dir):
	path = dir
	
	# find biggest bounding box
	print 'Finding biggest bounding box...'
	bboxes = []
	files = glob.glob(path + '/*' + IMAGE_EXT)
	for img_file in files:
		print 'file name' + img_file
		img = Image.open(img_file)
		bbox = img.getbbox()
		bboxes.append(bbox)
	
	biggest_bbox = biggestBBox(bboxes)
	
	# crop & save image with our biggest and constant bounding box
	print 'Cropping sprites to the biggest bounding box...'
	output_dir_name = 'trimed'
	output_dir = dir + '_trim'#os.path.join(dir, output_dir_name)
	
	if os.path.exists(output_dir):
		shutil.rmtree(output_dir)
	os.makedirs(output_dir)
	
	for img_file in files:
		img = Image.open(img_file)
		out_img = img.crop(biggest_bbox)
		out_img.load()
		
		img_out_file = os.path.join(output_dir, os.path.basename(img_file))
		print img_out_file
		
		out_img.save(img_out_file)

#
# START
#

if len(sys.argv) != 2:
	error('Specify unit number/directory.')
	
unit_dir = sys.argv[1]

prepareUnit(unit_dir)