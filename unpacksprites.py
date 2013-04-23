#!/usr/bin/python
#coding: utf8
#
# Konrad Kołakowski
# Copyright (C) Playsoft 2012
#
# This script is used for unpacking sprites from cocos2d .plist sprite sheets.
# I assume you are using Python 2.7 or later. Earlier versions not tested. 
# Usage: Usage: ./unpacksprites.py <plist_sheet_path> <target_dir>
# Unpacked sprites will be write to the root off target directory as .png files.
#
#
# To use it, you need to have PIL library.
# This is how to install it on Mac OS X ( should work on 10.7 or later ):
# Download:
#	curl -O -L http://effbot.org/downloads/Imaging-1.1.7.tar.gz
# Extract:
# 	tar -xzf Imaging-1.1.7.tar.gz
#	cd Imaging-1.1.7
# Build and install:
#	python setup.py build
#	sudo python setup.py install   -> for all users
#   python setup.py install --user -> only for you
#

import string, sys, os, glob, plistlib
from PIL import Image

def print_usage():
	print 'Usage: ./unpacksprites.py <plist_sheet_path> <target_dir>' 

def load_args(args):
	if len(args) != 3:
		print_usage()
		exit()

	plist_path = args[1]
	target_dir = args[2]
	
	if not os.path.exists(plist_path) or not os.path.isfile(plist_path):
		print 'Error: %s file does not exists!' % plist_path
		exit()
	
	return plist_path, target_dir

def texture_path(plist_path):
	base = os.path.splitext(plist_path)[0]
	texture = base + '.png' # PNG files by default
	
	if not os.path.exists(texture) or not os.path.isfile(texture):
		print 'Error: %s texture does not exists!' % texture
		exit()
	
	return texture

def image_from_frame(frame, texture):
	if frame['rotated'] == True:
		tmp = frame['width']
		frame['width']  = frame['height']
		frame['height'] = tmp 

	box = ( int(frame['x']), int(frame['y']), 
	        int(frame['x'] + frame['width']), int(frame['y'] + frame['height']) )  

	im = Image.open(texture)
	im = im.crop(box)
	if frame['rotated'] == True:
		im = im.rotate(90)

	return im
	
def save_sprite(img, frame_name, target_dir):
	if not os.path.exists(target_dir):
		os.makedirs(target_dir)

	# force PNG format of output sprites
	img_name = os.path.splitext(frame_name)[0] + '.png' 
	path = os.path.join(target_dir, img_name)
	
	img.save(path)

# -1 = unknown 0 - classic format, 1 - modern format, 2 - even different format
def sheet_format_version(root):
	sheet_version = 0
	if 'metadata' in root:
		sheet_version = 1
	
	if not 'frames' in root:
		sheet_version = -1
	
	if sheet_version == -1:
		print 'Error: sheet format uknonwn!'
		exit()
	
	return sheet_version


# Script entry
plist, dir    = load_args(sys.argv)
root          = plistlib.readPlist(plist)
texture       = texture_path(plist)
sheet_version = sheet_format_version(root)


print 'Texture name: %s' % texture
for frame_name in root['frames']:
	frame = None
	rotated = False
	if sheet_version == 1:
		# support for modern sprite sheet format
		sprite = root['frames'][frame_name]
		pos_rect = None
		if 'frame' in sprite:
			pos_rect = eval(sprite['frame'].replace('{', '[').replace('}', ']'))
		elif 'textureRect' in sprite:
			pos_rect = eval(sprite['textureRect'].replace('{', '[').replace('}', ']'))
		
		if 'rotated' in sprite:
			rotated = sprite['rotated']

		x      = pos_rect[0][0]
		y      = pos_rect[0][1]
		width  = pos_rect[1][0]
		height = pos_rect[1][1]
		
		frame = dict()
		frame['x']       = x
		frame['y']       = y
		frame['width']   = width
		frame['height']  = height
		frame['rotated'] = rotated
	else:
		sheet_frame = root['frames'][frame_name]
		
		frame = dict()
		frame['x']       = sheet_frame['x']
		frame['y']       = sheet_frame['y']
		frame['width']   = sheet_frame['width']
		frame['height']  = sheet_frame['height']
		frame['rotated'] = rotated
	
	frame['name'] = frame_name
	print "%s\t => x:%d y:%d w:%d h:%d" % (frame_name, frame['x'], frame['y'], frame['width'], frame['height'])
	
	img = image_from_frame(frame, texture)
	save_sprite(img, frame_name, dir)

