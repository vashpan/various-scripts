#!/usr/bin/python
#
# Script for creating rescaled versions of BMFont .fnt files.
# Usage: bmfontscale.py font.fnt 2

import sys, os.path, string

def error(msg):
	print "Error: %s" % msg
	exit(1)

def process(line, scale, out_file):
	# process each section
	elems = string.split(line)
	section = elems[0]
	new_pairs = []
	new_line = ""
	if section == "info":
		for pair in elems:
			splitted_pair = string.split(pair, "=")
			if splitted_pair[0] == "size" or splitted_pair[0] == "stretchH":
				splitted_pair[1] = str( int(splitted_pair[1])*scale )

			if len(splitted_pair) == 2:
				new_pair = splitted_pair[0] + "=" + splitted_pair[1]
			else:
				new_pair = pair
			new_pairs.append(new_pair)
	elif section == "common":
		for pair in elems:
			splitted_pair = string.split(pair, "=")
			if splitted_pair[0] == "lineHeight" or splitted_pair[0] == "base"  or splitted_pair[0] == "scaleW" or splitted_pair[0] == "scaleH":
				splitted_pair[1] = str( int(splitted_pair[1])*scale )

			if len(splitted_pair) == 2:
				new_pair = splitted_pair[0] + "=" + splitted_pair[1]
			else:
				new_pair = pair
			new_pairs.append(new_pair)
	elif section == "page":
		for pair in elems:
			splitted_pair = string.split(pair, "=")
			if splitted_pair[0] == "file":
				# we assume that .png file is the same as the output one
				splitted_pair[1] = '"' + out_file[:-4] + ".png" + '"'

			if len(splitted_pair) == 2:
				new_pair = splitted_pair[0] + "=" + splitted_pair[1]
			else:
				new_pair = pair
			new_pairs.append(new_pair)
	elif section == "char":
		for pair in elems:
			splitted_pair = string.split(pair, "=")
			if splitted_pair[0] == "x" or splitted_pair[0] == "y"  or splitted_pair[0] == "width" or splitted_pair[0] == "height" or splitted_pair[0] == "xadvance":
				splitted_pair[1] = str( int(splitted_pair[1])*scale )

			if len(splitted_pair) == 2:
				new_pair = splitted_pair[0] + "=" + splitted_pair[1]
			else:
				new_pair = pair
			new_pairs.append(new_pair)
	else:
		new_line = line
		if line[-1] == '\n':
			new_line = new_line[:-1]

	# merge a final new line
	for pair in new_pairs:
		new_line += pair + " "
	return new_line

# check if the file exists & read lines
if len(sys.argv) != 4:
	print "Usage: %s input.fnt output.fnt 2" % os.path.basename(sys.argv[0])
	error("Insufficient arguments.")

try:
	input_file  = sys.argv[1]
	output_file = sys.argv[2] 
	scale = int(sys.argv[3])

	# reading original
	out_lines = []
	with open(input_file) as f:
		lines = f.readlines()
		elems = string.split(lines[0])
		if elems[0] != "info":
			error("Probably not a BMFont file!")
		for l in lines:
			out_line = process(l, scale, output_file) + "\n"
			out_lines.append(out_line)

	# writing new one
	with open(output_file, "w") as f:
		f.writelines(out_lines)

except IOError as e:
	error("I/O error! %s" % e.strerror)
except:
	error("Unexpected error!")

